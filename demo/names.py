import json
import pandas as pd
import requests
import os
def nutrix_name(name):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    url="https://trackapi.nutritionix.com/v2/natural/nutrients"
    food_name=name
    querystring = {"query":food_name}
    headers = {
        'x-app-id': "809767c6",
        'x-app-key': "6f0672be9967f460f38fd1954120746f"
        }
    
    response = requests.request("POST", url, headers=headers, json=querystring)
    #parsed json response
    
    par=json.loads(response.text)
    try:
         par=par['foods'][0]
         par.pop("full_nutrients", None)
         par.pop("alt_measures", None)
         par.pop("photo", None)
         par.pop("tags", None)
    except KeyError:
        print("Error: can't find food: "+name)     
        par={"food_name":name,"status":"Can't Find It :("}
    df = pd.json_normalize(par)
    df.at[0,'food_name']=food_name
    if os.path.isfile("food_name_lookup.csv"):
        print(df)
        df.to_csv("food_name_lookup.csv", mode='a', header=False,index=False)
    else:
        df.to_csv("food_name_lookup.csv",index=False)
    #return json response as json object / dict
with open('foods.txt') as food_file:
    lss=[x for x in food_file.read().splitlines() if x]

    for food in lss:
        nutrix_name(food)
