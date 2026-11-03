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
