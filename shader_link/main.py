
import argparse

from pathlib import Path

from shader_link.logger import Logger
from shader_link.executor import Executor, FilesToCompile, Settings

def main():
    logger = Logger()

    try:
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-r", "--replace",
            required=False,
            default=False,
            help="replace existing output files",
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

        input_path = Path (str (args.input))
        output_path = Path (str (args.output))

        executor = Executor ()
        settings = Settings (args.replace)
        target = FilesToCompile (input_path, output_path)

        executor.compile (settings, target, logger)

    except KeyboardInterrupt:
        logger.report_interrupted()
    except Exception as error:
        logger.report_fatal (str(error))
    else:
        logger.report_done ()

if __name__ == "__main__":
    main()