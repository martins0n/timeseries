import json
import os
import pathlib

import dotenv
import openai
import pandas as pd
import requests

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

FILE_FOLDER = pathlib.Path(__file__).parent.absolute()


def get_readme_summary(link: str, library: str):
    readme = requests.get(
        (link + f"/master/README.md").replace("github.com", "raw.githubusercontent.com")
    )

    if readme.status_code == 404:
        readme = requests.get(
            (link + f"/main/README.md").replace(
                "github.com", "raw.githubusercontent.com"
            )
        )
    readme_text = readme.text

    messages = [
        {
            "role": "system",
            "content": (
                "You are data sciense expert and your field is time series analysis. "
                "Make a summary of the readme file of library. "
                "And create bullet points about the library. "
                "You should write at least 3 bullet points. "
                "You should be quite brief and concise. "
            ),
        },
        {"role": "user", "content": readme_text},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0.3,
        max_tokens=1024 * 8,
    )

    generated_texts = [
        choice.message["content"].strip() for choice in response["choices"]
    ]
    return generated_texts[0]


def create_library_md():
    with open(FILE_FOLDER.parent / "data" / "library.json") as f:
        library = json.load(f)

    for lib in library:
        if "summary" in lib:
            continue
        print(lib["library"])
        lib["summary"] = get_readme_summary(lib["link"], library=lib["library"])

    library = sorted(library, key=lambda x: x["library"])

    with open(FILE_FOLDER.parent / "data" / "library.json", "w") as f:
        json.dump(library, f, indent=4, sort_keys=True)

    table = "| Library | Status | Summary | Tasks |\n"
    table += "|---------|--------|---------|-------|\n"  # Table delimiters for markdown

    # Add each row to the table
    for entry in library:
        library_link = f"[{entry['library']}]({entry['link']})"
        tasks = ", ".join(entry["tasks"])
        summary = entry["summary"].split("\n")
        summary = (
            "<ul>"
            + "".join([f'<li>{item.strip("-")}</li>' for item in summary])
            + "</ul>"
        )
        table += f"| {library_link} | {entry['status']} | {summary} | {tasks} |\n"

    return table


if __name__ == "__main__":
    print(create_library_md())
