
import argparse

from pathlib import Path

from shader_link.logger import Logger
from shader_link.executor import Executor, FilesToCompile, Settings

def parse_args ():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r", "--replace",
        required=False,
        default=False,
        help="recompile forced with no skips",
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

    return parser.parse_args ()

def run_compilation (logger : Logger,
                     settings : Settings,
                     target : FilesToCompile):
    try:
        executor = Executor()
        executor.compile (settings, target, logger)
    except KeyboardInterrupt:
        logger.report_interrupted()
    except Exception as error:
        logger.report_fatal (str(error))
    else:
        logger.report_done ()

def main():
    logger = Logger ()

    try:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-r", "--replace",
            required=False,
            default=False,
            help="recompile forced with no skips",
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

        args = parser.parse_args()

        settings = Settings (args.replace)
        target = FilesToCompile (Path (args.input), Path (args.output))

        run_compilation (logger, settings, target)

    except KeyboardInterrupt:
        logger.report_interrupted()
    except Exception as error:
        logger.report_fatal (str(error))

if __name__ == "__main__":
    main()