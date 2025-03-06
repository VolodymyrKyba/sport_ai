from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn  # Import Uvicorn
from config import client
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)
class UserInput(BaseModel):
    name: str = Field(..., example="Johsdn")

def get_team_ai_info(team):

        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Give me short information about this team {team} in this format:

                Information:
                -Current standings: 
                info
                -Latest News: 
                info
                -Talking Points: 
                info
                -Fun Facts: 
                info
                -Slogan:
                info
                -Workplace Drama:
                info
                -Funny Metaphors: 
                info
                """,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

        team_desc = chat_completion.choices[0].message.content
        
        return team_desc


# def get_team_info(team):

#         chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful sport assistant."
#             },
#             {
#                 "role": "user",
#                 "content": f"""Give me link to logo of this team{team} 
#                 """,
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )

#         team_desc = chat_completion.choices[0].message.content

#         return team_desc

# def get_team_info(team):
            
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
#                 f"""Give me short information about this team {team} in this format:
#                  - Last games(score)
#                  - Current standings
#                  - Latest News
#                  - Talking Points
#                  - Fun Facts
#                  - Celebrity Gossip
#                  - Workplace Drama
#                  - Funny Metaphors 
#                  """
#             ),
#         },
#     ]
        
#     team_desc = client.chat.completions.create(
#     model="sonar-pro",
#     messages=messages,)
#     print(team_desc.choices[0].message.content
# )
#     return team_desc.choices[0].message.content

# def take_logo(team):
#     url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}"
    
#     response = requests.get(url)
        
#     if response.status_code == 200:
#         data = response.json()
#         if data.get("teams"):
#             return data["teams"][0].get("strBadge")
#     return None





def get_last_5_games(team_id):
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



def get_team_api_info(team):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}"
    
    response = requests.get(url)
        
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            info = data["teams"][0]
            id_Team = info.get("idTeam")
            team_Logo = info.get("strBadge")
            team_banner = info.get("strBanner")
            team_uniform = info.get("strEquipment")
            team_name = info.get("strTeam")
            team_year = f"<< {info.get("intFormedYear")} >>"
            team_website = info.get("strWebsite")
            team_facebook = info.get("strFacebook")
            team_twitter = info.get("strTwitter")
            team_inst = info.get("strInstagram")
    return id_Team , team_Logo , team_banner ,team_uniform , team_name ,team_year,team_website,team_facebook,team_twitter,team_inst

def beautify_text(text):
    replacements = {
        "Information:": "<h1>📖 Information about your team ",
        "-Current standings:": "<h3>📊  Current Standings:</h3>",
        "-Latest News:": "<h3>📰  Latest News:</h3>",
        "-Talking Points:": "<h3>💬  Talking Points:</h3>",
        "-Fun Facts:": "<h3>🎉  Fun Facts:</h3>",
        "-Slogan:": "<h3>🌟  Slogan:</h3>",
        "-Workplace Drama:": "<h3>🎭  Workplace Drama:</h3>",
        "-Funny Metaphors:": "<h3>😂  Funny Metaphors:</h3>"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    clean_text = "\n".join(line for line in text.splitlines() if line.strip())
    return clean_text

@app.post("/submit")
async def receive_name(user: UserInput):
    team = user.name
    team_id, logo_url ,team_banner , team_uniform ,team_name ,team_year,team_website,team_facebook,team_twitter,team_inst =  get_team_api_info(team)
    team_info = get_team_ai_info(team)
    team_info = beautify_text(team_info)
    team_l_5_events = get_last_5_games(team_id)
    print("Ready")

    # print(team_events)
    # print(team_id)
    # print(team_info)
    # print(logo_url)
    # print(team_l_5_events)

    return JSONResponse(content={
        "message": team_info,
        "banner_url": team_banner,
        "unifrom_url" : team_uniform,
        "logo" : logo_url,
        "nick_name" : team_name,
        "last_5_events" : team_l_5_events,
        "team_year" : team_year,
        "team_website" : team_website,
        "team_facebook" : team_facebook,
        "team_twitter" : team_twitter,
        "team_inst" : team_inst,
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
