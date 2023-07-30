import requests
from decouple import config

def notify(startTime, endTime, totalGames):
    url = config("DISCORDWEBHOOK")
    data = {
        "content": "Rezi has been updated!"
    }
    data["embeds"] = [
        {
            "title" : "Rezi scraper has completed.",
            "color" : 558272,
            "fields" : [
                {
                    "name" : "Time taken",
                    "value" : f"{round((endTime - startTime).total_seconds() / 60, 1)} minutes",
                    "inline" : True
                },
                {
                    "name" : "Total games",
                    "value" : totalGames,
                    "inline" : True
                }
            ]
        }
        
    ]
    requests.post(url, json=data)
    return

