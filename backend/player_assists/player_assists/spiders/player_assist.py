import requests
from bs4 import BeautifulSoup as bs

def get_social_media_reactions(t_n):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # 1. Пошук реакції у новинах
    search_query = f"{t_n} popular social media reactions"
    params = {"q": search_query, "tbm": "nws"}  # новини
    response = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)

    if response.status_code != 200:
        return None, None, None

    soup = bs(response.content, "html.parser")
    reaction_element = soup.select_one(".BNeawe.s3v9rd.AP7Wnd")

    # 2. Пошук картинки (мем / реакція)
    image_params = {"q": search_query, "tbm": "isch"} 
    image_response = requests.get("https://www.google.com/search", params=image_params, headers=headers, timeout=30)

    if image_response.status_code != 200:
        return None, None, None

    image_soup = bs(image_response.content, "html.parser")
    images = image_soup.select("img")

    # 3. Пошук останніх 3 новин
    news_list = []
    news_items = soup.select("div.dbsr")
    for item in news_items[:3]:
        title = item.select_one("div.JheGif.nDgy9d")
        link = item.a["href"]
        if title and link:
            news_list.append({"title": title.text, "link": link})

    # Формування результату
    reaction_text = reaction_element.text if reaction_element else "No reaction found"
    image_url = images[1]["src"] if len(images) > 1 else None

    return reaction_text, image_url, news_list

# Використання
print( get_social_media_reactions("Miami heat"))
