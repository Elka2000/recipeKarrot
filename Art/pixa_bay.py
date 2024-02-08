import requests

# API key (obtain one from https://pixabay.com/api/docs/)
api_key = "32179643-4da4f9bd1678f7af8e6f59732"

# Search term
q = "city+night"
#number of links per page
count = 4

# Send the request to the API
response = requests.get(f"https://pixabay.com/api/?key={api_key}&q={q}&per_page={count}")

# Check the status code
if response.status_code == 200:
    # Print the search results
    data = response.json()
    print('------------------------------------------------------------------------')
    print(data)
    num = 0
    
    for hit in data["hits"]:
        name = q+"_"+str(num)+".jpg" 
        
        print(hit["webformatURL"])
        response = requests.get(hit['webformatURL'])
        if response.status_code == 200:
        # Save the image to a file
            num+=1
            print(num)
            with open(name, "wb") as f:
                f.write(response.content)
            print("Image downloaded!")
        else:
            print("An error occurred")
        

else:
    print("An error occurred")
