import os
import json
from notion_client import Client

notion = Client(auth=os.environ["NOTION_API_KEY"])
database_id = os.environ["NOTION_DB_ID"]

results = notion.databases.query(database_id=database_id)["results"]

def parse_property(prop):
    prop_type = prop["type"]
    value = prop.get(prop_type)

    if prop_type == "title" and value:
        return value[0]["plain_text"] if value else ""
    elif prop_type == "rich_text" and value:
        return value[0]["plain_text"] if value else ""
    elif prop_type == "number":
        return value
    elif prop_type == "select":
        return value["name"] if value else ""
    elif prop_type == "multi_select":
        return [v["name"] for v in value] if value else []
    elif prop_type == "date":
        return value["start"] if value else ""
    elif prop_type == "checkbox":
        return value
    elif prop_type == "people":
        return [person["name"] for person in value] if value else []
    else:
        return str(value)  # fallback 처리

parsed = []
for row in results:
    props = row["properties"]
    row_data = {}

    for key, value in props.items():
        row_data[key] = parse_property(value)

    parsed.append(row_data)

with open("public/data.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, ensure_ascii=False, indent=2)
