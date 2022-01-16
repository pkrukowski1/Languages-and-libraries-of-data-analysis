from src.voice_assistant_modules.exchange import Exchange
from src.voice_assistant_modules.module_observer import ModuleObserver
from src.voice_assistant_modules.va_module import VAModule

import json

from ..utils.paths import get_log_path


class ModuleLogger(ModuleObserver):
    def __init__(self, module: VAModule, log_path=get_log_path()):
        self.module = module
        from os import path
        self.path_to_file = path.join(log_path, module.get_name() + ".json")

    def notify(self, exchange: Exchange):
        self.log(exchange)

    def log(self, exchange: Exchange):
        try:
            json_struct = json.load(open(self.path_to_file, 'r'))
        except FileNotFoundError:
            json_struct = []
        with open(self.path_to_file, 'w') as log_file:
            json_struct.append(exchange.to_dict())
            log_file.write(json.dumps(json_struct, default=str))
