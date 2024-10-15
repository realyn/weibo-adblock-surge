import os
import requests
from urllib.parse import urlparse

def fetch_js_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch content from {url}")
        return None

def convert_to_sgmodule(js_content, js_filename, js_url):
    base_filename = os.path.splitext(js_filename)[0]
    
    sgmodule_content = f'''#!name={base_filename}
#!desc=Converted from {js_filename}

[Script]
{base_filename} = type=http-response,pattern=^https?://.*$,requires-body=1,max-size=0,script-path={js_url}

[MITM]
hostname = %APPEND% *
'''
    return sgmodule_content

def save_sgmodule(content, filename):
    os.makedirs('loon_js_c_surge', exist_ok=True)
    with open(os.path.join('loon_js_c_surge', filename), 'w') as f:
        f.write(content)

def process_js_file(js_url):
    js_content = fetch_js_content(js_url)
    if js_content:
        js_filename = os.path.basename(urlparse(js_url).path)
        sgmodule_content = convert_to_sgmodule(js_content, js_filename, js_url)
        sgmodule_filename = js_filename.replace('.js', '.sgmodule')
        save_sgmodule(sgmodule_content, sgmodule_filename)
        print(f"Converted {js_filename} to {sgmodule_filename}")

def main():
    js_urls = [
        "https://raw.githubusercontent.com/luestr/ProxyResource/refs/heads/main/Resource/Script/Weibo/Weibo_remove_ads.js",
        "https://github.com/luestr/ProxyResource/raw/refs/heads/main/Resource/Script/Amap/Amap_remove_ads.js"
    ]
    
    for url in js_urls:
        process_js_file(url)

if __name__ == "__main__":
    main()