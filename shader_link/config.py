
import argparse
import pathlib
import shutil

class Arguments:
    @staticmethod
    def _make_parser () -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-f", "--forced",
            required=False,
            default=False,
            help="forcedly recompile all files",
            action="store_true")

        parser.add_argument(
            "-i", "--input",
            required=True,
            help="input shader directory or file",
            type=str)

        parser.add_argument(
            "-o", "--output",
            required=False,
            default="./out/",
            help="output shader directory or file",
            type=str)

        return parser

    def _validate (self) -> None:
        if not self.input_path.exists () or not (self.input_path.is_dir() or self.input_path.is_file ()):
            raise FileNotFoundError ("Invalid input path")

        if self.output_path.exists () and not self.output_path.is_dir ():
            raise NotADirectoryError ("Output path must be a directory")

        try:
            self.output_path.mkdir (parents=True, exist_ok=True)
            test_file = self.output_path / ".write_test"
            test_file.touch ()
            test_file.unlink ()
        except OSError:
            raise PermissionError (f"No permission to write to output directory")

    def __init__ (self):
        parser = self._make_parser ()
        args = parser.parse_args ()

        self.input_path = pathlib.Path (args.input)
        self.output_path = pathlib.Path (args.output)
        self.forced = bool (args.forced)

        self._validate ()

class Compiler:
    @staticmethod
    def _find_glslc () -> pathlib.Path | None:
        path = shutil.which("glslc")

        if path:
            return pathlib.Path (path)
        else:
            return None

    def _validate (self) -> None:
        if self.compiler_path is None or not self.compiler_path.exists () or not self.compiler_path.is_file ():
            raise FileNotFoundError ("A shader compiler (glslc.exe) was not found."
                                     "Make sure you have it installed.")

    def __init__ (self):
        self.compiler_path = self._find_glslc ()
        self._validate ()

class Config:
    def _make_cache_path (self):
        return self.output_path / "cache.json"

    def __init__ (self, args : Arguments, compiler : Compiler):
        self.input_path = args.input_path
        self.output_path = args.output_path
        self.compiler_path = compiler.compiler_path

        self.forced = args.forced

        self.cache_path = self._make_cache_path ()