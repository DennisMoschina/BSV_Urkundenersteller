from abc import ABC

from reportlab.pdfgen.canvas import Canvas

from urkundenersteller.reportlabUI.Frame import Frame


class View(ABC):
    __padding: float = 0

    def view(self) -> 'View':
        return self

    def build_view(self, canvas: Canvas,
                   top_left_corner: tuple[float, float] = (0, 0),
                   frame: Frame = Frame()) -> tuple[float, float]:
        return self.view().build_view(canvas)

    def render_view(self, canvas: Canvas,
                    top_left_corner: tuple[float, float] = (0, 0),
                    frame: Frame = Frame()) -> tuple[float, float]:
        view: View = self.view()

        top_left_corner = (top_left_corner[0], top_left_corner[1] + self.__padding)
        if view is self:
            bottom_right_corner = self.build_view(canvas, top_left_corner, frame)
        else:
            bottom_right_corner = self.view().render_view(canvas, top_left_corner, frame)

        bottom_right_corner = (bottom_right_corner[0], bottom_right_corner[1] + self.__padding)
        return bottom_right_corner

    def get_preferred_size(self) -> tuple[float, float]:
        size = self.view().get_preferred_size()
        for i in range(2):
            size[i] += 2 * self.__padding
        return size

    def get_min_size(self) -> tuple[float, float]:
        size = self.view().get_min_size()
        for i in range(2):
            size[i] += 2 * self.__padding
        return size

    # View modifiers

    def padding(self, amount: float = 10) -> 'View':
        self.__padding = amount
        return self
