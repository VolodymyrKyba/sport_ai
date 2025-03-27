import scrapy

class AssistsSpider(scrapy.Spider):
    name = "assists"
    allowed_domains = ["whoscored.com"]  # Або інший сайт з даними
    start_urls = ["https://www.whoscored.com/Statistics"]  # Замінити на актуальну сторінку

    def parse(self, response):
        players = response.css("table tr")  # Приклад, структура може відрізнятися
        for player in players:
            yield {
                "name": player.css("td.player-name::text").get(),
                "team": player.css("td.team-name::text").get(),
                "assists": player.css("td.assists::text").get()
            }
