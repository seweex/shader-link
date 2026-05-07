
import shutil
import subprocess

from pathlib import Path
from shader_link.logger import Logger

class FilesToCompile:
    def __init__(self, in_path : Path, out_path : Path) -> None:
        in_files = None
        out_dir = None

        if in_path.is_dir ():
            in_files = [str(file.absolute()).replace ('\\', '/') for file in in_path.iterdir ()]
        elif in_path.is_file ():
            in_files = [str(in_path.absolute()).replace ('\\', '/')]
        else:
            raise ValueError ("Input path must be a directory or a path to a single file")

        if not out_path.exists ():
            out_path.mkdir ()

        out_dir = str (out_path.absolute()).replace ('\\', '/')

        self.in_files = in_files
        self.out_dir = out_dir

class Executor:
    def __init__(self):
        path = shutil.which("glslc")

        if not path:
            raise FileNotFoundError("A shader compiler executable (glslc.exe) was not found."
                                    "Make sure you have it installed.")

        self.compiler_path = path

    def compile (self, target : FilesToCompile, logger : Logger) -> None:
        for file in target.in_files:
            name = file.replace ('\\', '/').split ('/') [-1]
            out = f'{target.out_dir}/{name}.bin'

            if Path(out).exists():
                logger.report_failed_compilation(name, 'File already exists')
                continue

            command = [self.compiler_path, file, '-o', out]
            proc = subprocess.run (command, capture_output=True, text=True)

            if proc.returncode == 0:
                logger.report_successful_compilation (name)
            else:
                logger.report_failed_compilation (name, proc.stderr)