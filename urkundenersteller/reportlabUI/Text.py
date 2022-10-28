from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.Frame import Frame
from urkundenersteller.reportlabUI.Frame import FrameType
from urkundenersteller.reportlabUI.View import View


class Text(View):
    __text: str
    __size: int
    __font: str

    def __init__(self, text: str, size: int = 12, font: str = ''):
        super(Text, self).__init__()
        self.__text = text
        self.__size = size
        self.__font = font

    def manage_fonts(self, canvas: Canvas):
        if self.__font == '':
            canvas.setFontSize(self.__size)
            return
        if self.__font not in canvas.getAvailableFonts():
            pdfmetrics.registerFont(TTFont(self.__font, self.__font + ".ttf"))

        canvas.setFont(self.__font, self.__size)

    def get_text_width(self) -> float:
        return stringWidth(self.__text, self.__font if self.__font != '' else 'Courier', self.__size)

    def get_content_size(self) -> tuple[float, float]:
        return self.get_text_width(), self.__size

    def build_view(self, canvas: Canvas,
                   top_left_corner: tuple[float, float] = (0, 0),
                   frame: Frame = Frame()) -> tuple[float, float]:
        self.manage_fonts(canvas)

        width = self.get_text_width()

        if frame.width[1] == FrameType.FIXED:
            width = frame.width[0]
        elif frame.width[1] == FrameType.MINIMUM:
            width = canvas._pagesize[0] - top_left_corner[0]
        elif frame.width[1] == FrameType.MAXIMUM:
            width = frame.width[0]

        # TODO: make work for left align and right align

        height: float = self.get_preferred_size()[1]

        if frame.height[1] == FrameType.FIXED:
            height = frame.height[0]
        elif frame.height[1] == FrameType.MINIMUM:
            # TODO: implement
            height = max(height, frame.height[0])
        elif frame.height[1] == FrameType.MAXIMUM:
            # TODO: implement
            pass

        extra_padding: float = (height - self.get_preferred_size()[1]) / 2

        x_pos: float = top_left_corner[0] + (width / 2)
        y_pos: float = top_left_corner[1] + extra_padding + self.__size

        canvas.drawCentredString(x_pos, y_pos, self.__text)
        return top_left_corner[0] + width, top_left_corner[1] + self.__size + extra_padding * 2
