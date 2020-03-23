import requests

# Number of bikes available at Madison and 48th


def fetch_live_data(key,field):
    r = requests.get("https://feeds.citibikenyc.com/stations/stations.json")
    if r.status_code==200:
        data = r.json()
        station_data = [ d for d in data["stationBeanList"] if int(d["id"])==key ]
        if len(station_data)==1:
            record = station_data[0]
            return record[field]
        else:
            raise Exception("Invalid key")
    else:
        return None


def madison_bikes_available():
    return fetch_live_data(key=456,field="availableBikes")

