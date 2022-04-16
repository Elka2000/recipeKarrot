import http.client

conn = http.client.HTTPSConnection("random-recipes.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "random-recipes.p.rapidapi.com",
    'x-rapidapi-key': "5df4348c1emsh0e08e22d3e30845p18a7edjsn864c503474fc"
    }

conn.request("GET", "/ai-quotes/%7Bid%7D", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))