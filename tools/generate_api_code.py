import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APIS_JSON_PATH = os.path.join(SCRIPT_DIR, '../kiwoom_rest/apis.json')
OUTPUT_PATH = os.path.join(SCRIPT_DIR, '../kiwoom_rest/generated.py')

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

def clean_base_name(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    words = snake.split('_')
    
    stopwords = {
        'request', 'for', 'of', 'inquiry', 'status', 
        'and', 'or', 'to', 'view', 'the', 'on', 'in', 'at', 'a', 'an', 's'
    }
    filtered_words = [w for w in words if w not in stopwords and w]
    
    if not filtered_words:
        return "Api"
        
    cleaned = ''.join(w.capitalize() for w in filtered_words)
    
    cleaned = cleaned.replace("EachAccount", "ByAccount")
    
    overrides = {
        "AccessTokenIssuance": "IssueAccessToken",
        "DiscardAccessToken": "RevokeAccessToken",
        "DetailsOrderDetailsByAccount": "OrderDetailsByAccount",
    }
    return overrides.get(cleaned, cleaned)

with open(APIS_JSON_PATH, 'r', encoding='utf-8') as f:
    apis = json.load(f)

# ====================================================================
# [MANUAL PATCHES] 
# 공식 문서의 누락/오류를 보정하기 위한 고정 패치 구간입니다.
# ====================================================================
for api in apis:
    # ka10080 (주식분봉차트조회): 응답에 acc_trde_qty 누락 보정
    if api.get("id") == "ka10080":
        for item in api.get("res_body", []):
            if item.get("key") == "stk_min_pole_chart_qry":
                has_acc_trde_qty = any(child.get("key") == "acc_trde_qty" for child in item.get("children", []))
                if not has_acc_trde_qty:
                    item["children"].append({
                        "key": "acc_trde_qty",
                        "type": "String",
                        "desc": "누적거래량 (공식문서 누락 수동 패치)",
                        "default": "",
                        "children": []
                    })
# ====================================================================

out = [
    "from pydantic import BaseModel, Field, ConfigDict, BeforeValidator", 
    "from typing import Optional, Dict, Any, List, Type, Annotated, Callable, Union", 
    "from .core import KiwoomCore",
    "",
    "# ====================================================================",
    "# 0. Type Validators (키움증권 예외 타입 처리기)",
    "# ====================================================================",
    "def _force_str(v: Any) -> str:",
    "    if v == [] or v is None:",
    '        return ""',
    "    if isinstance(v, list):",
    '        return ",".join(str(x) for x in v)',
    "    return str(v)",
    "",
    "def _force_list(v: Any) -> Any:",
    '    if v == "" or v is None:',
    "        return []",
    "    if not isinstance(v, list):",
    "        return [v]",
    "    return v",
    "",
    "def _force_int(v: Any) -> int:",
    '    if v == "" or v is None:',
    "        return 0",
    "    try:",
    "        return int(v)",
    "    except ValueError:",
    "        return 0",
    "",
    "SafeStr = Annotated[str, BeforeValidator(_force_str)]",
    "SafeInt = Annotated[int, BeforeValidator(_force_int)]",
    "SafeListStr = Annotated[List[str], BeforeValidator(_force_list)]",
    "",
    "# ====================================================================",
    "# 1. API Models (입력 및 출력 모델)",
    "# ====================================================================",
    ""
]

def generate_sub_models(api, items, parent_class_name):
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
            
            field_declarations.append(f'    {py_key}: Annotated[List[{sub_class_name}], BeforeValidator(_force_list)] = Field(default_factory=list{alias_str}, description="{desc}")')
        else:
            ktype = item.get("type", "").replace(" ", "")
            if ktype == "String[]":
                field_declarations.append(f'    {py_key}: SafeListStr = Field(default_factory=list{alias_str}, description="{desc}")')
            elif ktype == "int":
                field_declarations.append(f'    {py_key}: SafeInt = Field(default=0{alias_str}, description="{desc}")')
            else:
                field_declarations.append(f'    {py_key}: SafeStr = Field(default=""{alias_str}, description="{desc}")')
            
    return sub_model_classes, field_declarations

for api in apis:
    base_name = clean_base_name(api['class_name'])
    req_class_name = f"{base_name}Request"
    # Response라는 단어를 없애고, 순수 데이터 모델 객체명으로 승격
    res_class_name = base_name
    
    # ---------------- REQUEST MODEL ----------------
    req_sub_classes, req_fields = generate_sub_models(api, api.get('headers', []) + api.get('params', []), req_class_name)
    out.extend(req_sub_classes)
    
    out.append(f"class {req_class_name}(BaseModel):")
    out.append(f'    """[{api["id"]}] {api["name"]} 요청 모델 (내부 검증 및 Playground UI 용)"""')
    out.append('    model_config = ConfigDict(populate_by_name=True)')
    
    if not req_fields:
        out.append("    pass")
    else:
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
    out.append(f'    """[{api["id"]}] {api["name"]} 응답 데이터 모델"""')
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
    "# 2. Generated API Client (자동 생성된 중수준 레이어)",
    "# ====================================================================",
    "",
    "class KiwoomGeneratedClient:",
    '    """',
    '    명시적 파라미터(Named Arguments)를 통해 IDE 자동완성을 완벽하게 지원하는 중수준 클라이언트입니다.',
    '    입력값은 자동으로 Pydantic 내부 검증을 거치며, 응답은 타입이 보장된 객체(BaseModel)로 반환됩니다.',
    '    """',
    "    def __init__(self, core: KiwoomCore):",
    "        self.core = core",
    "",
    "    async def connect_ws(self, on_message: Callable[[Dict[str, Any]], Any]):",
    "        await self.core.connect_ws(on_message)",
    "",
    "    async def disconnect_ws(self):",
    "        await self.core.disconnect_ws()",
    ""
])

