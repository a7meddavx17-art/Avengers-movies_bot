import requests, json, os, sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

URL = "https://egy.voxcinemas.com/movies/whatson"
TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FILE = "seen.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

html = None
for _ in range(3):
    try:
        html = requests.get(URL, timeout=40, headers=headers).text
        break
    except requests.RequestException as e:
        print("محاولة فشلت:", e)

if html is None:
    sys.exit("الموقع مردش")

soup = BeautifulSoup(html, "html.parser")

SKIP = {"whatson", "comingsoon", "advance-sales", "experiences"}

movies = {}
for a in soup.select('a[href*="/movies/"]'):
    if "#" in a["href"] or "?" in a["href"]:
        continue
    href = a["href"]
    slug = href.rstrip("/").split("/")[-1]
    if not slug or slug in SKIP or slug == "movies":
        continue
    name = a.get("title") or a.get_text(strip=True)
    if name and href not in movies:
        movies[href] = name

print("لقيت", len(movies), "فيلم")

if not movies:
    sys.exit("مفيش أفلام اتقرأت")

seen = set(json.load(open(FILE))) if os.path.exists(FILE) else None

if seen is not None:
    for href in movies.keys() - seen:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID,
                    "text": f"فيلم جديد نزل: {movies[href]}\n{urljoin(URL, href)}"},
        )

json.dump(sorted((seen or set()) | set(movies)), open(FILE, "w"), ensure_ascii=False)
