import enum


class FrameType(enum.Enum):
    """Enum for the different types of frames"""
    FIXED = 0
    MINIMUM = 1
    MAXIMUM = 2


class Frame:
    height: (float, FrameType)
    width: (float, FrameType)

    def __init__(self, height: (float, FrameType) = (0, FrameType.MINIMUM),
                 width: (float, FrameType) = (0, FrameType.MINIMUM)):
        self.height = height
        self.width = width
