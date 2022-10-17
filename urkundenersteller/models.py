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

    def __init__(self, discipline_type: DisciplineType, age_group: AgeGroup, gender: Gender):
        self.disciplineType = discipline_type
        self.ageGroup = age_group
        self.gender = gender


class Tournament:
    name: str
    date: datetime.date

    def __init__(self, name: str, date: datetime.date):
        self.name = name
        self.date = date


class Club:
    name: str

    def __init__(self, name: str):
        self.name = name


class Player:
    name: str
    club: Club

    def __init__(self, name: str, club: Club):
        self.name = name
        self.club = club


class Certificate:
    tournament: Tournament
    discipline: Discipline
    place: int
    players: list[Player]

    def __init__(self, tournament: Tournament, discipline: Discipline, place: int, players: list[Player]):
        self.tournament = tournament
        self.discipline = discipline
        self.place = place
        self.players = players
