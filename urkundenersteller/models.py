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

    def __str__(self):
        age_group_str: str = self.ageGroup.name

        if self.disciplineType == DisciplineType.MIXED:
            return f"Mixed {age_group_str}"

        gender_str: str = "Jungen" if self.gender == Gender.MALE else "Mädchen"
        discipline_type_str: str = "Doppel" if self.disciplineType == DisciplineType.DOUBLE else "Einzel"
        return f"{gender_str}-{discipline_type_str} {age_group_str}"


class Club:
    name: str

    def __init__(self, name: str):
        self.name = name


class Tournament:
    name: str
    date: datetime.date
    organizer: Club

    def __init__(self, name: str, date: datetime.date, organizer: Club):
        self.name = name
        self.date = date
        self.organizer = organizer


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
