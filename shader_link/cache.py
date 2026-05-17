
import json
import shader_link.config

class Cache:
    def __init__ (self, data : dict):
        self.data: dict = data

    def update (self, filename : str, checksum : str) -> None:
        self.data [filename] = { "checksum" : checksum }

    def is_actual (self, filename : str, checksum : str) -> bool:
        if filename in self.data:
            return self.data [filename] ["checksum"] == checksum
        else:
            return False

class CacheStorage:
    def __init__ (self, config : shader_link.config.Config):
        self.path = config.cache_path

    def load (self) -> Cache:
        if not self.path.exists ():
            return Cache ({})

        try:
            with open (self.path, 'r', encoding='utf-8') as file:
                return Cache (json.load (file))
        except json.JSONDecodeError:
            self.path.unlink ()
            return Cache ({})

    def dump (self, cache : Cache) -> None:
        with open (self.path, 'w', encoding='utf-8') as file:
            json.dump (cache.data, file, indent=4, ensure_ascii=False)
