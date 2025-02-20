from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
import uvicorn  # Import Uvicorn
from config import client

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





@app.post("/submit")
async def receive_name(user: UserInput):

    team = user.name
    
    
    
    text = str(get_team_info(team))

    return {"message": text}

# print(receive_name())
# Run Uvicorn when this script is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
