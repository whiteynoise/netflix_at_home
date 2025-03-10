import sentry_sdk
from constants import SENTRY_DSN
from core.film import film_bp
from core.user import user_bp
from flask import Flask
from flask_marshmallow import Marshmallow
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FlaskIntegration()])

app = Flask(__name__)
app.register_blueprint(film_bp)
app.register_blueprint(user_bp)
ma = Marshmallow(app)


@app.route("/ping")
def health():
    return "Pong", 200


if __name__ == "__main__":
    app.run()
