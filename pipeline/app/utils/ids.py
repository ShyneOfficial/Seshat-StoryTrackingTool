import re
import uuid


SESHAT_NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


def normalize_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"\s+", " ", name)
    return name


def make_entity_id(entity_type: str, name: str) -> str:
    normalized_name = normalize_name(name)
    raw_id = uuid.uuid5(SESHAT_NAMESPACE, f"{entity_type}:{normalized_name}")

    return f"{entity_type}_{raw_id.hex[:12]}"
