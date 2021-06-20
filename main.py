import json
import os
import datetime
from scraper_discord import ScraperDiscord
from dotenv import load_dotenv, find_dotenv 

load_dotenv(find_dotenv())

server_id = 357480372084408322
channel_id = 370840938739925003
secret_jwt_token = os.environ.get("TOKEN")
template = [
    {
        'id': 0,
        'content': 0,
        'author': {
            'username': 0,
        },
        'attachments': [
            {
                'filename': 0,
                'size': 0,
                'content_type': 0
            }
        ],
        'edited_timestamp': 0,
        'reactions': [
            {
                'emoji': {
                    'id': 0,
                    'name': 0
                },
                'count': 0
            }
        ]
    }
]

# Init

scraper = ScraperDiscord(secret_jwt_token)
scraper.set_target(server_id, channel_id)

# Example 1

res = scraper.scraping_last(3, template)
print(f"Count: {len(res)}")
scraper.save()

# Example 2

older_timestamp = datetime.datetime.strptime("19/06/2021", "%d/%m/%Y").timestamp()
newer_timestamp = older_timestamp+60*60*10
#res = scraper.scraping_in_range(newer_timestamp, older_timestamp, template)
#print(f"Count: {len(res)}")
#scraper.save()

# Example 3 

#res = scraper.scraping_all()