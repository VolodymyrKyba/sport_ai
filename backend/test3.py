import json
from config2 import client
import re
import requests
from config import client_2
import http.client
import json
from bs4 import BeautifulSoup as bs
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
from scrapy import signals

class PlayerAssistSpider(scrapy.Spider):
    name = "player_assist"

    def __init__(self, team, *args, **kwargs):
        super(PlayerAssistSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://www.statmuse.com/fc/ask/player-with-most-assists-for-{team}"]

    def parse(self, response):
        assists = response.css('span.text-team-secondary span::text').getall()
        players = response.css('span.hidden::text').getall()

        for player, assist in zip(players, assists):
            yield {'player': player, 'assists': assist}

class PlayerFoulsDrawnSpider(scrapy.Spider):
    name = "player_fouls_drawn"

    def __init__(self, team, *args, **kwargs):
        super(PlayerFoulsDrawnSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://www.statmuse.com/fc/ask/player-with-most-fouls-drawn-for-{team}"]

    def parse(self, response):
        fouls = response.css('span.text-team-secondary span::text').getall()
        players = response.css('span.hidden::text').getall()

        for player, foul in zip(players, fouls):
            yield {'player': player, 'fouls_drawn': foul}


team = "Liverpool"


def Name(t_n):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
    response = requests.get(url)   
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            team_name = info.get("strTeam")
    return team_name

def Nickname(t_n):
        chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell me this team {t_n} nicknames, return only nicknames
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

        team_desc = chat_completion.choices[0].message.content
        
        return team_desc

def FoundingYear(t_n):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
    response = requests.get(url)   
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            team_year= info.get("intFormedYear")
    return team_year

def Location(t_n):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
    response = requests.get(url)   
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            team_location= info.get("strLocation")
    return team_location

def League_Division(t_n):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
    response = requests.get(url)
    lst_of_league = []
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            lst_of_league.append(info.get("strLeague"))
            for i in range(1, 8):  
                league_key = f"strLeague{i}" if i == 1 else f"strLeague{i-1}"
                league_value = info.get(league_key)
                if league_value and league_value != "":
                    lst_of_league.append(league_value)

    return lst_of_league

def Stadium_VenueName(t_n):
    try:
        formatted_name = t_n.replace(" ", "%20")
        conn = http.client.HTTPSConnection("v3.football.api-sports.io")
        headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': "4e1796c9bebdff310d3b134a9d9642d9"
        }
        conn.request("GET", 
                    f"/teams?name={formatted_name}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        venue_info = json.loads(data.decode("utf-8")).get("response")[0].get("venue")
        venue_details = f"Stadium Name: {venue_info['name']}\n" \
                        f"Address: {venue_info['address']}\n" \
                        f"City: {venue_info['city']}\n" \
                        f"Capacity: {venue_info['capacity']}\n" \
                        f"Surface: {venue_info['surface']}\n" \
                        f"Image: {venue_info['image']}"

        return venue_details
    except:
        return None



def TeamColors(t_n):

    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
    response = requests.get(url)
    lst_of_color = []
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            for i in range(1, 8):  # Check leagues from strLeague to strLeague7
                league_key = f"strColour{i}" if i == 1 else f"strColour{i-1}"
                league_value = info.get(league_key)
                if league_value and league_value != "":
                    lst_of_color.append(league_value)
    return lst_of_color

def Mascot(t_n):
    lst_image = []
    promt = f"{t_n} mascot"
    params = {"q" : promt , "tbm" : "isch",}
    html = requests.get("https://www.google.com/search",params=params,timeout=30)
    html.text
    soup = bs(html.content,features="html.parser")
    images = soup.select("div img")
    
    lst_image.append(images[1]["src"])
    lst_image.append( images[2]["src"])
    lst_image.append(images[3]["src"])

    return lst_image

    
def OfficialWebsite(t_n):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
    response = requests.get(url)   
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            team_website = info.get("strWebsite")
    return f"https://{team_website}"

def SocialMediaHandles(t_n):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
    response = requests.get(url)   
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            team_facebook = "https://" + info.get("strFacebook")
            team_twitter = "https://" + info.get("strTwitter")
            team_inst = "https://" + info.get("strInstagram")
    return f"{team_facebook}\n{team_twitter}\n{team_inst}"

# def SocialMediaEngagementMetrics(t_n):
#     return "SocialMediaEngagementMetrics by func"

# def NewsOutlets(t_n):
#     return "NewsOutlets by func"
    

def MajorAchievements(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell me shortly this team {t_n} major achievments
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc

def HistoricalRivals(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell me shortly this team {t_n} historical rivals
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc

def Songs(t_n):
    lst_of_songs = []
    query = f"{t_n} fan songs"

    params = {
        "q": query,
        "tbm": "vid"  
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)

    if "detected unusual traffic" in response.text.lower():
        print("⚠ Google заблокував запит. Спробуйте VPN або API.")
    else:
        soup = bs(response.text, "html.parser")

        video_links = [a["href"] for a in soup.select("a") if a.has_attr("href") and "youtube.com" in a["href"]]

        if video_links:

            for link in video_links[:5]:  
                
                lst_of_songs.append(link)

    return(lst_of_songs)

def Traditions(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell me top 3 traditions of this sport team {t_n}
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc
    

# def FanEngagementInitiatives(t_n):
#     return "FanEngagementInitiatives by func"

def TV_RadioBroadcasters(t_n):
    lst_of_broadcast = []
    query = f"{t_n} broadcast"

    params = {
        "q": query,
        "tbm": "vid"  
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)

    if "detected unusual traffic" in response.text.lower():
        print("⚠ Google заблокував запит. Спробуйте VPN або API.")
    else:
        soup = bs(response.text, "html.parser")

        video_links = [a["href"] for a in soup.select("a") if a.has_attr("href") and "youtube.com" in a["href"]]

        if video_links:

            for link in video_links[:5]:  
                
                lst_of_broadcast.append(link)

    return(lst_of_broadcast)

def Playing_Styles(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell shortly  about playing styles of this team {t_n}
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc
    

def HistoricalSignificance(t_n):
    lst_image = []
    promt = f"{t_n}  Historical Significance sport  team"
    params = {"q" : promt , "tbm" : "isch",}
    html = requests.get("https://www.google.com/search",params=params,timeout=30)
    html.text
    soup = bs(html.content,features="html.parser")
    images = soup.select("div img")
    
    lst_image.append(images[1]["src"])
    lst_image.append( images[2]["src"])
    lst_image.append(images[3]["src"])
    lst_image.append(images[4]["src"])
    lst_image.append(images[5]["src"])

    return lst_image

# def SymbolismAndIconography(t_n):
#     return "SymbolismAndIconography by func"

def LegendaryPlayers(t_n):
    dct_of_player = {}
    def took_image(player_name):
        promt = f"{player_name}"
        params = {"q" : promt , "tbm" : "isch",}
        html = requests.get("https://www.google.com/search",params=params,timeout=30)
        html.text
        soup = bs(html.content,features="html.parser")
        images = soup.select("div img")
        return images[1]["src"]

    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Return a list [] with name of top 3 legendary players of this team {t_n}
                1.Name
                2.Name
                3.Name 
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
    names = re.findall(r"\d+\.\s(.+)", team_desc) 
    for name in names:
        dct_of_player[name] = took_image(name)
    return dct_of_player

    

def Coaches_Managers(t_n):
    dct_of_coach = {}
    def took_image(coach_name):
        promt = f"{coach_name}"
        params = {"q" : promt , "tbm" : "isch",}
        html = requests.get("https://www.google.com/search",params=params,timeout=30)
        html.text
        soup = bs(html.content,features="html.parser")
        images = soup.select("div img")
        return images[1]["src"]

    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Return a list [] with name of top 3 coach of this team {t_n}
                1.Name
                2.Name
                3.Name 
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
    names = re.findall(r"\d+\.\s(.+)", team_desc) 
    for name in names:
        dct_of_coach[name] = took_image(name)
    return dct_of_coach

# def Owners_Executives(t_n):
#     return "Owners/Executives by func"

def CharitableInitiatives(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell shortly about Charitable Initiatives of this team {t_n}
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc

# def YouthDevelopmentPrograms(t_n):
#     return "YouthDevelopmentPrograms by func"

# def StadiumFeatures(t_n):
#     return "StadiumFeatures by func"

def PreGameRituals(t_n):
    lst_of_rituals = []
    query = f"{t_n} Pre Game Rituals"

    params = {
        "q": query,
        "tbm": "vid"  
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)

    if "detected unusual traffic" in response.text.lower():
        print("⚠ Google заблокував запит. Спробуйте VPN або API.")
    else:
        soup = bs(response.text, "html.parser")

        video_links = [a["href"] for a in soup.select("a") if a.has_attr("href") and "youtube.com" in a["href"]]

        if video_links:

            for link in video_links[:5]:  
                
                lst_of_rituals.append(link)

    return(lst_of_rituals)

# def ConcessionOptions(t_n):
#     return "ConcessionOptions by func"

def RecentPerformance(t_n):
    def get_team_api_info(t_n):
        url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("teams"):
                return data["teams"][0].get("idTeam")
        return None  # Ensure it returns None if no team is found

    team_id = get_team_api_info(t_n)
    if not team_id:
        return "<p>Team not found.</p>"

    url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            info = data["results"]
            events = "<h3>📅 Last 5 Matches:</h3><table border='1' style='width:100%; text-align:center;'><tr><th>Date</th><th>Home</th><th>Score</th><th>Away</th></tr>"
            for match in info:
                events += f"<tr><td>{match.get('dateEventLocal')}</td><td>{match.get('strHomeTeam')}</td><td>{match.get('intHomeScore')}-{match.get('intAwayScore')}</td><td>{match.get('strAwayTeam')}</td></tr>"
            events += "</table>"
            return events
    return "<p>No match data available.</p>"

def HistoricalStatistics(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Provide historical statistics of this team {t_n}
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc

def PlayerGoals(t_n):
    lst_of_top_moments = []
    query = f"{t_n} Top goal and moments"

    params = {
        "q": query,
        "tbm": "vid"  
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)

    if "detected unusual traffic" in response.text.lower():
        print("⚠ Google заблокував запит. Спробуйте VPN або API.")
    else:
        soup = bs(response.text, "html.parser")

        video_links = [a["href"] for a in soup.select("a") if a.has_attr("href") and "youtube.com" in a["href"]]

        if video_links:

            for link in video_links[:5]:  
                
                lst_of_top_moments.append(link)

    return(lst_of_top_moments)

 

def PlayerAssists(t_n):
    logging.getLogger('scrapy').setLevel(logging.WARNING)

    results = []

    def collect_items(item, response, spider):
        results.append(item)

    process = CrawlerProcess(settings={"LOG_LEVEL": "WARNING"})
    crawler = process.create_crawler(PlayerAssistSpider)
    crawler.signals.connect(collect_items, signals.item_scraped)

    process.crawl(crawler, team=t_n)
    process.start()

    return results

def PlayerFoulsDrawn(team_name):
    logging.getLogger('scrapy').setLevel(logging.WARNING)

    results = []

    def collect_items(item, response, spider):
        results.append(item)

    process = CrawlerProcess(settings={"LOG_LEVEL": "WARNING"})
    crawler = process.create_crawler(PlayerFoulsDrawnSpider)
    crawler.signals.connect(collect_items, signals.item_scraped)

    process.crawl(crawler, team=team_name)
    process.start()

    return results




# def PlayerTacklesMade(t_n):
#     return "PlayerTacklesMade by func"

# def FantasyFootballRankings(t_n):
#     return "FantasyFootballRankings by func"

# def StrengthOfSchedule(t_n):
#     return "StrengthOfSchedule by func"

# def BoomOutlierPlayers(t_n):
#     return "BoomOutlierPlayers by func"

# def TeamMascot(t_n):
#     return "TeamMascot by func"




def SpecialEvents(t_n):
    def get_team_api_info(t_n):
        url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={t_n}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("teams"):
                return data["teams"][0].get("idTeam")
        return None  # Ensure it returns None if no team is found

    team_id = get_team_api_info(t_n)
    if not team_id:
        return "<p>Team not found.</p>"

    url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            info = data["results"]
            events = "<h3>📅 Last 5 Matches:</h3><table border='1' style='width:100%; text-align:center;'><tr><th>Date</th><th>Home</th><th>Score</th><th>Away</th></tr>"
            for match in info:
                events += f"<tr><td>{match.get('dateEventLocal')}</td><td>{match.get('strHomeTeam')}</td><td>{match.get('intHomeScore')}-{match.get('intAwayScore')}</td><td>{match.get('strAwayTeam')}</td></tr>"
            events += "</table>"
            return events
    return "<p>No match data available.</p>"

# def FanForumsAndCommunities(t_n):
#     url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}"
    
#     response = requests.get(url)
        
#     if response.status_code == 200:
#         data = response.json()
#         if data.get("teams"):
#             info = data["teams"][0]
#             team_website = info.get("strWebsite")
#             team_facebook = info.get("strFacebook")
#             team_twitter = info.get("strTwitter")
#             team_inst = info.get("strInstagram")
#     return team_website,team_facebook,team_twitter,team_inst

def FamousFans(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell me famous fans of this team {t_n} 
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc

def PreferredFormation(t_n):
    
    promt = f"{t_n} preferred formation"
    params = {"q" : promt , "tbm" : "isch",}
    html = requests.get("https://www.google.com/search",params=params,timeout=30)
    html.text
    soup = bs(html.content,features="html.parser")
    images = soup.select("div img")
    return images[1]["src"]

# def TacticalStyle(t_n):
#     return "TacticalStyle by func"

def SetPieceTactics(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Tell me shortly Set Piece Tactics of this team {t_n} 
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc

# def NotableTacticalChanges(t_n):
#     return "NotableTacticalChanges by func"

def CurrentHeadCoach_Manager(t_n):
  
    search_query = f"{t_n} current head coach"
    params = {"q": search_query, "tbm": "nws"}  # Використання пошуку новин для кращого результату
    response = requests.get("https://www.google.com/search", params=params, timeout=30)
    
    if response.status_code != 200:
        return None, None
    
    soup = bs(response.content, "html.parser")
    name_element = soup.select_one(".BNeawe.s3v9rd.AP7Wnd")  # Пошук першого релевантного текстового результату
    
    image_params = {"q": f"{t_n} current head coach", "tbm": "isch"}  # Пошук зображень
    image_response = requests.get("https://www.google.com/search", params=image_params, timeout=30)
    
    if image_response.status_code != 200:
        return None, None
    
    image_soup = bs(image_response.content, "html.parser")
    images = image_soup.select("div img")
    
    coach_name = name_element.text if name_element else "Unknown"
    coach_image = images[1]["src"] if len(images) > 1 else None
    
    return coach_name, coach_image
 

   

# def AssistantCoaches(t_n):
#     return "AssistantCoaches by func"


# def PreviousNotableManagers(t_n):
#     return "PreviousNotableManagers by func"

# def ManagerialPhilosophy(t_n):
#     return "ManagerialPhilosophy by func"

def EstimatedTeamValue(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Return only estimated team value of this team {t_n} 
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc

def MajorSponsors(t_n):
    chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Return only major sponsors of this team {t_n} 
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    team_desc = chat_completion.choices[0].message.content
        
    return team_desc
# def KitManufacturer(t_n):
#     return "KitManufacturer by func"

# def TicketPrices(t_n):
#     return "TicketPrices by func"

# def AttendanceRecords(t_n):
#     return "AttendanceRecords by func"

# def MajorTrophies(t_n):
#     return "MajorTrophies by func"

# def ClubLegends(t_n):
#     return "ClubLegends by func"

# def RecordsAndMilestones(t_n):
#     return "RecordsAndMilestones by func"

# def EsotericRules(t_n):
#     return "EsotericRules by func"

# def TeamCharityWork(t_n):
#     return "TeamCharityWork by func"

# def SocialResponsibilityInitiatives(t_n):
#     return "SocialResponsibilityInitiatives by func"

# def YouthAcademy(t_n):
#     return "YouthAcademy by func"

# def IconicMemes(t_n):
#     return "IconicMemes by func"

# def PopularSocialMediaReactions(t_n):
#     return "PopularSocialMediaReactions by func"

# def FanMadeContent(t_n):
#     return "FanMadeContent by func"


def extract_numbers_from_text(text):
    numbers = re.findall(r'\d+', text)
    return [int(number) for number in numbers]


with open("/home/volodymyrkyba/work/sport_ai/backend/source_data.json", "r", encoding="utf-8") as file:
    dict_of_point = json.load(file)


# def get_team_ai_info(team,dict_of_point):
            
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You are a helpful sport assistant"
#             ),
#         },
#         {   
#             "role": "user",
#             "content": (
#                 f"""I'm creating a web page that would provide information about a sports team for someone going to a meeting with their boss or friends to stay up to date on the topic. Also choose songs I have a list of key features  so choose the ones that best fit the team {team} Here we have list {dict_of_point},
#                 return only serial number of features
#                 """
#             ),
#         },
#     ]
        
#     team_desc = client.chat.completions.create(
#     model="sonar-pro",
#     messages=messages,)
#     return team_desc.choices[0].message.content




# def get_team_ai_info(team,dict_of_point):

#         chat_completion = client_2.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful sport assistant."
#             },
#             {
#                 "role": "user",
#                 "content": f"""From this list {dict_of_point} choose the best features about this team,
#                 return only serial number of features
#                 """,
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )

#         team_desc = chat_completion.choices[0].message.content
        
#         return team_desc



# lst_of_point = extract_numbers_from_text(get_team_ai_info(team,dict_of_point))
# print(lst_of_point)
# for number in lst_of_point:
#     feature = dict_of_point.get(str(number))
    
#     if feature in globals(): 
        
#         print(globals()[feature](team))




# print(Coaches_Managers("Manchester United"))
# print(CharitableInitiatives("Miami Heat"))
# print(PreGameRituals("Chicago Bulls"))
# print(RecentPerformance("Barcelona"))
# print(HistoricalStatistics("Barcelona"))
# print(PlayerGoals("Chicago Bulls"))
# print(PlayerAssists("Barcelona"))
# print(PreferredFormation("Barcelona"))
# print(EstimatedTeamValue("Barcelona"))
print(MajorSponsors("Barcelona"))