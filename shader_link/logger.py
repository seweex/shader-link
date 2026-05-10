
import os

class Logger:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[96m'
    RESET = '\033[0m'

    def __init__(self):
        os.system('')

    def report_skip (self, name : str):
        print (f'Skipped compiled {self.BLUE}{name}{self.RESET}')

    def report_successful_compilation (self, file : str):
        print (f'Successfully compiled {self.GREEN}{file}{self.RESET}')

    def report_failed_compilation (self, file : str, error : str):
        print (f'Failed to compile {self.RED}{file}{self.RESET}: {error}')

    def report_done (self):
        print (f'{self.GREEN}[!] Compilation done{self.RESET}')

    def report_fatal (self, error : str):
        print (f'Fatal error: {self.RED}{error}{self.RESET}')

    def report_interrupted (self):
        print ('Interrupted')