from urkundenersteller.models import Certificate
from urkundenersteller.reportlabUI.HStack import HStack
from urkundenersteller.reportlabUI.Spacer import Spacer
from urkundenersteller.reportlabUI.Text import Text
from urkundenersteller.reportlabUI.View import View


class CertificateView(View):

    def __init__(self, certificate: Certificate):
        super(CertificateView, self).__init__()
        self.__certificate = certificate

    def view(self) -> View:
        return HStack([
            Text("Urkunde", 96)
            .padding(30),
            Text(self.__certificate.tournament.name, 40),
            Text(self.__certificate.discipline.ageGroup.name, 40)
            .padding(10),
            Text(f"Ausrichter: {self.__certificate.tournament.organizer.name}", 16),
            Spacer(10),
            Text(self.__certificate.discipline.__str__(), 48)
            .padding(10),
            Text(f"{self.__certificate.place}. Platz", 48)
            .padding(10)
        ])
