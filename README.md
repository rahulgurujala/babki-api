# Denarii API

Denarii API is the official API for handling all backend interactions for the Denarii application both on web and mobile (coming soon).

## Getting Started
1. Clone the repository:
```
https://github.com/victor-ajayi/denarii-api.git
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Start up Docker container services. This application uses Docker containers for connecting the API to the database.
```
docker compose up --build
```

Alternatively, you can start up the app locally with this command. However, a local PostgreSQL database would need to be created.
```
uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload
```

## Usage
If the Docker containers were built successfully then the interactive Swagger documentation for the API would be available at `http://localhost:8000/`.

The application built with a PostgreSQL database. So the following environment variables would be needed to start up the Docker container for the database in order for the application to run correctly: `DB_USERNAME`, `DB_PASSWORD`, `DB_HOSTNAME`, `DB_PORT`, and `DB_NAME`.

`SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` variables also need to be set as the app relies on them for authentication and security purposes.


## Testing
Exhaustive tests for the API have been implemented with Pytest and can be run with the command:
```
pytest tests
```
Or if testing the started Docker service:
```
docker exec -it denarii-api pytest tests
```