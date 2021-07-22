run:
	poetry run geese-bot

lint:
	poetry run flake8 bot

test:
	poetry run mypy bot
	poetry run pytest

coverage:
	poetry run coverage run -m pytest
	poetry run coverage xml

install:
	poetry build
	pip3 install --force-reinstall dist/Geeses_s_telegram_bot-0.1.0-py3-none-any.whl