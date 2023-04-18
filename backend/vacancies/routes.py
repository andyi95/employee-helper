from app.core.types import URL
from .models import Vacancy
from vacancies.schema import Vacancy_Pydantic
from fastapi import APIRouter, BackgroundTasks
from typing import List, Optional, Union
from urllib.parse import urlparse


from .schema import AddVacancyResponse

router = APIRouter()


@router.get('/', response_model=List[Vacancy_Pydantic], status_code=200, tags=['vacancies'])
async def get_vacancies(offset: int = 0, limit: int = 100):
    objects = await Vacancy.all().prefetch_related(
        'vacancy_skills', 'vacancy_skills__skill', 'employer'
    ).limit(limit).offset(offset)
    return objects

@router.post('/', response_model=AddVacancyResponse, status_code=201, tags=['vacancies'])
async def add_vacancy(vacancy: Union[int, URL], background_tasks: BackgroundTasks):
    """Добавить вакансию в список отслеживаемых. На вход ожидается id вакансии или ссылка на неё."""
    from services.parse_hh import HHParser
    if isinstance(vacancy, URL):
        parsed = urlparse(vacancy)
        vacancy = parsed.path.split('/')[-1]
    background_tasks.add_task(HHParser().get_vacancy(vacancy))
    return {"message": "Parsing started"}
