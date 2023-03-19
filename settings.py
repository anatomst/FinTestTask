from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE: str
    DB_USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env"

    def get_database_url(self) -> str:
        return (
            f"{self.DATABASE}://"
            f"{self.DB_USER}:"
            f"{self.PASSWORD}@"
            f"{self.HOST}:"
            f"{self.PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()
