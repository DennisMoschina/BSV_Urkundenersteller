from reportlab.pdfgen.canvas import Canvas

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

    def view(self, canvas: Canvas):
        self.increase_vertical_position(self.__size)
        if self.__font == '':
            canvas.setFontSize(self.__size)
        else:
            canvas.setFont(self.__font, self.__size)
        canvas.drawCentredString(canvas._pagesize[0] / 2, canvas._pagesize[1] - self.get_vertical_position(), self.__text)
