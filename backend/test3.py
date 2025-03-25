import json
from config2 import client
import re
import requests
from config import client_2
import http.client
import json
from bs4 import BeautifulSoup as bs

team = "Yankees"


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
            for i in range(1, 8):  # Check leagues from strLeague to strLeague7
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
        # Use the team ID for Barcelona, which is 529
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

# def LegendaryPlayers(t_n):
#     return "LegendaryPlayers by func"

# def Coaches_Managers(t_n):
#     return "Coaches/Managers by func"

# def Owners_Executives(t_n):
#     return "Owners/Executives by func"

# def CharitableInitiatives(t_n):
#     return "CharitableInitiatives by func"

# def YouthDevelopmentPrograms(t_n):
#     return "YouthDevelopmentPrograms by func"

# def StadiumFeatures(t_n):
#     return "StadiumFeatures by func"

# def PreGameRituals(t_n):
#     return "PreGameRituals by func"

# def ConcessionOptions(t_n):
#     return "ConcessionOptions by func"

# def RecentPerformance(t_n):
#     return "RecentPerformance by func"

# def HistoricalStatistics(t_n):
#     return "HistoricalStatistics by func"

# def PlayerGoals(t_n):
#     return "PlayerGoals by func"

# def PlayerAssists(t_n):
#     return "PlayerAssists by func"

# def PlayerFoulsDrawn(t_n):
#     return "PlayerFoulsDrawn by func"

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

# def SpecialEvents(t_n):
#     return "SpecialEvents by func"

# def FanForumsAndCommunities(t_n):
#     return "FanForumsAndCommunities by func"

# def FamousFans(t_n):
#     return "FamousFans by func"

# def PreferredFormation(t_n):
#     return "PreferredFormation by func"

# def TacticalStyle(t_n):
#     return "TacticalStyle by func"

# def SetPieceTactics(t_n):
#     return "SetPieceTactics by func"

# def NotableTacticalChanges(t_n):
#     return "NotableTacticalChanges by func"

# def CurrentHeadCoach_Manager(t_n):
#     return "CurrentHeadCoach/Manager by func"

# def AssistantCoaches(t_n):
#     return "AssistantCoaches by func"

# def PreviousNotableManagers(t_n):
#     return "PreviousNotableManagers by func"

# def ManagerialPhilosophy(t_n):
#     return "ManagerialPhilosophy by func"

# def EstimatedTeamValue(t_n):
#     return "EstimatedTeamValue by func"

# def MajorSponsors(t_n):
#     return "MajorSponsors by func"

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
    # Використовуємо регулярний вираз для пошуку всіх чисел у тексті
    numbers = re.findall(r'\d+', text)
    # Перетворюємо знайдені числа на тип int
    return [int(number) for number in numbers]


with open("/home/volodymyrkyba/work/sport_ai/backend/source_data.json", "r", encoding="utf-8") as file:
    dict_of_point = json.load(file)
    # print(dict_of_point)


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




def get_team_ai_info(team,dict_of_point):

        chat_completion = client_2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""From this list {dict_of_point} choose the best features about this team,
                return only serial number of features
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

        team_desc = chat_completion.choices[0].message.content
        
        return team_desc



lst_of_point = extract_numbers_from_text(get_team_ai_info(team,dict_of_point))
print(lst_of_point)
for number in lst_of_point:
    feature = dict_of_point.get(str(number))
    
    if feature in globals(): 
        
        print(globals()[feature](team))


