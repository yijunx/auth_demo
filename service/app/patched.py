def get_patched_app():
    from app.app import app

    return app


app = get_patched_app()
