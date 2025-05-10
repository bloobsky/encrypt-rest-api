from flask import Flask
from api.handlers.registration import registration_bp
from api.handlers.login import login_bp
from api.handlers.logout import logout_bp
from api.handlers.user import user_bp
from api.handlers.welcome import welcome_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(welcome_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(port=4000, debug=True)
