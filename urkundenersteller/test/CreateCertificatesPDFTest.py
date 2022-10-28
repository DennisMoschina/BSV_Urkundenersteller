import os
import unittest
from datetime import datetime

from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.logic import create_pdf_from_certificate
from urkundenersteller.models import AgeGroup
from urkundenersteller.models import Certificate
from urkundenersteller.models import Club
from urkundenersteller.models import Discipline
from urkundenersteller.models import DisciplineType
from urkundenersteller.models import Gender
from urkundenersteller.models import Player
from urkundenersteller.models import Tournament


class CreateCertificatesPDFTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.exists("out"):
            os.mkdir("out")
        cls.counter = 0

    def setUp(self) -> None:
        self.pdf = Canvas(f"out/test{self.counter}.pdf", bottomup=0)

    def tearDown(self) -> None:
        self.pdf.save()
        self.counter += 1

    def test_create_single_certificate(self):
        certificate: Certificate = Certificate(
            tournament=Tournament(name="Testturnier", date=datetime.now(), organizer=Club(name="Testverein")),
            discipline=Discipline(discipline_type=DisciplineType.SINGLE, age_group=AgeGroup.U19, gender=Gender.MALE),
            place=1,
            players=[Player(name="Testspieler", club=Club(name="Testverein"))]
        )
        create_pdf_from_certificate(certificate, self.pdf)

    def test_create_double_certificate(self):
        certificate: Certificate = Certificate(
            tournament=Tournament(name="Testturnier", date=datetime.now(), organizer=Club(name="Testverein")),
            discipline=Discipline(discipline_type=DisciplineType.DOUBLE, age_group=AgeGroup.U19, gender=Gender.MALE),
            place=1,
            players=[
                Player(name="Testspieler 1",
                       club=Club(name="Testverein")),
                Player(name="Testspieler 2",
                       club=Club(name="Testverein"))
            ]
        )
        create_pdf_from_certificate(certificate, self.pdf)


if __name__ == '__main__':
    unittest.main()
