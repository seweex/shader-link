
import os

import shader_link.config
import shader_link.cache
import shader_link.execution
import shader_link.export
import shader_link.logger

class App:
    @staticmethod
    def make_config ():
        args = shader_link.config.Arguments ()
        compiler = shader_link.config.Compiler ()

        return shader_link.config.Config (args, compiler)

    def __init__ (self, config : shader_link.config.Config) -> None:
        os.system ('')

        self.config = config

        self.cache_storage = shader_link.cache.CacheStorage (self.config)
        self.task = shader_link.execution.Task (self.config)
        self.compiler = shader_link.execution.Compiler (self.config)
        self.exporter = shader_link.export.Exporter ()

    def run (self):
        cache = self.cache_storage.load ()

        for target in self.task.input_files:
            if not self.compiler.compile (self.config.forced, target, cache):
                continue

            if self.task.export:
                self.exporter.export (target ['output_path'], target ['export_path'], target ['name'])

        self.cache_storage.dump (cache)
