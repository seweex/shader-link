
import argparse

from pathlib import Path

from shader_link.logger import Logger
from shader_link.executor import Executor, FilesToCompile

def main():
    logger = Logger()

    try:
        parser = argparse.ArgumentParser()

        parser.add_argument("-i", "--input", required=True, help="input shader directory or file")
        parser.add_argument("-o", "--output", required=False, help="output shader directory or file", default="./out/")

        args = parser.parse_args()

        input_path = Path (str (args.input))
        output_path = Path (str (args.output))

        executor = Executor ()
        target = FilesToCompile (input_path, output_path)

        executor.compile (target, logger)
    except KeyboardInterrupt:
        logger.report_interrupted()
    except Exception as error:
        logger.report_fatal (str(error))
    else:
        logger.report_done ()

if __name__ == "__main__":
    main()