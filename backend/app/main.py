from dataclasses import asdict
from pprint import pprint

from app.modules.entities import CharacterModule, LocationModule
from app.modules.links import VisitModule
from app.pipeline.nlp import NLPPipeline


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def main() -> None:
    path = "data/input1.txt"
    text = load_text(path)
    pipeline = NLPPipeline()

    ############################################################
    ##### Entity modules MUST execute before link modules. #####
    ############################################################
    pipeline.add_module(CharacterModule())
    pipeline.add_module(LocationModule())

    pipeline.add_module(VisitModule())

    result = pipeline.run(text=text, chapter_id="chapter_001")

    pprint(asdict(result))


if __name__ == "__main__":
    main()
