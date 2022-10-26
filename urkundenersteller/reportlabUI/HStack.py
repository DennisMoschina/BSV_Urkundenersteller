from typing import Callable

from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.Frame import Frame
from urkundenersteller.reportlabUI.Frame import FrameType
from urkundenersteller.reportlabUI.Stack import Stack
from urkundenersteller.reportlabUI.View import View


class HStack(Stack):

    def __init__(self, views: list[View]):
        super(HStack, self).__init__(views)
        self.__views: list[View] = views

    @classmethod
    def create(cls, items: list, create_view: Callable[[any], View]) -> 'HStack':
        views = [create_view(item) for item in items]
        return HStack(views)

    def build_view(self, canvas: Canvas,
                   top_left_corner: tuple[float, float] = (0, 0),
                   frame: Frame = Frame()) -> tuple[float, float]:
        # TODO: use Frame

        bottom_right_corner = top_left_corner
        for view in self.__views:
            frame = Frame(width=(view.get_min_size()[0], FrameType.MAXIMUM))
            bottom_right_corner = view.render_view(canvas, (bottom_right_corner[0], top_left_corner[1]), frame)

        return bottom_right_corner

    def get_min_size(self) -> tuple[float, float]:
        min_width = 0
        min_height = 0
        for view in self.__views:
            min_width += view.get_min_size()[0]
            min_height = max(min_height, view.get_min_size()[1])
        return min_width, min_height
