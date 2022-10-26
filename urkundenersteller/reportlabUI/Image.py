from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.Frame import Frame
from urkundenersteller.reportlabUI.View import View


class Image(View):
    __image: str

    def __init__(self, image: str, height: float = -1, width: float = -1):
        super(Image, self).__init__()
        self.__image = image
        self.__height = height
        self.__width = width

    def get_min_size(self) -> tuple[float, float]:
        return max(self.__width, 0), max(self.__height, 0)

    def get_preferred_size(self) -> tuple[float, float]:
        if self.__width >= 0 and self.__height >= 0:
            return self.__width, self.__height

        image = ImageReader(self.__image)
        (width, height) = image.getSize()
        return width if self.__width < 0 else self.__width, height if self.__height < 0 else self.__height

    def build_view(self, canvas: Canvas,
                   top_left_corner: tuple[float, float] = (0, 0),
                   frame: Frame = Frame()) -> tuple[float, float]:
        (width, height) = self.get_preferred_size()
        canvas.saveState()
        canvas.scale(1, -1)
        canvas.drawImage(self.__image, top_left_corner[0], - top_left_corner[1] - height, width=width, height=height)
        canvas.restoreState()
        return top_left_corner[0] + width, top_left_corner[1] + height
