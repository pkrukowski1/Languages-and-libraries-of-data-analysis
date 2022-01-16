import abc

from src.voice_assistant_modules.exchange import Exchange


class ModuleObserver(abc.ABC):
    @abc.abstractmethod
    def notify(self, exchange: Exchange):
        pass

