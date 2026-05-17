
import os

import shader_link.config
import shader_link.cache
import shader_link.execution
import shader_link.logger

class App:
    @staticmethod
    def _make_config ():
        args = shader_link.config.Arguments ()
        compiler = shader_link.config.Compiler ()

        return shader_link.config.Config (args, compiler)

    def __init__ (self) -> None:
        try:
            os.system ('')

            self.config = self._make_config ()

            self.cache_storage = shader_link.cache.CacheStorage (self.config)
            self.task = shader_link.execution.Task (self.config)
            self.compiler = shader_link.execution.Compiler (self.config)

        except KeyboardInterrupt:
            shader_link.logger.Logger.interrupted ()
        except RuntimeError as e:
            shader_link.logger.Logger.fatal (str (e))

    def run (self):
        try:
            cache = self.cache_storage.load ()

            for target in self.task.input_files:
                self.compiler.compile (self.config.forced, target, cache)

            self.cache_storage.dump (cache)

        except KeyboardInterrupt:
            shader_link.logger.Logger.interrupted ()
        except RuntimeError as e:
            shader_link.logger.Logger.fatal (str (e))
        else:
            shader_link.logger.Logger.done ()
