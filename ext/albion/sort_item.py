from rapidfuzz import process, fuzz
import json
import os
import requests

def getrawfromAPI():
    response = requests.get("https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json")
    data = response.json()
    datasortraw = []
    for i in range(len(data)):
        try:
            datainput = {
                'id' : data[i]['Index'],
                'name': data[i]['LocalizedNames']['EN-US'],
                'uniq_name' : data[i]['UniqueName']
            }
            datasortraw.append(datainput) if datainput not in datasortraw else datasortraw
        except:
            continue

    return datasortraw

def ByNames(item):
    data = getrawfromAPI()
    datasortraw = []
    for i in range(len(data)):
        datainput = data[i]['name']
        datasortraw.append(datainput) if datainput not in datasortraw else datasortraw
    data_ret = process.extract(item, datasortraw, scorer=fuzz.WRatio, limit=5)
    return data_ret

def ByTier(tier, name):
    if tier == 'T1':
        tiername = "Beginner's"
    if tier == 'T2':
        tiername == "Novice's"
    if tier == 'T3':
        tiername == "Journeyman's"
    if tier == 'T4':
        tiername == "Adept's"
    if tier == 'T5':
        tiername == "Expert's"
    if tier == 'T6':
        tiername == "Master's"
    if tier == 'T7':
        tiername == "Grandmaster's"
    if tier == 'T8':
        tiername == "Elder's"

# print(ByNames("Adept Facebreaker")[0][0])