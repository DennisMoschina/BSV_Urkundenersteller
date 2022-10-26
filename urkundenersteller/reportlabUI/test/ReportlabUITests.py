import os
import unittest

from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.HStack import HStack
from urkundenersteller.reportlabUI.Image import Image
from urkundenersteller.reportlabUI.Text import Text
from urkundenersteller.reportlabUI.VStack import VStack


class MyTestCase(unittest.TestCase):

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

    def test_put_text_centered(self):
        top = 0
        for font in self.pdf.getAvailableFonts():
            view = Text(font, font=font)
            view.padding(10)
            top = view.render_view(self.pdf, (0, top))[1]

    def test_VStack_of_text(self):
        views: list[Text] = [Text("Use VStack", 50)]
        for font in self.pdf.getAvailableFonts():
            views.append(Text(font, font=font).padding(10))

        stack = VStack(views)
        stack.render_view(self.pdf, (0, 0))

    def test_VStack_from_items(self):
        items = self.pdf.getAvailableFonts()
        stack = VStack.create(items, lambda item: Text(item, font=item).padding(10))
        stack.render_view(self.pdf, (0, 0))

    def test_HStack_of_text(self):
        views: list[Text] = []
        for font in self.pdf.getAvailableFonts():
            views.append(Text(font, font=font).padding(10))

        stack = HStack(views)
        stack.render_view(self.pdf, (0, 0))

    def test_image_default_size(self):
        view = Image("resources/player_logo.png")
        view.render_view(self.pdf, (0, -466))


if __name__ == '__main__':
    unittest.main()
