"""
DNS Central - Multi-Provider Domain Management
"""

import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-key-change-me")
    
    # Config
    app.config["NETCUP_CUSTOMER_ID"] = os.getenv("NETCUP_CUSTOMER_ID")
    app.config["NETCUP_API_KEY"] = os.getenv("NETCUP_API_KEY")
    app.config["NETCUP_API_PASSWORD"] = os.getenv("NETCUP_API_PASSWORD")
    app.config["NETCUP_DOMAINS"] = os.getenv("NETCUP_DOMAINS", "")
    app.config["SERVERS"] = os.getenv("SERVERS", "{}")
    
    # Routes registrieren
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app
