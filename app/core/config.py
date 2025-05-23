from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "user"
    db_password: str = "password"
    db_name: str = "database"
    
class LocalSettings(Settings):
    db_file_name: str = "database.db"
    db_url: str = "sqlite:///./database.db"
    

    
    
    