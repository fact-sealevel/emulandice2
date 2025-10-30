format:
	uv run ruff format src

lint:
	uv run ruff check --fix src

validate: format lint
