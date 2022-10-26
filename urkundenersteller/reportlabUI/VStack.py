from typing import Callable

from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.Frame import Frame
from urkundenersteller.reportlabUI.Stack import Stack
from urkundenersteller.reportlabUI.View import View


class VStack(Stack):

    def __init__(self, views: list[View]):
        super(VStack, self).__init__(views)
        self.__views: list[View] = views

    @classmethod
    def create(cls, items: list, create_view: Callable[[any], View]) -> 'VStack':
        views = [create_view(item) for item in items]
        return VStack(views)

    def build_view(self, canvas: Canvas,
                   top_left_corner: tuple[float, float] = (0, 0),
                   frame: Frame = Frame()) -> tuple[float, float]:
        # TODO: use Frame

        bottom_right_corner = top_left_corner
        for view in self.__views:
            bottom_right_corner = view.render_view(canvas, (top_left_corner[0], bottom_right_corner[1]))

        return bottom_right_corner

    def get_min_size(self) -> tuple[float, float]:
        min_width = 0
        min_height = 0
        for view in self.__views:
            min_width = max(min_width, view.get_min_size()[0])
            min_height += view.get_min_size()[1]
        return min_width, min_height
