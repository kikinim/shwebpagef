# 📄 scripts/update_data.py
import os
import json
from notion_client import Client

notion = Client(auth=os.environ["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"])
database_id = os.environ["206697d446ea8090a9dfd66d97a8c797"]

results = notion.databases.query(database_id=database_id)["results"]

parsed = []
for row in results:
    props = row["properties"]
    name = props["Name"]["title"][0]["plain_text"] if props["Name"]["title"] else ""
    score = props["점수"]["number"]
    parsed.append({"name": name, "score": score})

with open("public/data.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, ensure_ascii=False, indent=2)
