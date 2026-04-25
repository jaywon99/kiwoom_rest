import requests
from bs4 import BeautifulSoup
import json
import time
from deep_translator import GoogleTranslator
import re

translator = GoogleTranslator(source='ko', target='en')

def get_class_name(kor_name):
    eng_name = translator.translate(kor_name)
    eng_name = re.sub(r'[^a-zA-Z0-9\s]', ' ', eng_name)
    words = eng_name.split()
    return ''.join(word.capitalize() for word in words)

def process_table_rows(tbody, is_request):
    fields = []
    stack = [(-1, fields)]  # (level, list_to_append)
    
    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 6:
            raw_name = tds[0].text.strip()
            if not raw_name: continue
            if is_request and raw_name.lower() == "authorization": continue
            
            prefix_match = re.match(r'^([\-\s]+)', raw_name)
            if prefix_match:
                prefix = prefix_match.group(1)
                level = prefix.count('-')
                clean_name = raw_name[len(prefix):]
            else:
                level = 0
                clean_name = raw_name
                
            el_desc_kor = tds[1].text.strip()
            el_desc = tds[5].text.strip()
            
            item = {
                "key": clean_name,
                "desc": f"{el_desc_kor} {el_desc}".strip(),
                "default": "",
                "children": []
            }
            
            while stack and stack[-1][0] >= level:
                stack.pop()
                
            stack[-1][1].append(item)
            stack.append((level, item["children"]))
            
    return fields

base_url = "https://openapi.kiwoom.com"

print("Fetching main guide...")
resp = requests.get(f"{base_url}/guide/apiguide?dummyVal=0")
soup = BeautifulSoup(resp.text, 'html.parser')

groups = []

menus = soup.find_all('li', class_='guide-menu')
for menu in menus:
    a_tag = menu.find('a', class_='guide-menu-a')
    if not a_tag: continue
    
    group_name = a_tag.text.strip()
    sub_ul = menu.find('ul')
    if not sub_ul: continue
        
    sub_items = []
    for li in sub_ul.find_all('li'):
        sub_a = li.find('a')
        if sub_a:
            onclick = sub_a.get('onclick', '')
            if "apiGuideSelect" in onclick:
                parts = onclick.split("'")
                if len(parts) >= 4:
                    job_tp_code = parts[1]
                    sub_name = li.text.strip()
                    sub_items.append({"code": job_tp_code, "name": sub_name})
                    
    groups.append({"name": group_name, "categories": sub_items})

all_apis = []
seen_classes = set()

for group in groups:
    for cat in group['categories']:
        print(f"Fetching category: {group['name']} -> {cat['name']}")
        
        c_resp = requests.get(f"{base_url}/guide/apiGuideContents?jobTpCode={cat['code']}")
        c_soup = BeautifulSoup(c_resp.text, 'html.parser')
        
        api_links = c_soup.find_all('a')
        for link in api_links:
            onclick = link.get('onclick', '')
            if 'apiGuideTrIo' in onclick:
                parts = onclick.split("'")
                if len(parts) >= 5:
                    api_id = parts[1]
                    api_name = parts[3]
                    
                    cname = get_class_name(api_name)
                    original_cname = cname
                    counter = 1
                    while cname in seen_classes:
                        cname = f"{original_cname}{counter}"
                        counter += 1
                    seen_classes.add(cname)
                    class_name = cname
                    
                    print(f"  Fetching API: {api_name} ({api_id}) -> {class_name}")
                    
                    api_resp = requests.get(f"{base_url}/guide/apiGuideContents?jobTpCode={cat['code']}&apiId={api_id}")
                    api_soup = BeautifulSoup(api_resp.text, 'html.parser')
                    
                    method = "POST"
                    path = ""
                    
                    th_method = api_soup.find(lambda tag: tag.name == "th" and tag.text.strip() == "Method")
                    if th_method:
                        td_method = th_method.find_next_sibling("td")
                        if td_method:
                            method = td_method.text.strip()
                            
                    th_url = api_soup.find(lambda tag: tag.name == "th" and tag.text.strip() == "URL")
                    if th_url:
                        td_url = th_url.find_next_sibling("td")
                        if td_url:
                            path = td_url.text.strip()
                            
                    headers = []
                    params = []
                    res_headers = []
                    res_body = []
                    
                    section_state = None
                    
                    for tag in api_soup.find_all(['h3', 'table']):
                        if tag.name == 'h3':
                            text = tag.text.strip()
                            if text == '요청':
                                section_state = "request"
                            elif text == '응답':
                                section_state = "response"
                        
                        elif tag.name == 'table' and section_state:
                            cap = tag.find("caption")
                            if not cap: continue
                            cap_text = cap.text.strip()
                            
                            tbody = tag.find("tbody")
                            if not tbody: continue
                            
                            parsed_fields = process_table_rows(tbody, is_request=(section_state=="request"))
                            
                            if section_state == "request":
                                if "Header" in cap_text:
                                    headers.extend(parsed_fields)
                                elif "Body" in cap_text or "Parameter" in cap_text:
                                    params.extend(parsed_fields)
                            elif section_state == "response":
                                if "Header" in cap_text:
                                    res_headers.extend(parsed_fields)
                                elif "Body" in cap_text or "Parameter" in cap_text:
                                    res_body.extend(parsed_fields)
                                            
                    all_apis.append({
                        "group": group["name"],
                        "category": cat["name"],
                        "id": api_id,
                        "name": api_name,
                        "class_name": class_name,
                        "method": method,
                        "path": path,
                        "headers": headers,
                        "params": params,
                        "res_headers": res_headers,
                        "res_body": res_body
                    })
                    
        time.sleep(0.1)

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "../kiwoom/apis.json")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(all_apis, f, ensure_ascii=False, indent=2)

print("Saved to kiwoom/apis.json with nested response models included.")
