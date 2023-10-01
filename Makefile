generate_readme:
	bash script/readme_gen.sh

lint:
	poetry run isort --check-only .
	poetry run black --check .

format:
	poetry run isort .
	poetry run black .