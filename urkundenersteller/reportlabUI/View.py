from abc import ABC
from abc import abstractmethod

from reportlab.pdfgen.canvas import Canvas


class View(ABC):
    __vertical_position: float = 0
    __parent: 'View' = None

    __padding: float = 0

    @abstractmethod
    def view(self, canvas: Canvas):
        pass

    def render_view(self, canvas: Canvas):
        if self.__parent is not None:
            self.set_vertical_position(self.__parent.get_vertical_position())
        self.increase_vertical_position(self.__padding)
        self.view(canvas)
        self.increase_vertical_position(self.__padding)
        if self.__parent is not None:
            self.__parent.set_vertical_position(self.__vertical_position)

    def set_vertical_position(self, vertical_position: float):
        self.__vertical_position = vertical_position

    def get_vertical_position(self) -> float:
        return self.__vertical_position

    def increase_vertical_position(self, amount: float):
        self.__vertical_position += amount

    def set_parent(self, parent: 'View'):
        self.__parent = parent

    def get_parent(self) -> 'View':
        return self.__parent

    # View modifiers

    def padding(self, amount: float = 10) -> 'View':
        self.__padding = amount
        return self
