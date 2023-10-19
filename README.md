# HHRU Question Bot

## Run or stop stack from root

- `make serve` to run dev mode
- `make down` to stop

### Use local resources to watch project

- [api swagger docs](http://localhost:8001/docs/)
- [api redoc](http://localhost:8001/redoc/)
- [mongoDB admin panel](http://localhost:8082/)

### Develop with each service

1. Go to service folder, f.e. `cd data-api/app` and create VSCode project by `code .`
2. Install poery dependencies and add environment for python linting. Use `poetry config virtualenvs.in-project true` for creation of env folder inside project. Then `poetry init` (if pyproject.toml not exist) and `poetry install --with dev`.
3. Inside container use:

    - `pytest -v -s -x` for all tests
    - use `python -m IPython` to check code
    - `mypy --install-types`
    - `mypy app` and `flake8 app`

## Links

- [about TG bots connectors](https://konstantinklepikov.github.io/myknowlegebase/notes/telegram-bots.html)
- [TG API](https://core.telegram.org/)
- [hh.ru api](https://github.com/hhru/api)
- [aiohttp](https://konstantinklepikov.github.io/myknowlegebase/notes/aiohttp.html)
- [fastapi aiohttp example](https://github.com/raphaelauv/fastAPI-aiohttp-example/blob/master/src/fastAPI_aiohttp/fastAPI.py)
- [mongo motor](https://konstantinklepikov.github.io/myknowlegebase/notes/mongomotor.html)

## Scheme of services

![scheme](scheme.png "scheme")

## For using services define .env file with variables

You must use telegram and hh.ru official API accounts.

```sh
# mongo dev
DEV_ROOT_USERNAME=
DEV_ROOT_PASSWORD=
# mongo admin panel
ADMINUSERNAME=
ADMINPASSWORD=
MONGODB_URL=mongodb://${DEV_ROOT_USERNAME}:${DEV_ROOT_PASSWORD}@wzzzz-mongo-dev:27017/
DB_NAME=dev-db

TEST_ROOT_USERNAME=mongo-test
TEST_ROOT_PASSWORD=123456789
TEST_MONGODB_URL=mongodb://${TEST_ROOT_USERNAME}:${TEST_ROOT_PASSWORD}@wzzzz-mongo-test:27021/

# telegram api token
TG_API_TOKEN=

# hh.ru secrets
CLIENT_ID=
CLIENT_SECRET=
HHRU_API_TOKEN=
HHRU_CLIENT_EMAIL=

# redis
REDIS_URL=wzzzz-redis-dev
```

## Still oppened problems

- [72](https://github.com/KonstantinKlepikov/wzzzz/issues/72) rewrite query for db ids (get ids from chunk asynchronously) and rewrite cumbersome csv getter for bot
- [71](https://github.com/KonstantinKlepikov/wzzzz/issues/71) test all stack
- [70](https://github.com/KonstantinKlepikov/wzzzz/issues/70) switch redis to aiohttp pub/sub
- [39](https://github.com/KonstantinKlepikov/wzzzz/issues/39) add change template resource to api and bot
- [15](https://github.com/KonstantinKlepikov/wzzzz/issues/15) get vacancy by id
