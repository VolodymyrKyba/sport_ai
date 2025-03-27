import scrapy
from scrapy.crawler import CrawlerProcess

class PlayerAssistSpider(scrapy.Spider):
    name = "player_assist"
    start_urls = ["https://www.espn.com/soccer/team/stats/_/id/83/barcelona"]

    def parse(self, response):
        # Вибірка всіх імен гравців
        players = response.css('td.Table__TD span a.AnchorLink::text').getall()

        # Відкриваємо файл для запису
        with open('players_list.txt', 'w') as f:
            # Записуємо кожне ім'я гравця в файл
            for player in players:
                f.write(player + '\n')  # Додаємо кожне ім'я на новому рядку

# Створення та запуск Scrapy-процесу
if __name__ == "__main__":
    process = CrawlerProcess()
    
    # Запуск павука
    process.crawl(PlayerAssistSpider)
    process.start()  # Запуск процесу та обробка даних
