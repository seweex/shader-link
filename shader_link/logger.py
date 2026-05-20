
class Logger:
    _RED = '\033[91m'
    _GREEN = '\033[92m'
    _YELLOW = '\033[93m'
    _BLUE = '\033[96m'
    _PURPLE = '\033[95m'
    _RESET = '\033[0m'

    @staticmethod
    def skip (name : str):
        print (f'Skipped compiled {Logger._PURPLE}{name}{Logger._RESET}')

    @staticmethod
    def successful_compilation (file : str):
        print (f'Compiled {Logger._GREEN}{file}{Logger._RESET}')

    @staticmethod
    def failed_compilation (file : str, error : str):
        print (f'Failed to compile {Logger._RED}{file}{Logger._RESET}: {error}')

    @staticmethod
    def successful_export (file : str):
        print (f'Exported {Logger._GREEN}{file}{Logger._RESET}')

    @staticmethod
    def failed_export (file : str, error : str):
        print (f'Failed to export {Logger._RED}{file}{Logger._RESET}: {error}')

    @staticmethod
    def fatal (error : str):
        print (f'Fatal error: {Logger._RED}{error}{Logger._RESET}')

    @staticmethod
    def interrupted ():
        print (f'{Logger._YELLOW}Interrupted{Logger._RESET}')