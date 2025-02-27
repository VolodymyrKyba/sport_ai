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

def get_team_info(team):

        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful sport assistant."
            },
            {
                "role": "user",
                "content": f"""Give me short information about this team {team} in this format:
                - Last games(score)
                - Current standings
                - Latest News
                - Talking Points
                - Fun Facts
                - Celebrity Gossip
                - Workplace Drama
                - Funny Metaphors 
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

def take_logo(team):
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}"
    
    response = requests.get(url)
        
    if response.status_code == 200:
        data = response.json()
        if data.get("teams"):
            return data["teams"][0].get("strBadge")
    return None

def beautify_text(text):
    replacements = {
        "**Last games(score)**": "🏆 Last Games (Score)",
        "**Current standings**": "📊 Current Standings",
        "**Latest News**": "📰 Latest News",
        "**Talking Points**": "💬 Talking Points",
        "**Fun Facts**": "🎉 Fun Facts",
        "**Celebrity Gossip**": "🌟 Celebrity Gossip",
        "**Workplace Drama**": "🎭 Workplace Drama",
        "**Funny Metaphors**": "😂 Funny Metaphors"
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

@app.post("/submit")
async def receive_name(user: UserInput):
    team = user.name
    logo_url = take_logo(team)
    team_info = get_team_info(team)
    team_info = beautify_text(team_info)
    print(team_info)
    print(logo_url)
    
    return JSONResponse(content={
        "message": team_info,
        "logo_url": logo_url
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
