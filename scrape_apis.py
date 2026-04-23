import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://openapi.kiwoom.com"

print("Fetching main guide...")
resp = requests.get(f"{base_url}/guide/apiguide?dummyVal=0")
soup = BeautifulSoup(resp.text, 'html.parser')

groups = []

menus = soup.find_all('li', class_='guide-menu')
for menu in menus:
    a_tag = menu.find('a', class_='guide-menu-a')
    if not a_tag:
        continue
    
    group_name = a_tag.text.strip()
    
    sub_ul = menu.find('ul')
    if not sub_ul:
        continue
        
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
                    
                    print(f"  Fetching API: {api_name} ({api_id})")
                    
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
                    
                    is_request_section = False
                    
                    for tag in api_soup.find_all(['h3', 'table']):
                        if tag.name == 'h3':
                            text = tag.text.strip()
                            if text == '요청':
                                is_request_section = True
                            elif text == '응답':
                                is_request_section = False
                        
                        elif tag.name == 'table' and is_request_section:
                            cap = tag.find("caption")
                            if not cap: continue
                            cap_text = cap.text.strip()
                            
                            tbody = tag.find("tbody")
                            if not tbody: continue
                            
                            for tr in tbody.find_all("tr"):
                                tds = tr.find_all("td")
                                if len(tds) >= 6:
                                    el_name = tds[0].text.strip()
                                    el_desc_kor = tds[1].text.strip()
                                    el_desc = tds[5].text.strip()
                                    
                                    item = {
                                        "key": el_name,
                                        "desc": f"{el_desc_kor} {el_desc}".strip(),
                                        "default": ""
                                    }
                                    
                                    if "Header" in cap_text:
                                        if el_name.lower() != "authorization":
                                            headers.append(item)
                                    elif "Body" in cap_text:
                                        params.append(item)
                                    
                    all_apis.append({
                        "group": group["name"],
                        "category": cat["name"],
                        "id": api_id,
                        "name": api_name,
                        "method": method,
                        "path": path,
                        "headers": headers,
                        "params": params
                    })
                    
        time.sleep(0.1)

with open("static/apis.json", "w", encoding="utf-8") as f:
    json.dump(all_apis, f, ensure_ascii=False, indent=2)

print("Saved to static/apis.json")
