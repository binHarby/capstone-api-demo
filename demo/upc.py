import requests import json import pandas as pd
import os
def nutri_upc(upc_code):
    url="https://api.nutritionix.com/v1_1/item?"
    querystring = {"upc":str(upc_code)}
    headers = {
        'appId': "809767c6",
        'appKey': "6f0672be9967f460f38fd1954120746f"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    #parsed json response
    LS=[1,3,4]
    par=json.loads(response.text)

    #return json response as json object / dict
    return par
def get_upc_data():
    Arr=[]
    #set panadas option for printing dataframes
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    with open('upc_codes.txt') as my_file:
        #have all upc codes from file in a list, with no spaces or new lines or tabs
        Arr=[x.replace(" ","") for x in my_file.read().splitlines() if x]
        #issue an api call for each upc code
        for x in Arr:
            #fetch api response 
            par=nutri_upc(x)
            #treat response as a dict, get its items to make dataframe
            par_items=par.items()
            par_list=list(par_items)
            df=pd.DataFrame(par_list)
            #transpose dataframe
            df_t=df.T
            #since first column is null, replace it with upc code
            df_t.at[0,0]='UPC_CODE'
            df_t.at[1, 0] = x
            if os.path.isfile("nutrix_upc.csv"):
                df_t.drop(index=df_t.index[0], axis=0,inplace=True)
                print(df_t) 
                df_t.to_csv("nutrix_upc.csv", mode='a', header=False,index=False)
            else:
                print(df_t) 
                df_t.to_csv("nutrix_upc.csv",header=False,index=False)

get_upc_data()
