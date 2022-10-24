from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.View import View


class Image(View):
    __image: str

    def __init__(self, image: str, height: float = -1, width: float = -1):
        super(Image, self).__init__()
        self.__image = image
        self.__height = height
        self.__width = width

    def build_view(self, canvas: Canvas):
        image = ImageReader(self.__image)
        (width, height) = image.getSize()
        width = width if self.__width < 0 else self.__width
        height = height if self.__height < 0 else self.__height

        self.increase_vertical_position(height)

        canvas.drawImage(image,
                         (canvas._pagesize[0] - width) / 2,
                         canvas._pagesize[1] - self.get_vertical_position(),
                         width,
                         height)
