
import hashlib
import subprocess

import pathlib

import shader_link.config
import shader_link.cache
import shader_link.logger

class Task:
    @staticmethod
    def _group_file_info (file_path : pathlib.Path, out_path : pathlib.Path) -> dict:
        return {
            "input_path": str (file_path.absolute ()),
            "output_path": str ((out_path / (file_path.name + '.spv')).absolute ()),
            "name": file_path.stem
        }

    @staticmethod
    def _group_input_files (input_path : pathlib.Path, output_path : pathlib.Path) -> list[dict]:
        if input_path.is_file ():
            return [Task._group_file_info (input_path, output_path)]
        else:
            return [Task._group_file_info (file, output_path) for file in input_path.iterdir ()]

    def __init__ (self, config : shader_link.config.Config) -> None:
        self.input_files = self._group_input_files (config.input_path, config.output_path)
        self.forced = config.forced

class Compiler:
    @staticmethod
    def calc_checksum (file_path : str) -> str:
        with open (file_path, 'rb') as file:
            return hashlib.sha256 (file.read ()).hexdigest()

    @staticmethod
    def _submit_compilation (command: list):
        return subprocess.run (command, capture_output=True, text=True)

    def _form_command (self, info : dict) -> list:
        return [self.compiler_path, info ['input_path'], '-o', info ['output_path']]

    def __init__ (self, config : shader_link.config.Config) -> None:
        self.compiler_path = str (config.compiler_path.absolute ())

    def compile (self, forced : bool, info : dict, cache : shader_link.cache.Cache) -> None:
        checksum = None

        if not forced:
            checksum = self.calc_checksum (info ['input_path'])

            if cache.is_actual (info ['name'], checksum):
                shader_link.logger.Logger.skip (info ['name'])
                return None

        command = self._form_command (info)
        result = self._submit_compilation (command)

        if checksum is not None:
            cache.update (info['name'], checksum)

        if result.returncode == 0:
            shader_link.logger.Logger.successful (info['name'])
        else:
            shader_link.logger.Logger.failed (info['name'], result.stderr)

        return None