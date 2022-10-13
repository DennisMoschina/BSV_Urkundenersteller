import datetime

from django.db import models

from enum import Enum


# Create your models here.


class Gender(Enum):
    MALE = 1
    FEMALE = 2


class AgeGroup(Enum):
    U9 = 1
    U11 = 2
    U13 = 3
    U15 = 4
    U17 = 5
    U19 = 6
    U21 = 7


class DisciplineType(Enum):
    SINGLE = 1
    DOUBLE = 2
    MIXED = 3


class Discipline:
    disciplineType: DisciplineType
    ageGroup: AgeGroup
    gender: Gender


class Tournament:
    name: str
    date: datetime.date


class Club:
    name: str


class Player:
    firstName: str
    lastName: str
    club: Club


class Certificate:
    tournament: Tournament
    discipline: Discipline
    place: int
    players: list[Player]
