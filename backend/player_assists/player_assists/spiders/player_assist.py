import scrapy
from scrapy.crawler import CrawlerProcess
import logging
from scrapy import signals
import requests

class TeamSpecialEventsSpider(scrapy.Spider):
    name = "team_special_events"

    def __init__(self, team_name, team_id, *args, **kwargs):
        super(TeamSpecialEventsSpider, self).__init__(*args, **kwargs)
        self.team_name = team_name
        self.team_id = team_id
        self.start_urls = [f"https://www.espn.com/soccer/team/fixtures/_/id/{team_id}"]

    def parse(self, response):
        rows = response.css('td[width="10%"]')
        for row in rows:
            link = row.css('a::attr(href)').get()
            date = row.css('::text').get().strip()
            if link and "event" in link:
                event_id = link.split("/")[2].split("-")[0]
                yield {
                    "team": self.team_name,
                    "event_id": event_id,
                    "date": date,
                    "url": f"https://www.espn.com{link}"
                }


def get_team_api_info(team_name):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            return data["teams"][0].get("idTeam")
    return None


def get_special_events(teams):
    logging.getLogger('scrapy').setLevel(logging.WARNING)

    results = []

    def collect_items(item, response, spider):
        results.append(item)

    process = CrawlerProcess(settings={"LOG_LEVEL": "WARNING"})

    for team_name in teams:
        team_id = get_team_api_info(team_name)
        if team_id:
            crawler = process.create_crawler(TeamSpecialEventsSpider)
            crawler.signals.connect(collect_items, signals.item_scraped)
            process.crawl(crawler, team_name=team_name, team_id=team_id)

    process.start()

    return results


# Приклад використання:
teams = [
    "real madrid",
    "barcelona",
    "chelsea"
]

events_list = get_special_events(teams)
print(events_list)