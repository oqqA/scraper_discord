import requests
import datetime
import json
import os

class ScraperDiscord(object):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.309 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36'
    api_version = 'v9'
    step_count = 50

    def __init__(self, token):
        self.__token = token

    def set_target(self, server_id, channel_id):
        self.server_id = server_id
        self.channel_id = channel_id

    def scraping_in_range(self, newer_timestamp, older_timestamp, template=None):
        return self.__scraping(
            newer_timestamp, 
            older_timestamp,
            template
        )
        
    def scraping_last(self, count_messages, template=None):
        newer_timestamp = datetime.datetime.now().timestamp()
        return self.__scraping(
            newer_timestamp, 
            count_messages=count_messages,
            template=template,
        )

    def scraping_all(self, template=None):
        newer_timestamp = datetime.datetime.now().timestamp()
        older_timestamp = datetime.datetime.strptime("01/01/2015", "%d/%m/%Y").timestamp()
        return self.__scraping(
            newer_timestamp, 
            older_timestamp,
            template
        )

    def __scraping(self, newer_timestamp, older_timestamp=None, template=None, count_messages=None):
        newer_snowflake = self.timestampToSnowflake(newer_timestamp)
        older_snowflake = self.timestampToSnowflake(older_timestamp) if older_timestamp is not None else newer_snowflake
        
        search = f'https://discord.com/api/{self.api_version}/channels/{self.channel_id}/messages?before={newer_snowflake}&limit={self.step_count}'

        headers = {
            'User-Agent': self.user_agent,
            'Authorization': self.__token,
            'Referer': f'https://discord.com/channels/{self.server_id}/{self.channel_id}'
        }

        res = []
        before = newer_snowflake

        while True:
            search = f'https://discord.com/api/{self.api_version}/channels/{self.channel_id}/messages?before={before}&limit={self.step_count}'

            data = requests.get(search, headers=headers)
            data = data.json()

            if len(data) > 0:
                before = int(data[-1]['id'])

            if older_timestamp is not None and before < older_snowflake:
                for i,v in enumerate(data):
                    if int(v['id']) < older_snowflake:
                        data = data[:i]
                        break

            if template is not None:
                data = ScraperDiscord.__selective_copying_json(data, template)
            
            res += data

            if count_messages is not None and count_messages > 0 and len(res) >= count_messages:
                res = res[:count_messages]
                break

            if older_timestamp is not None and before < older_snowflake:
                break

            if len(data) != self.step_count or len(data) == 0:
                break
        
        self.last_res = res

        return res

    def save(self, path_folder = "./data/"):
        if self.last_res is None: return
        if path_folder[-1] != '/': path_folder += '/'

        if not os.path.exists(path_folder):
            os.makedirs(path_folder)

        real_timestamp = int(datetime.datetime.now().timestamp())
        with open(f'{path_folder}{real_timestamp}_{len(self.last_res)}.json', 'w') as file:
            json.dump(self.last_res, file)

    @staticmethod
    def timestampToSnowflake(timestamp):
        return int(timestamp*1000-1420070400000) << 22

    @staticmethod
    def snowflakeToTimestamp(snowflake):
        return ((int(snowflake) >> 22) + 1420070400000)//1000

    @staticmethod
    def __selective_copying_json(data, template):
        res = None
        if isinstance(data, list) and isinstance(template, list):
            res = []
            for v in data:
                res.append(
                    ScraperDiscord.__selective_copying_json(v, template[0]))
        if isinstance(data, dict) and isinstance(template, dict):
            res = {}
            for k, v in template.items():
                if not k in data:
                    res.update({k: None})
                    continue
                if isinstance(v, list) or isinstance(v, dict):
                    res.update(
                        {k: ScraperDiscord.__selective_copying_json(data[k], v)})
                else:
                    res.update({k: data[k]})
        return res

__todo = '''

async def fetch(session, url):
    async with session.get(url) as response:
        resp = await response.json()
        return resp

async def fetch_all(cities):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city in cities:
            tasks.append(
                fetch(
                    session,
                    f"https://example.com/communes?kekw={city}",
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses
@timeit
def run(cities):
    responses = asyncio.run(fetch_all(cities))
    return responses

'''