from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.Frame import Frame
from urkundenersteller.reportlabUI.View import View


class Spacer(View):
    __size: float

    def __init__(self, size: float = 10):
        super(Spacer, self).__init__()
        self.__size = size

    def build_view(self, canvas: Canvas,
                   top_left_corner: tuple[float, float] = (0, 0),
                   frame: Frame = Frame()) -> tuple[float, float]:
        return top_left_corner[0] + self.__size, top_left_corner[1] + self.__size
