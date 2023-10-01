echo "Generating README.md"

echo "# Timeseries" > README.md
echo "## Python libraries" >> README.md
poetry run python script/library.py >> README.md