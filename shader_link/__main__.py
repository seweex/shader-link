import shader_link.app
import shader_link.logger

def main ():
    try:
        config = shader_link.app.App.make_config ()
        app = shader_link.app.App (config)
        app.run()
    except KeyboardInterrupt:
        shader_link.logger.Logger.interrupted()
    except Exception as e:
        shader_link.logger.Logger.fatal (str(e))

if __name__ == "__main__":
    main ()