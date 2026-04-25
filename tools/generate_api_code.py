import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APIS_JSON_PATH = os.path.join(SCRIPT_DIR, '../kiwoom/apis.json')
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '../kiwoom/typed_api.py')

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].title() + ''.join(x.title() for x in components[1:])

def clean_api_key(key):
    real_key = re.sub(r'^[\-\s]+', '', key)
    py_key = real_key.replace('-', '_')
    py_key = re.sub(r'[^a-zA-Z0-9_]', '', py_key)
    if re.match(r'^[0-9]', py_key):
        py_key = "n_" + py_key
    return real_key, py_key

with open(APIS_JSON_PATH, 'r', encoding='utf-8') as f:
    apis = json.load(f)

out = [
    "from pydantic import BaseModel, Field, ConfigDict", 
    "from typing import Optional, Dict, Any, List, Type", 
    "from .client import KiwoomClient",
    "",
    "# ====================================================================",
    "# 1. API Models (입력 및 출력 모델)",
    "# ====================================================================",
    ""
]

def generate_sub_models(api, items, parent_class_name):
    # 재귀적으로 children이 있는 항목들의 SubModel 클래스를 생성하고 선언 코드를 반환합니다.
    sub_model_classes = []
    field_declarations = []
    seen_keys = set()
    
    for item in items:
        real_key, py_key = clean_api_key(item['key'])
        if py_key in seen_keys: continue
        seen_keys.add(py_key)
        
        desc = item['desc'].replace('\r', ' ').replace('\n', ' ').replace('"', "'")
        alias_str = f', alias="{real_key}"' if real_key != py_key else ""
        
        if item.get('children'):
            sub_class_name = f"{parent_class_name}_{to_camel_case(py_key)}"
            sub_sub_classes, sub_fields = generate_sub_models(api, item['children'], sub_class_name)
            sub_model_classes.extend(sub_sub_classes)
            
            sub_model_classes.append(f"class {sub_class_name}(BaseModel):")
            sub_model_classes.append(f'    model_config = ConfigDict(populate_by_name=True)')
            if not sub_fields:
                sub_model_classes.append("    pass")
            else:
                sub_model_classes.extend(sub_fields)
            sub_model_classes.append("")
            
            field_declarations.append(f'    {py_key}: Optional[List[{sub_class_name}]] = Field(default=None{alias_str}, description="{desc}")')
        else:
            field_declarations.append(f'    {py_key}: Optional[Any] = Field(default=None{alias_str}, description="{desc}")')
            
    return sub_model_classes, field_declarations

for api in apis:
    req_class_name = f"{api['class_name']}Request"
    res_class_name = f"{api['class_name']}Response"
    
    # ---------------- REQUEST MODEL ----------------
    req_sub_classes, req_fields = generate_sub_models(api, api.get('headers', []) + api.get('params', []), req_class_name)
    out.extend(req_sub_classes)
    
    out.append(f"class {req_class_name}(BaseModel):")
    out.append(f'    """[{api["id"]}] {api["name"]} 요청 모델"""')
    out.append('    model_config = ConfigDict(populate_by_name=True)')
    
    if not req_fields:
        out.append("    pass")
    else:
        # Request에는 api_id 필터링 적용
        filtered_req_fields = [f for f in req_fields if not re.search(r'^\s*api_id:', f, re.IGNORECASE)]
        if not filtered_req_fields:
            out.append("    pass")
        else:
            out.extend(filtered_req_fields)
    out.append("")

    # ---------------- RESPONSE MODEL ----------------
    res_sub_classes, res_fields = generate_sub_models(api, api.get('res_headers', []) + api.get('res_body', []), res_class_name)
    out.extend(res_sub_classes)
    
    out.append(f"class {res_class_name}(BaseModel):")
    out.append(f'    """[{api["id"]}] {api["name"]} 응답 모델"""')
    out.append('    model_config = ConfigDict(populate_by_name=True)')
    
    if not res_fields:
        out.append("    pass")
    else:
        filtered_res_fields = [f for f in res_fields if not re.search(r'^\s*api_id:', f, re.IGNORECASE)]
        if not filtered_res_fields:
            out.append("    pass")
        else:
            out.extend(filtered_res_fields)
    out.append("")

out.extend([
    "# ====================================================================",
    "# 2. Typed API Client (타입이 보장되는 클라이언트)",
    "# ====================================================================",
    "",
    "class KiwoomTypedClient:",
    '    """',
    '    kwargs 대신 명시적인 Pydantic 모델을 사용하여 API를 호출하는 안전한 클라이언트입니다.',
    '    요청 및 응답 모두 Type Hinting이 적용된 객체를 사용합니다.',
    '    """',
    "    def __init__(self, client: KiwoomClient):",
    "        self.client = client",
    ""
])

for api in apis:
    req_class_name = f"{api['class_name']}Request"
    res_class_name = f"{api['class_name']}Response"
    method_name = to_snake_case(api['class_name'])
    
    if method_name in ["import", "class", "def", "pass", "return", "yield"]:
        method_name += "_api"
        
    out.append(f"    def {method_name}(self, req: {req_class_name}) -> {res_class_name}:")
    out.append(f'        """[{api["id"]}] {api["name"]} ({api["group"]} - {api["category"]})"""')
    out.append(f'        raw_response = self.client.call("{api["id"]}", **req.model_dump(by_alias=True, exclude_none=True))')
    out.append(f'        return {res_class_name}(**raw_response)')
    out.append("")


out.extend([
    "# ====================================================================",
    "# 3. Registry (동적 호출을 위한 매핑)",
    "# ====================================================================",
    "",
    "API_ID_TO_METHOD: Dict[str, str] = {",
])
for api in apis:
    method_name = to_snake_case(api['class_name'])
    if method_name in ["import", "class", "def", "pass", "return", "yield"]:
        method_name += "_api"
    out.append(f'    "{api["id"]}": "{method_name}",')
out.append("}")
out.append("")

out.append("API_ID_TO_REQ_MODEL: Dict[str, Type[BaseModel]] = {")
for api in apis:
    req_class_name = f"{api['class_name']}Request"
    out.append(f'    "{api["id"]}": {req_class_name},')
out.append("}")
out.append("")

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("✅ kiwoom/typed_api.py generated with Request AND Response models!")
