import requests
from bs4 import BeautifulSoup

LANGUAGES = {
    "c": {
        "url": "https://github.com/trending/c?since=daily",
        "pending_file": "c_pending.txt",
        "done_file": "./done/c_done.txt",
    },
    "cpp": {
        "url": "https://github.com/trending/c++?since=daily",
        "pending_file": "cpp_pending.txt",
        "done_file": "./done/cpp_done.txt",
    }
}

def load_existing_links(*file_paths):
    existing_links = set()
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                existing_links.update(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            continue
    return existing_links

def fetch_trending_repos(url):
    base_url = "https://github.com"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[!] 요청 실패: {response.status_code} - {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return [base_url + a['href'] for a in soup.select('article h2 a')]

def save_new_links(file_path, new_links):
    with open(file_path, 'a', encoding='utf-8') as f:
        for link in new_links:
            f.write(link + '\n')

def main():
    for lang, config in LANGUAGES.items():
        print(f"\n {lang.upper()} Trending repositories 수집 중...")

        existing_links = load_existing_links(config['pending_file'], config['done_file'])
        trending_links = fetch_trending_repos(config['url'])

        new_links = [link for link in trending_links if link not in existing_links]
        duplicate_count = len(trending_links) - len(new_links) 

        if new_links:
            save_new_links(config['pending_file'], new_links)
        else:
            print("  -- 새로 추가된 저장소 없음 --")

        print(f"  -- 추가된 저장소 수: {len(new_links)}")
        print(f"  -- 중복된 저장소 수: {duplicate_count}")

if __name__ == "__main__":
    main()