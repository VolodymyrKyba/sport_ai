import requests
from bs4 import BeautifulSoup as bs

team = "Real Madrid"  # Приклад команди
query = f"{team} fan songs"

params = {
    "q": query,
    "tbm": "vid"  # Пошук лише відео
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

response = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)

if "detected unusual traffic" in response.text.lower():
    print("⚠ Google заблокував запит. Спробуйте VPN або API.")
else:
    soup = bs(response.text, "html.parser")

    # Витягуємо посилання на відео, перевіряючи, чи є атрибут "href"
    video_links = [a["href"] for a in soup.select("a") if a.has_attr("href") and "youtube.com" in a["href"]]

    if video_links:
        print("\n📺 Знайдені відео:")
        for link in video_links[:5]:  # Виводимо перші 5 відео
            print(link)
    else:
        print("❌ Відео не знайдено.")
