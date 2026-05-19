import shader_link.app
import shader_link.logger

def main ():
    try:
        app = shader_link.app.App()
        app.run()
    except KeyboardInterrupt:
        shader_link.logger.Logger.interrupted()
    except Exception as e:
        shader_link.logger.Logger.fatal (str(e))

if __name__ == "__main__":
    main ()