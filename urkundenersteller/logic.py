import re

import chardet
import pandas as pd
import io

from urkundenersteller.models import AgeGroup
from urkundenersteller.models import Certificate
from urkundenersteller.models import Discipline
from urkundenersteller.models import DisciplineType
from urkundenersteller.models import Gender

gender_regex_map: dict[Gender, str] = {Gender.MALE: "J", Gender.FEMALE: "M"}
discipline_type_regex_map: dict[DisciplineType, str] = {
    DisciplineType.SINGLE: "E",
    DisciplineType.DOUBLE: "D",
    DisciplineType.MIXED: "MX"
}
age_group_regex_map: dict[AgeGroup, str] = dict(map(lambda a: (a, str(a.name)), [a for a in AgeGroup]))

gender_regex: str = "|".join(gender_regex_map.values())
discipline_type_regex: str = "|".join(discipline_type_regex_map.values())
age_group_regex: str = "|".join(age_group_regex_map.values())

discipline_regex: str = f"(?P<dis_type_w_gender>(?P<gender>{gender_regex})(?P<dis_type>{discipline_type_regex})" \
                        f"|{discipline_type_regex_map[DisciplineType.MIXED]})" \
                        f" (?P<age_group>{age_group_regex})"


def parse_discipline_type(discipline_type_str: str) -> DisciplineType:
    return [k for k, v in discipline_type_regex_map.items() if v == discipline_type_str][0]


def parse_gender(gender_str: str) -> Gender:
    return [k for k, v in gender_regex_map.items() if v == gender_str][0]


def parse_age_group(age_group_str: str) -> AgeGroup:
    return [k for k, v in age_group_regex_map.items() if v == age_group_str][0]


def parse_discipline(discipline_str: str) -> Discipline:
    pattern = re.compile(discipline_regex)
    match = pattern.match(discipline_str)
    dis_type: DisciplineType = parse_discipline_type(match.group("dis_type"))
    age_group: AgeGroup = parse_age_group(match.group("age_group"))
    gender: Gender = parse_gender(match.group("gender"))

    discipline = Discipline()
    discipline.type = dis_type
    discipline.age_group = age_group
    discipline.gender = gender
    return discipline


def parse_winner_input(file: bytes) -> list[Certificate]:
    encoding = chardet.detect(file)

    bytes_io: io.BytesIO = io.BytesIO(file)
    bytes_io.seek(0)
    data_frame: pd.DataFrame = pd.read_csv(bytes_io, sep=",",
                                           encoding=encoding["encoding"],
                                           skiprows=1,
                                           usecols=["Konkurrenz", "Pos.", "Name", "Verein"])

    print(data_frame)

    discipline_strings: list[str] = data_frame["Konkurrenz"].unique()
    # remove nan from disciplines
    discipline_strings = [x for x in discipline_strings if str(x) != 'nan']

    # map disciplines to their index in the dataframe
    discipline_index_map: dict[str, int] = {}

    for discipline_str in discipline_strings:
        row = data_frame.index[data_frame["Konkurrenz"] == discipline_str]
        discipline_index_map[discipline_str] = row[0]
        print(f"Discipline: {parse_discipline(discipline_str)}")

    print(discipline_index_map)

    # map disciplines to their respective dataframes
    discipline_str_data_frame_map: dict[str, pd.DataFrame] = {}
    # create a dataframe for each discipline
    for i, discipline_str in enumerate(discipline_strings):
        start_index = discipline_index_map[discipline_str] + 1
        end_index = (discipline_index_map[discipline_strings[i + 1]] - 1) if (i + 1 < len(discipline_strings)) else len(data_frame)
        # create DataFrame for discipline from start_index to end_index while excluding "Konkurrenz" column
        discipline_str_data_frame_map[discipline_str] = data_frame.iloc[start_index:end_index, 1:]

    print(f"dataframes: {discipline_str_data_frame_map}")



    certificates: list[Certificate] = []
    return certificates
