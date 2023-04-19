# HHRU Question Bot

## Run or stop stack from root

- `make serve` to run dev mode
- `make down` to stop

### Use local resources to watch project

- [api swagger docs](http://localhost:8001/docs/)
- [api redoc](http://localhost:8001/redoc/)
- [mongoDB admin panel](http://localhost:8082/)
- [flower](http://localhost:5556/)

### Test inside api or bot container

`pytest -v -s -x` for all tests

use `python -m IPython` to check code

`mypy --install-types`

`mypy app` and `flake8 app` inside container

## Links

- [about TG bots connectors](https://konstantinklepikov.github.io/myknowlegebase/notes/telegram-bots.html)
- [TG API](https://core.telegram.org/)
- [hh.ru api](https://github.com/hhru/api)
- [aiohttp](https://konstantinklepikov.github.io/myknowlegebase/notes/aiohttp.html)
- [fastapi aiohttp example](https://github.com/raphaelauv/fastAPI-aiohttp-example/blob/master/src/fastAPI_aiohttp/fastAPI.py)
- [mongo motor](https://konstantinklepikov.github.io/myknowlegebase/notes/mongomotor.html)
