def main():
    """
    Main entry point for the application.

    The application can be configured using environment variables:
    - HOST: The host to bind to (default: 127.0.0.1)
    - PORT: The port to listen on (default: 8000)

    Example:
    HOST=0.0.0.0 PORT=8080 python main.py
    """

    from app.app import WebApp

    app = WebApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye!")
    except Exception as e:
        print(f"Error: {e}")
