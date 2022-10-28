import unittest

from urkundenersteller.logic import parse_winner_input
from urkundenersteller.models import Certificate
from urkundenersteller.models import DisciplineType


class CreateCertificatesTest(unittest.TestCase):
    def test_single(self):
        file_path: str = "resources/winnerSingle.CSV"

        with open(file_path, "rb") as f:
            certificates: list[Certificate] = parse_winner_input(f.read())
        self.assertEqual(8, len(certificates))
        for certificate in certificates:
            self.assertEqual(certificate.discipline.disciplineType, DisciplineType.SINGLE)
            self.assertEqual(1, len(certificate.players))

    def test_double(self):
        file_path: str = "resources/winnerDouble.CSV"

        with open(file_path, "rb") as f:
            certificates: list[Certificate] = parse_winner_input(f.read())
        self.assertEqual(8, len(certificates))
        for certificate in certificates:
            self.assertEqual(certificate.discipline.disciplineType, DisciplineType.DOUBLE)
            self.assertEqual(2, len(certificate.players))


if __name__ == '__main__':
    unittest.main()
