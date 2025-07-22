install:
	uv sync

dev:
	uv run --with .venv python3 -m flask --app page_analyzer.app run --debug --host 0.0.0.0 --port 5000

PORT ?=8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run ruff check .

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
