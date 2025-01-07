# Configuration for the Flask application
class Config():
    # Base configuration settings

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids unnecessary overhead

class LocalDevelopmentConfig(Config):
    # Development-specific configuration settings
    SQLALCHEMY_DATABASE_URI = "sqlite:///householddb.sqlite3"  # Path to the SQLite database
    UPLOAD_FOLDER = "Backend/uploads"
    DEBUG = True  # Enables debug mode for easier troubleshooting
    SECURITY_PASSWORD_HASH = "bcrypt"  # Secure password hashing with bcrypt
    SECURITY_PASSWORD_SALT = "SAROHA@22#"  # Salt for password hashing
    SECRET_KEY = "VERYSECRETKEY"  # Secret key for session and CSRF protection
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    
    # cache specific
    # CACHE_TYPE =  "RedisCache"
    # CACHE_DEFAULT_TIMEOUT = 30
    # CACHE_REDIS_PORT = 6379
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://localhost:6379"  
    CACHE_DEFAULT_TIMEOUT = 500

    WTF_CSRF_ENABLED = False # Disable CSRF in dev environment (enable in production)