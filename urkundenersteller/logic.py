import datetime
import json
import re
from typing import Any

import chardet
import pandas as pd
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.models import AgeGroup
from urkundenersteller.models import Certificate
from urkundenersteller.models import Club
from urkundenersteller.models import Discipline
from urkundenersteller.models import DisciplineType
from urkundenersteller.models import Gender
from urkundenersteller.models import Player
from urkundenersteller.models import Tournament

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

tournament: Tournament = Tournament(name="Testturnier", date=datetime.date.today(), organizer=Club(name="Testverein"))


def create_tournament(tournament_name: str, date: datetime.date, organizer_name: str):
    global tournament
    tournament = Tournament(name=tournament_name, date=date, organizer=Club(name=organizer_name))


def parse_discipline_type(discipline_type_str: str) -> DisciplineType:
    """
    Parses the discipline type from the given string.
    @param discipline_type_str: The string to parse the discipline type from.
    @return: The parsed discipline type.
    """
    return [k for k, v in discipline_type_regex_map.items() if v == discipline_type_str][0]


def parse_gender(gender_str: str) -> Gender:
    """
    Parses the string as a Gender.
    @param gender_str the string to parse
    @return the gender based on the input
    """
    return [k for k, v in gender_regex_map.items() if v == gender_str][0]


def parse_age_group(age_group_str: str) -> AgeGroup:
    """
    Parses the age group from the given string.
    @param age_group_str: The string to parse the age group from.
    @return The parsed age group.
    """
    return [k for k, v in age_group_regex_map.items() if v == age_group_str][0]


def parse_discipline(discipline_str: str) -> Discipline:
    """
    Parses the discipline from the given string.
    @param discipline_str: The string to parse the discipline from.
    @return The parsed discipline.
    """
    pattern = re.compile(discipline_regex)
    match = pattern.match(discipline_str)
    dis_type: DisciplineType = parse_discipline_type(match.group("dis_type"))
    age_group: AgeGroup = parse_age_group(match.group("age_group"))
    gender: Gender = parse_gender(match.group("gender"))

    return Discipline(age_group=age_group, discipline_type=dis_type, gender=gender)


def discipline_to_string(discipline: Discipline) -> str:
    """
    Create a String representation of the given discipline.
    @param discipline: The discipline to create a String representation for.
    @return: The String representation of the given discipline.
    """

    age_group_str: str = age_group_regex_map[discipline.ageGroup]

    if discipline.disciplineType == DisciplineType.MIXED:
        return f"Mixed {age_group_str}"

    gender_str: str = "Jungen" if discipline.gender == Gender.MALE else "Mädchen"
    discipline_type_str: str = "Doppel" if discipline.disciplineType == DisciplineType.DOUBLE else "Einzel"
    return f"{gender_str}-{discipline_type_str} {age_group_str}"


def parse_club(club_name: str) -> Club:
    return Club(name=club_name)


def parse_player(player_name: str, club: Club) -> Player:
    return Player(name=player_name, club=club)


def parse_place(place_str: str) -> int:
    return int(place_str)


def create_certificate(discipline: Discipline, data_frame: pd.DataFrame) -> Certificate:
    assert discipline.disciplineType == DisciplineType.SINGLE and len(data_frame) == 1 or \
           discipline.disciplineType != DisciplineType.SINGLE and len(data_frame) == 2

    place: int = parse_place(data_frame.iloc[0]["Pos."])
    club: Club = parse_club(data_frame.iloc[0]["Verein"])
    player: Player = parse_player(data_frame.iloc[0]["Name"], club)

    # TODO: make work for doubles and mixed
    # TODO: add real tournament
    return Certificate(discipline=discipline, place=place, players=[player], tournament=tournament)


def create_certificats_for_discipline(discipline: Discipline, data_frame: pd.DataFrame) -> list[Certificate]:
    if discipline.disciplineType == DisciplineType.SINGLE:
        step_size: int = 1
    else:
        assert len(data_frame) % 2 == 0
        step_size: int = 2

    certificates: list[Certificate] = []
    for i in range(0, len(data_frame), step_size):
        certificates.append(create_certificate(discipline, data_frame.iloc[i:i + step_size]))
    return certificates


