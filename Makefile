requirements.txt: pyproject.toml
	uv pip compile -o requirements.txt pyproject.toml
	uv sync

lint:
	uvx ruff check --select I --fix

fmt:
	uvx ruff format
