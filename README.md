# HHRU Question Bot

## Run or stop stack from root

- `make serve` to run dev mode
- `make down` to stop

### Use local resources to watch project

- [api swagger docs](http://localhost:8000/docs/)
- [api redoc](http://localhost:8000/redoc/)
- [mongoDB admin panel](http://localhost:8081/)

### Test inside api or bot container

`pytest -v -s -x` for all tests

use `python -m IPython` to check code

## Links

- [about TG bots connectors](https://konstantinklepikov.github.io/myknowlegebase/notes/telegram-bots.html)
- [TG API](https://core.telegram.org/)
- [aiohttp](https://konstantinklepikov.github.io/myknowlegebase/notes/aiohttp.html)
- [mongo motor](https://konstantinklepikov.github.io/myknowlegebase/notes/mongomotor.html)
