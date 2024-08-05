import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError
