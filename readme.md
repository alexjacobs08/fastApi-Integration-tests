This repo serves as an example for doing integration tests with fastAPI and pytest.

Checkout the accompanying post https://alex-jacobs.com/posts/fastapitests/

Contained is a toy fastAPI app with simple JWT auth and some endpoints to serve as good examples for making integration / API tests.
 
In `tests` thee are a number of examples using different patterns for integration testing fastAPI applications.


## Install
either use poetry or pip to install the dependencies
```bash
poetry install
```
or 
```bash
pip install -r requirements.txt
```

## Run Tests
```bash
pytest
```

## Run App
```bash
uvicorn app.main:app --reload
```

## Build Docker Image
```bash
docker build -t fastapi-integration-tests .
```

## Run Docker Image
```bash
docker compose up
```
or
```bash
docker run -p 8000:8000 fastapi-integration-tests
```