def parse_winner_input(file: bytes) -> list[Certificate]:
    """
    Parses the input file and returns a list of certificates.
    @param file: The input file read as bytes
    """
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
    str_discipline_map: dict[str, Discipline] = {}

    for discipline_str in discipline_strings:
        row = data_frame.index[data_frame["Konkurrenz"] == discipline_str]
        discipline_index_map[discipline_str] = row[0]
        str_discipline_map[discipline_str] = parse_discipline(discipline_str)

    # map disciplines to their respective dataframes
    discipline_data_frame_map: dict[Discipline, pd.DataFrame] = {}
    # create a dataframe for each discipline
    for i, discipline_str in enumerate(discipline_strings):
        start_index = discipline_index_map[discipline_str] + 1
        end_index = (discipline_index_map[discipline_strings[i + 1]]) if (i + 1 < len(discipline_strings)) else len(
            data_frame)
        # create DataFrame for discipline from start_index to end_index while excluding "Konkurrenz" column
        discipline: Discipline = str_discipline_map[discipline_str]
        discipline_data_frame_map[discipline] = data_frame.iloc[start_index:end_index, 1:]

    print(f"dataframes: {discipline_data_frame_map}")

    certificates: list[Certificate] = []

    # iterate over disciplines and create certificates from their dataframes
    for discipline, data_frame in discipline_data_frame_map.items():
        certificates.extend(create_certificats_for_discipline(discipline, data_frame))

    return certificates


def place_centred_text_on_pdf(pdf: Canvas, text: str, x: float, y: float, font_size: int, font: str):
    pdf.setFontSize(font_size)  # TODO set font
    pdf.drawCentredString(x, y, text)


def get_style_of_text(style: dict[str, Any]) -> dict[str, Any]:
    font_size: int = style["fontSize"]
    font: str = style["font"]
    padding: int = style["padding"]
    return dict(fontSize=font_size, font=font, padding=padding)


def create_pdf_from_certificate(certificate: Certificate) -> bytes:
    """
    Creates a pdf from the given certificate.
    @param certificate: The certificate to create a pdf from.
    @return: The pdf as bytes.
    """

    resources_path: str = "urkundenersteller/resources"
    format_resource: str = f"{resources_path}/urkunde_format.json"

    pdf: Canvas = Canvas("Urkunde.pdf", pagesize=A4)

    canvas_width: int = pdf._pagesize[0]
    canvas_height: int = pdf._pagesize[1]

    canvas_width_center: float = canvas_width / 2

    format_file = open(format_resource)
    format_json: dict[str, Any] = json.load(format_file)
    format_file.close()

    vertical_position: float = canvas_height

    for key in format_json.keys():
        element: dict[str, Any] = format_json[key]
        assert isinstance(element, dict)
        element_type: str = element["type"]

        if element_type == "string":
            text: str = element["text"]
            style: dict[str, Any] = get_style_of_text(element["style"])
            font_size: int = style["fontSize"]

            vertical_position -= font_size
            place_centred_text_on_pdf(pdf, text, canvas_width_center, vertical_position, font_size, style["font"])

        if element_type == "f string":
            element_text: str = element["text"]
            text: str = eval(f'f"{element_text}"')      # this is a security risk
            style: dict[str, Any] = get_style_of_text(element["style"])
            font_size: int = style["fontSize"]
            font: str = style["font"]

            vertical_position -= font_size + style["padding"]
            place_centred_text_on_pdf(pdf, text, canvas_width_center, vertical_position, font_size, font)
            vertical_position -= style["padding"]

        if element_type == "property":
            element_text: str = element["text"]
            element_text = "{" + element_text + "}"
            text: str = eval(f'f"{element_text}"')      # this is a security risk

            style: dict[str, Any] = get_style_of_text(element["style"])
            font_size: int = style["fontSize"]
            font: str = style["font"]

            vertical_position -= font_size + style["padding"]
            place_centred_text_on_pdf(pdf, text, canvas_width_center, vertical_position, font_size, font)
            vertical_position -= style["padding"]

        if element_type == "image":
            pass
        if element_type == "image banner":
            image_path: str = element["image"]
            image_path = f"{resources_path}/{image_path}"
            width: float = canvas_width / int(element["count"])
            aspect_ratio: (int, int) = element["aspectRatio"].split(":")
            height: float = width / (int(aspect_ratio[0]) / int(aspect_ratio[1]))

            vertical_position -= height
            for i in range(int(element["count"])):
                pdf.drawImage(image_path, i * width, vertical_position, width=width, height=height)

    pdf.save()
