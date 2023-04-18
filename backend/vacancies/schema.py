from tortoise.contrib.pydantic import pydantic_model_creator
from vacancies.models import Vacancy, Employer, VacancySkill, Skill
from typing import Optional, List
from pydantic import BaseModel


BaseVacancyPydantic = pydantic_model_creator(Vacancy)
EmployerPydantic = pydantic_model_creator(Employer)
BaseVacancySkillPydantic = pydantic_model_creator(VacancySkill)
BaseSkillPydantic = pydantic_model_creator(Skill)


class SkillPydantic(BaseSkillPydantic):
    name: Optional[str]
    id: Optional[int]

    def __init__(self):
        super().__init__()

class VacancySkillPydantic(BaseVacancySkillPydantic):
    skill: Optional[SkillPydantic]

    class Meta:
        exclude = ['vacancies', ]

    def __init__(self):
        super().__init__()

# Vacancy_Pydantic = pydantic_model_creator(Vacancy)
class Vacancy_Pydantic(BaseVacancyPydantic):
    vacancy_skills: Optional[List[VacancySkillPydantic]]
    employer: Optional[EmployerPydantic]

class AddVacancyResponse(BaseModel):
    message: str
