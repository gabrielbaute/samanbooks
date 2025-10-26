from app.config import AppConfig
from app.app_factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=AppConfig.PORT)