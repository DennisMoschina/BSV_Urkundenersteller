from urkundenersteller.models import Certificate
from urkundenersteller.reportlabUI.HStack import HStack
from urkundenersteller.reportlabUI.VStack import VStack
from urkundenersteller.reportlabUI.Image import Image
from urkundenersteller.reportlabUI.Spacer import Spacer
from urkundenersteller.reportlabUI.Text import Text
from urkundenersteller.reportlabUI.View import View


class CertificateView(View):

    def __init__(self, certificate: Certificate):
        super(CertificateView, self).__init__()
        self.__certificate = certificate

    def view(self) -> View:
        return VStack([
            HStack.create(range(7), lambda i: Image("../resources/BSV_Logo.png", width=85, height=93)),
            Text("Urkunde", 96)
            .padding(20),
            Text(self.__certificate.tournament.name, 40),
            Text(self.__certificate.discipline.ageGroup.name, 40)
            .padding(10),
            Text(f"Ausrichter: {self.__certificate.tournament.organizer.name}", 16),
            Spacer(10),
            Text(self.__certificate.discipline.__str__(), 48)
            .padding(10),
            Text(f"{self.__certificate.place}. Platz", 48)
            .padding(10),
            VStack.create(self.__certificate.players, lambda player: Text(player.name, 48).padding(10)),
            HStack([
                VStack([
                    Spacer(150),
                    HStack([
                        Text("Eggenstein,", 12),
                        Text(self.__certificate.tournament.date.strftime("%d.%m.%Y"), 12),
                        Text("_____________________________________", 12)
                    ])
                ]),
                Image("../resources/player_logo.png")
            ])
        ])
