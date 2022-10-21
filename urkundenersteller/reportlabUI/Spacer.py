from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.View import View


class Spacer(View):
    __size: float

    def __init__(self, size: float = 10):
        super(Spacer, self).__init__()
        self.__size = size

    def build_view(self, canvas: Canvas):
        self.increase_vertical_position(self.__size)
