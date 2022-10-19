from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.View import View


class HStack(View):

    def __init__(self, views: list[View]):
        super(HStack, self).__init__()
        self.__views: list[View] = views
        for view in self.__views:
            view.set_parent(self)

    def view(self, canvas: Canvas):
        for view in self.__views:
            view.render_view(canvas)

