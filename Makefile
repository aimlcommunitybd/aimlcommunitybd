run:
	PYTHONPATH=src uv run python src/app/main.py

server:
	PYTHONPATH=src gunicorn -w 4 -b 0.0.0.0:10000 app.main:app

dev:
	PYTHONPATH=src uv run python scripts/setup.py

rm-db:
	rm -r database.db -f