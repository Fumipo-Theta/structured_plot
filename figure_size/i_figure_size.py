import abc


class IFigureSize(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def use(self)->dict:
        pass
