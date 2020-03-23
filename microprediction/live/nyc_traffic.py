import requests

URL        = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"  # MTA city of NY realtime feed
VERRAZANO  = "416"  # "Verrazano-Narrows-Bridge"
BRONX      = "142"  # "BE S Griswold - Castle Hill Avenue"

def fetch_live_data(key,field):
    r = requests.get(URL)
    if r.status_code==200:
        data = r.json()
        selection = [ d for d in data if int(d["id"])==int(key) and d["status"]=="0"]
        selection.sort(key=lambda x:x["data_as_of"], reverse=True)
        if len(selection)>0:
            record = selection[0]
            return record[field]
        else:
            return None
    else:
        return None

def verrazano_speed():
    return fetch_live_data(key=VERRAZANO, field="speed")

def bronx_speed():
    return fetch_live_data(key=BRONX, field="speed")