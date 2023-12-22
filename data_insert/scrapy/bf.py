import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import time

def download_file(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = os.path.basename(urlparse(url).path)
            file_path = os.path.join("./download", file_name)
            # with open(file_path, 'wb') as file:
            #     file.write(response.content)
            with open(file_path, 'wb') as file:
                # 逐块写入文件
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
                    
            print(f"File downloaded: {file_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def get_links_from_page(url, domain):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            extracted_links = []
            for link in links:
                href = link.get('href')
                if href:
                    if not href.startswith('http'):
                        href = url + href
                    parsed_url = urlparse(href)
                    if parsed_url.netloc.endswith(domain):
                        extracted_links.append(urljoin(url, href))
            return extracted_links
    except Exception as e:
        print(f"Failed to fetch links from {url}: {e}")
        return []

def crawl_website(start_url, domain, file_types):
    visited_urls = set()
    queue = [start_url]
    qps_limit = 10  # 设置 QPS 限制为 10

    while queue:
        current_url = queue.pop(0)
        visited_urls.add(current_url)
        print(f"Processing: {current_url}")

        links = get_links_from_page(current_url, domain)

        if links:
            for link in links:
                if link not in visited_urls and link not in queue:
                    queue.append(link)

        for file_type in file_types:
            if current_url.lower().endswith(file_type):
                download_file(current_url)

        # 控制 QPS
        time.sleep(1 / qps_limit)  # 每次请求后等待一段时间

if __name__ == "__main__":
    start_url = 'https://finance.ustc.edu.cn'  # 将你的起始页面 URL 替换成实际的 URL
    domain = 'finance.ustc.edu.cn'  # 想要爬取的域名
    file_types = ['.pdf', '.docx', '.xlsx']  # 想要下载的文件类型

    crawl_website(start_url, domain, file_types)

