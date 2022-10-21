from typing import Callable

from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.View import View


class ForEach(View):

    __items: list
    __create_view: Callable[[any], View]

    def __init__(self, items: list, create_view: Callable[[any], View]):
        super(ForEach, self).__init__()
        self.__items = items
        self.__create_view = create_view

    def build_view(self, canvas: Canvas):
        for item in self.__items:
            view: View = self.__create_view(item)
            view.set_parent(self)
            view.render_view(canvas)
