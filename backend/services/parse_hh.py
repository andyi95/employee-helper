from typing import Optional
from datetime import datetime
from app.core.init_app import get_app_list, get_tortoise_config
from tortoise import Tortoise
import requests
import asyncio
import json
import re
import logging
from .exceptions import CaptchaRequiredError
from vacancies.models import Employer, Skill, VacancySkill, Vacancy, VacancyProfRole, ProfRole
import time
import random
import logging.config
logger = logging.getLogger(__name__)


class HHParser:
    BASE_URL = 'https://api.hh.ru/vacancies/'

    def __init__(self, area: int = 113, text: str = 'Python backend', per_page: int = 100):
        self.params = {
            'area': area,
            'text': text,
            'per_page': per_page
        }
        self.session = requests.Session()

    def get_object(self, path, params=None):
        url = self.BASE_URL + path
        try:
            response = self.session.get(url, params=params).json()
            if not 'errors' in response.keys():
                return response
            if response['errors'][0]['value'] == 'captcha_required':
                raise CaptchaRequiredError(response['errors'][0]['captcha_url'])
        except (requests.RequestException, json.JSONDecodeError) as e:
            logging.exception(e)

    async def get_vacancy(self, vacancy_id: str, attempt: int=10):
        url = f'{self.BASE_URL}{vacancy_id}'
        data = requests.get(url).json()
        if 'errors' in data.keys() and attempt > 0:
            time.sleep(random.randint(1, 20) / 10)
            return self.get_vacancy(vacancy_id, attempt - 1)

        for dt_str in ('created_at', 'published_at'):
            value = datetime.strptime(data[dt_str], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None) if data.get(
                dt_str) else datetime.now()
            data[dt_str] = value

        vacancy = Vacancy(
            id=data['id'], name=data.get('name'), created_at=data['created_at'], published_at=data['published_at']
        )
        if 'employer' in data.keys():
            employer = await self.get_employer(data['employer'])
            vacancy.employer = employer
            await vacancy.save()
        vacancy_obj = await Vacancy.filter(id=data['id']).first()
        if not vacancy_obj:
            vacancy_obj = vacancy
        skills = []
        for d in data.get('key_skills'):
            skill = await self.get_skill(d['name'])
            skills.append(skill)
        await vacancy_obj.save()
        for skill in skills:
            await VacancySkill.get_or_create(vacancy=vacancy_obj, skill=skill)
        for role_data in data.get('professional_roles'):
            prof, _ = await ProfRole.get_or_create(id=role_data['id'], name=role_data['name'])
            await VacancyProfRole.get_or_create(role=prof, vacancy=vacancy_obj)
        return vacancy_obj

    async def get_skill(self, skill_name: str) -> Optional[Skill]:
        skill, created = await Skill.get_or_create(name=skill_name)
        return skill

    async def get_employer(self, data: dict):
        time.sleep(random.randint(1, 10)/10)
        employer, created = await Employer.get_or_create(id=int(data['id']), defaults={'name': data['name']})
        return employer

    async def get_pages(self):
        response = requests.get(self.BASE_URL, params=self.params)
        pages_amt = response.json().get('pages', -1)
        ids = []
        vacancies = []
        for i in range(pages_amt + 1):
            params = self.params
            params['page'] = i
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()
            if 'items' not in data:
                break
            for item in data['items']:
                item['id'] = int(item['id'])
                vacancy = await Vacancy.get_or_none(id=item['id'])
                if vacancy:
                    continue
                resp = self.get_vacancy(item['id'])
                item = resp if resp else item
                for dt_str in ('created_at', 'published_at'):
                    value = datetime.strptime(item[dt_str], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None) if item.get(
                        dt_str) else datetime.now()
                    item.update({dt_str: value})
                vacancy = await Vacancy.create(
                    id=int(item['id']), name=item['name'], description=item.get('description', ''), published_at=item[
                        'published_at'], created_at=item['created_at']
                )
                if 'key_skills' not in item.keys() or 'employer' not in item.keys():
                    await vacancy.save()
                    time.sleep(random.randint(2,15))
                    continue
                for skill in item['key_skills']:
                    skill_obj = await self.get_skill(skill['name'])
                    await VacancySkill.get_or_create(skill=skill_obj, vacancy=vacancy)

                if 'id' in item['employer'].keys():
                    vacancy.employer = await self.get_employer(item['employer'])

                await vacancy.save()
                time.sleep(random.randint(1,10))
                vacancies.append(vacancy)

async def main():
    await Tortoise.init(config=get_tortoise_config())
    Tortoise.init_models(get_app_list(), 'models')
    parser = HHParser()
    await parser.get_pages()

# if __name__ == '__main__':
#     asyncio.run(main())