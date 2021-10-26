import requests
import json 
import pandas as pd
import os
pd.set_option("display.max_rows", None, "display.max_columns", None)
def logmeals_calls(image):
    #get path to image
    img=os.path.join(os.getcwd(),"images",image)
    api_user_token = 'bfdd636af5854c3e953d2982364585ea78e79d55'
    headers = {'Authorization': 'Bearer ' + api_user_token}
    
    # Single/Several Dishes Detection
    url = 'https://api.logmeal.es/v2/recognition/complete'
    resp = requests.post(url,files={'image': open(img, 'rb')},headers=headers)
    
    # Nutritional information
    try:
        url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
        resp = requests.post(url,json={'imageId': resp.json()['imageId']}, headers=headers)
        par=json.loads(resp.text)
    except Exception as e:
        par={"image path":img,"status":"Can't find it :("}
    par_indent=json.dumps(par, indent=4, sort_keys=True)
    print(img)
    print(par_indent)
    with open("res.txt","a+") as o:
        o.write(img)
        o.write(par_indent)
    #df = pd.json_normalize(par)
    #print(df)
    #df.at[0,'image path']=img
    #df.to_csv("logmeals_food.csv",index=False)
#print(resp.json()) # display json response
pathh=os.path.join(os.getcwd(),"images")
ls_file=[f for f in os.listdir(pathh) if os.path.isfile(os.path.join(pathh,f))]

for x in ls_file:
    logmeals_calls(x)
