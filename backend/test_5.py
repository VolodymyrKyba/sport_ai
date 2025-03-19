import requests

url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2025-03-19&'
       'sortBy=popularity&'
       'apiKey=2c9b21ba89654e01b5d383356c8c1228')

response = requests.get(url)

print(response)