import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Application settings
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Database connection settings
    SQL_CONNECTION_STRING = os.getenv('SQL_CONNECTION_STRING')

    # Flask app settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
