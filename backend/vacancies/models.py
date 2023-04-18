from typing import List, Optional

from app.core.models import BaseCreatedAtModel, BaseDBModel
from tortoise import fields
import enum
from tortoise.contrib.pydantic import pydantic_model_creator


class EXPIERENCE_TYPES(str, enum.Enum):
    noExpierence = 'Нет опыта'
    between1And3 = 'От 1 года до 3 лет'


class VacancySkill(BaseDBModel):
    skill = fields.ForeignKeyField(
        'models.Skill', related_name='vacancy_skills', null=True, on_delete=fields.SET_NULL
    )
    vacancy = fields.ForeignKeyField(
        'models.Vacancy', related_name='vacancy_skills', null=True, on_delete=fields.SET_NULL
    )


class Skill(BaseDBModel):
    name = fields.CharField(max_length=255)
    vacancies: fields.ReverseRelation['VacancySkill']


class ProfRole(BaseDBModel):
    name = fields.CharField(max_length=255)
    # vacancies: fields.ManyToManyRelation['Vacancy']

class VacancyProfRole(BaseDBModel):
    role = fields.ForeignKeyField(
        'models.ProfRole', related_name='vacancy_profrole', null=True, on_delete=fields.CASCADE
    )
    vacancy = fields.ForeignKeyField(
        'models.Vacancy', related_name='vacancy_profrole', null=True, on_delete=fields.CASCADE
    )

class Vacancy(BaseDBModel):
    name = fields.CharField(max_length=512, default='')
    salary_defined = fields.BooleanField(default=False)
    salary_from = fields.IntField(null=True)
    salary_to = fields.IntField(null=True)
    schedule = fields.CharField(max_length=512, default='')
    description = fields.TextField(default='')
    published_at = fields.DatetimeField()
    created_at = fields.DatetimeField()
    remote = fields.BooleanField(default=False)
    employer: fields.ForeignKeyNullableRelation['Employer'] = fields.ForeignKeyField(
        'models.Employer', related_name='vacancies', null=True, on_delete=fields.SET_NULL
    )
    roles: Optional[fields.ReverseRelation['ProfRole']]
    expierence = fields.CharEnumField(EXPIERENCE_TYPES, default=EXPIERENCE_TYPES.noExpierence)
    address = fields.TextField(default='')
    lat = fields.CharField(max_length=16, default='')
    lon = fields.CharField(max_length=16, default='')
    vacancy_skills: Optional[fields.ReverseRelation['VacancySkill']]


class Employer(BaseDBModel):
    name = fields.CharField(max_length=255, default='')
    url = fields.CharField(max_length=255, default='')
    vacancies: fields.ReverseRelation[Vacancy]


class Subscription(BaseCreatedAtModel):
    user = fields.ForeignKeyField(
        'users.User', related_name='subscriptions', on_delete=fields.CASCADE
    )
    employer = fields.ForeignKeyField(
        'models.Employer', related_name='subscribed', on_delete=fields.CASCADE
    )

class Note(BaseCreatedAtModel):
    user = fields.ForeignKeyField(
        'users.User', related_name='bookmarks', on_delete=fields.CASCADE
    )
    vacancy = fields.ForeignKeyField(
        'models.Vacancy', related_name='bookmarks', on_delete=fields.CASCADE
    )
    content = fields.TextField(default='')


