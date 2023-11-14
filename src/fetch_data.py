import requests
from os import listdir
from os.path import isfile, join
import sys

from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

def fetch_images(data_type:str)->None:
    url={}
    path = f'.\\data\\{data_type}s'
    if data_type == 'agent':
        response = requests.get('https://valorant-api.com/v1/agents')
        path += '\\full_image'
        for _ in response.json()['data']:
            if _['role'] is None:
                continue
            url[_["displayName"].lower().replace('/', '')] = {
                "full_image": _['fullPortrait'], 
                "headshot":_['displayIcon'],
                "role": _['role']["displayIcon"]
    }
            
    elif data_type == 'map':
        response = requests.get('https://valorant-api.com/v1/maps')
        for _ in response.json()['data']:
            url[_['displayName'].lower()] = _['splash']
        del url['the range']


    old = [_.replace('agent_', '').replace('map_', '').replace('.png', '') for _ in [f for f in listdir(path) if isfile(join(path, f))]]
    new = list(set(url.keys()) - set(old))
    path = f'.\\data\\{data_type}s'
    if new:
        download(new, data_type, path, url)
    else:
        sys.stdout.write(f'No new {data_type} image need to be downloaded\r')
        sys.stdout.flush()


def download(new:list, data_type:str, path:str, url:dict)->None:
    for i, _ in enumerate(new):
        progress(i, len(new), suffix=f' Downloading new {data_type} image: {_}')
        if len(url[_]) == 3:
            for name, item in url[_].items():
                response = requests.get(item, timeout=30)
                finalpath = f'{path}\\{name}\\{data_type}_{_}.png'
        else:
            response = requests.get(url[_], timeout=30)
            finalpath = f'{path}\\{data_type}_{_}.png'

        with open(finalpath, 'wb') as f:
            f.write(response.content)

def fetch_matches(mgr, content) -> list:
    matches = mgr.client.fetch_match_history()["History"]
    choices = [Choice("custom", "use my own match id"), Separator()]
    for i, match in enumerate(matches):
        match_data = mgr.client.fetch_match_details(match["MatchID"])

        me = next(player for player in match_data["players"] if player["subject"] == mgr.client.puuid)
        my_team = next(team for team in match_data["teams"] if team["teamId"] == me["teamId"])
        other_team = next(team for team in match_data["teams"] if team["teamId"] != me["teamId"])

        queue = match_data["matchInfo"]["queueID"]
        if queue == " " or queue == "":
            queue = "custom"
        match_id = match_data["matchInfo"]["matchId"]
        score = f"{my_team['roundsWon']}-{other_team['roundsWon']}"

        agent = next(agent for agent in content["agents"] if agent["uuid"] == me["characterId"])
        agent = agent["display_name"]

        string = f"[{score}] {queue} - {agent} ({match_id})"
        choices.append(Choice(match_id, string))

        progress(i, len(matches), suffix=f' Fetching recent matches')
    return choices


def progress(count, total, suffix=''):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percents, '%', suffix + ' '*20))
    sys.stdout.flush()

if __name__ == '__main__':
    fetch_images('agent')
    fetch_images('map')
