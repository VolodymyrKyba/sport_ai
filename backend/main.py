from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi.middleware.cors import CORSMiddleware
import uvicorn  # Import Uvicorn

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

@app.post("/submit")
async def receive_name(user: UserInput):
    n = len(user.name)
    

    return {"message": n}

# print(receive_name())
# Run Uvicorn when this script is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
