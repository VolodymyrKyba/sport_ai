from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.perplexity.ai")