for api in apis:
    base_name = clean_base_name(api['class_name'])
    req_class_name = f"{base_name}Request"
    res_class_name = base_name
    method_name = to_snake_case(base_name)
    
    if method_name in ["import", "class", "def", "pass", "return", "yield"]:
        method_name += "_api"
        
    # 메서드 파라미터 조립
    items = api.get('headers', []) + api.get('params', [])
    sig_params = []
    call_kwargs = []
    
    seen_keys = set()
    for item in items:
        real_key, py_key = clean_api_key(item['key'])
        if py_key in seen_keys: continue
        seen_keys.add(py_key)
        if py_key.lower() == "api_id": continue
        
        ktype = item.get("type", "").replace(" ", "")
        if ktype == "String[]":
            py_type = "List[str]"
            default_val = "None"
        elif ktype == "int":
            py_type = "int"
            default_val = "0"
        else:
            py_type = "str"
            default_val = '""'
            
        sig_params.append(f"{py_key}: {py_type} = {default_val}")
        call_kwargs.append(f"{py_key}={py_key}")

    sig_str = ", ".join(sig_params)
    if sig_str:
        sig_str = ", " + sig_str
        
    kwargs_str = ", ".join(call_kwargs)
    
    if api.get("path") == "/api/dostk/websocket":
        out.append(f"    async def {method_name}(self{sig_str}):")
        out.append(f'        """')
        out.append(f'        [{api["id"]}] {api["name"]}')
        out.append(f'        분류: {api["group"]} - {api["category"]}')
        out.append(f'        """')
        out.append(f'        req = {req_class_name}({kwargs_str})')
        out.append(f'        await self.core.send_ws(req.model_dump(by_alias=True, exclude_none=True))')
        out.append("")
    else:
        out.append(f"    def {method_name}(self{sig_str}) -> {res_class_name}:")
        out.append(f'        """')
        out.append(f'        [{api["id"]}] {api["name"]}')
        out.append(f'        분류: {api["group"]} - {api["category"]}')
        out.append(f'        """')
        out.append(f'        req = {req_class_name}({kwargs_str})')
        out.append(f'        raw_response = self.core.call("{api["id"]}", **req.model_dump(by_alias=True, exclude_none=True))')
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
    base_name = clean_base_name(api['class_name'])
    method_name = to_snake_case(base_name)
    if method_name in ["import", "class", "def", "pass", "return", "yield"]:
        method_name += "_api"
    out.append(f'    "{api["id"]}": "{method_name}",')
out.append("}")
out.append("")

out.append("API_ID_TO_REQ_MODEL: Dict[str, Type[BaseModel]] = {")
for api in apis:
    base_name = clean_base_name(api['class_name'])
    out.append(f'    "{api["id"]}": {base_name}Request,')
out.append("}")
out.append("")

out.append("API_ID_TO_RES_MODEL: Dict[str, Type[BaseModel]] = {")
for api in apis:
    base_name = clean_base_name(api['class_name'])
    out.append(f'    "{api["id"]}": {base_name},')
out.append("}")
out.append("")

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print("✅ kiwoom_rest/generated.py generated successfully with Name Cleaning & Parameter Unpacking!")
