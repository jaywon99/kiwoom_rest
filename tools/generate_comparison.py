import json
import sys
import os

# Add tools dir to path so we can import generate_api_code
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_api_code import clean_base_name as clean_base_name_new, to_snake_case
import re


def clean_base_name_old(name: str) -> str:
    name = re.sub(r"RequestFor|Request|Inquiry|For|Of|Status|Details", "", name, flags=re.IGNORECASE)
    name = re.sub(r"And|Or", "", name)
    return name or "Api"


with open("../kiwoom_rest/apis.json", "r", encoding="utf-8") as f:
    apis = json.load(f)

with open("../api_names_comparison.md", "w", encoding="utf-8") as out:
    out.write("| 한글 이름 | As-Is (이전 이름) | To-Be (개선된 이름) |\n")
    out.write("| :--- | :--- | :--- |\n")
    for api in apis:
        kor_name = api.get("name", "")
        original_class = api.get("class_name", "")

        old_cleaned = clean_base_name_old(original_class)
        as_is = to_snake_case(old_cleaned)

        new_cleaned = clean_base_name_new(original_class)
        to_be = to_snake_case(new_cleaned)

        if as_is != to_be:
            out.write(f"| {kor_name} | `❌ {as_is}` | **`✅ {to_be}`** |\n")
        else:
            out.write(f"| {kor_name} | `{as_is}` | `{to_be}` |\n")

print("File generated at api_names_comparison.md")
