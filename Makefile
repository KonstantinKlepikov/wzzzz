# target: all - Default target. Does nothing.
all:
	echo "Hello, this is make for jewelry-recomender"
	echo "Try 'make help' and search available options"

# target: help - List of options
help:
	egrep "^# target:" [Mm]akefile

# target: dev - run docker-compose
serve:
	sh ./scripts/dev.sh

# target: down - stop and down docker stack
down:
	docker compose -f docker-stack.yml down
