import requests

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '4e1796c9bebdff310d3b134a9d9642d9'
# Replace 'TEAM_ID' with the actual team ID for FC Barcelona
team_id = '529'
# Define the number of recent games you want to retrieve
number_of_games = 5
# Define the API endpoint URL for the last fixtures
api_url = f'https://v3.football.api-sports.io/fixtures?team=529'

# Set up the API request headers with the correct 'x-apisports-key'
headers = {
    'x-apisports-key': api_key,
    'Accept': 'application/json',
}

# Make the API request using the requests library
response = requests.get(api_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Print the details of the recent games
    print(data)