
import hashlib
import subprocess
import shutil

import pathlib

import shader_link.config
import shader_link.cache
import shader_link.logger

class Task:
    @staticmethod
    def _group_file_info (
            file_path : pathlib.Path,
            out_path : pathlib.Path,
            export_path : pathlib.Path | None) -> dict:
        return {
            "input_path": str (file_path.absolute ()),
            "output_path": str ((out_path / (file_path.name + '.spv')).absolute ()),
            "export_path": str ((export_path / (file_path.name + '.hpp')).absolute ()) if export_path else None,
            "name": file_path.name
        }

    @staticmethod
    def _group_input_files (
            input_path : pathlib.Path,
            output_path : pathlib.Path,
            export_path : pathlib.Path | None) -> list[dict]:

        if input_path.is_file ():
            return [Task._group_file_info (input_path, output_path, export_path)]
        else:
            return [Task._group_file_info (file, output_path, export_path) for file in input_path.iterdir ()]

    def __init__ (self, config : shader_link.config.Config) -> None:
        self.input_files = self._group_input_files (config.input_path, config.temp_output_path, config.temp_export_path)
        self.forced = config.forced
        self.export = config.temp_export_path is not None

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

    def compile (self, forced : bool, info : dict, cache : shader_link.cache.Cache) -> bool:
        checksum = None

        if not forced:
            checksum = self.calc_checksum (info ['input_path'])

            if cache.is_actual (info ['name'], checksum):
                shader_link.logger.Logger.skip (info ['name'])
                return False

        command = self._form_command (info)
        result = self._submit_compilation (command)

        if checksum is not None:
            cache.update (info['name'], checksum)

        if result.returncode == 0:
            shader_link.logger.Logger.successful_compilation (info['name'])
        else:
            shader_link.logger.Logger.failed_compilation (info['name'], result.stderr)

        return True

class Deployer:
    @staticmethod
    def _deploy_files (src_path : pathlib.Path, dst_path : pathlib.Path) -> None:
        dst_path.mkdir (parents=True, exist_ok=True)

        for item in src_path.iterdir ():
            if item.is_file():
                shutil.copy2(item, dst_path / item.name)

    def __init__ (self, config : shader_link.config.Config) -> None:
        self.temp_output_path = config.temp_output_path
        self.temp_export_path = config.temp_export_path

        self.target_output_path = config.target_output_path
        self.target_export_path = config.target_export_path

        self.copy_export = config.temp_export_path is not None

    def deploy (self):
        self._deploy_files (self.temp_output_path, self.target_output_path)

        if self.copy_export:
            self._deploy_files (self.temp_export_path, self.target_export_path)

    def delete_temps (self):
        shutil.rmtree (self.temp_output_path)

        if self.copy_export:
            shutil.rmtree (self.temp_export_path)