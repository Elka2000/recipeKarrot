# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import requests




# Set the base URL for the Forismatic API
base_url = "http://api.forismatic.com/api/1.0/"

# Set the parameters for the API request
params = {
    "method": "getQuote",
    "lang": "en",  # specify the language of the quote
    "format": "text"  # specify the format of the response
}

# Send the API request and store the response
response = requests.get(base_url, params=params)
quote = "Hello present Alan. Take 10 minutes to meditate today. "+response.text
# Print the quote
print(quote)




# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC84dba84f7b524a63732c2e7dd1f3af45"
auth_token = "0faa32fb720c85b31f8bb122444fa5fd"
client = Client(account_sid, auth_token)

message = client.messages.create(
  body=quote,
  from_="+12068752717",
  to="+18012051758"
)

print(message.sid)