from dataclasses import asdict
from pprint import pprint

from app.pipeline.factory import create_nlp_pipeline


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def main() -> None:
    path = "data/input1.txt"
    text = load_text(path)
    pipeline = create_nlp_pipeline()

    result = pipeline.run(text=text, chapter_id="chapter_001")

    pprint(asdict(result))


if __name__ == "__main__":
    main()
