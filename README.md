
# Conduit fastapi implementation

Medium.com clone backend built using FastApi

## Reference

Created using this api specs:
- [Endpoints](https://realworld-docs.netlify.app/specifications/backend/endpoints/)
- [Responses](https://realworld-docs.netlify.app/specifications/backend/api-response-format/)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DB_USERNAME`

`DB_PASSWORD`

`DB_URL`

`DB_NAME`

`SECRET_KEY`


## Setup

Install dependencies with pip

```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```

Run
```bash
  python main.py
```

Or using uvicorn
```bash
  uvicorn main:app
```
## Running Tests

To run tests, run the following command

```bash
  APIURL={your api url} tests/api/run-api-tests.sh
```
