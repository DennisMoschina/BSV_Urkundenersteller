from typing import Callable

from urkundenersteller.reportlabUI.View import View


class Stack(View):
    __views: list[View]

    def __init__(self, views: list[View]):
        super(Stack, self).__init__()
        self.__views = views

    @classmethod
    def create(cls, items: list, create_view: Callable[[any], View]) -> 'Stack':
        views = [create_view(item) for item in items]
        return Stack(views)
