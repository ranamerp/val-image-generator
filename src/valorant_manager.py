#from valclient.client import Client 
import os, json, datetime, requests

from .content_loader import Loader

class Valorant:

    cur_path = os.path.dirname(__file__)
    #file_path = os.path.join(cur_path,"../match_reference.json")

    # def __init__(self):
    #     self.client = Client(region="na") 
    #     self.client.activate()
    #     self.content = Loader.load_all_content(self.client)

    def load_match_data(self, match_data):
        
        # tags = player_tag.split('#')
        # name = tags[0]
        # tag = tags[1]
        # matchapiv3 = f'https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}' 
        
        # match = requests.get(matchapiv3)
        # match_data = match.json()
        
        #For now taking last map, but should set this up to be whatever map out of last 5 is chosen
        #match_data = match_data['data'][0]
        #match_data = self.client.fetch_match_details(match_id)
        
        # with open("match_reference.json", "w") as f:
        #     f.write(json.dumps(match_data))
        
        #total_rounds = len(match_data["roundResults"])
        #total_rounds = match_data['metadata']['rounds_played']
        total_rounds = len(match_data['rounds'])
        

        firstkills = {}
        currentRound = -1

        for kill in match_data['kills']:
            itemRound = kill['round']
            if currentRound == itemRound:
                continue
            killer = kill['killer']['puuid']
            if killer in firstkills:
                firstkills[killer] += 1 
            else:
                firstkills[killer] = 1
            currentRound += 1

        if match_data["metadata"]["queue"]['id'] != "Deathmatch":
            payload = {
                "match_id": match_data["metadata"]["match_id"],
                "match_map_display_name": match_data["metadata"]["map"]['name'],
                "match_mode": match_data["metadata"]["queue"]['name'],
                #"timestamp": datetime.datetime.fromtimestamp(match_data["metadata"]["game_start"]//1000).strftime('%m/%d/%Y %H:%M:%S'),
                "timestamp": match_data['metadata']['started_at'],
                #"match_mode_display_name": self.content["queue_aliases"][match_data["matchInfo"]["queueID"]],
                #"match_map_display_name": [gmap for gmap in self.content["maps"] if match_data["matchInfo"]["mapId"] in gmap["path"]][0]["display_name"],
                "teams": [
                    {
                        "team_name": team['team_id'],
                        "team_alias": "ATK" if team['team_id'] == "Red" else "DEF",
                        "won_bool": team["won"],
                        "won": "WIN" if team["won"] else "LOSS",
                        "rounds_won": team["rounds"]['won'],
                    } for team in match_data["teams"]
                ],
                "players": [
                    [
                        {
                            "puuid": player["puuid"],
                            "display_name": player["name"],
                            "team_id": player["team_id"],
                            "agent_display_name": "kayo" if player["agent"]['name'].lower() == "kay/o" else player["agent"]['name'].lower(),
                            #"agent_display_name": [agent for agent in self.content["agents"] if player["characterId"] in agent["uuid"]][0]["display_name"],
                            "kd": str(round(player["stats"]["kills"] / (player["stats"]["deaths"] if player["stats"]["deaths"] != 0 else 1),1)),
                            "kills": player["stats"]["kills"],
                            "first_kills": 0 if player['puuid'] not in firstkills else firstkills[player["puuid"]],
                            "deaths": player["stats"]["deaths"],
                            "combat_score": player["stats"]["score"] // total_rounds,
                            "won_bool": team["won"],
                        } for player in match_data["players"] if player['team_id'] == team['team_id']
                    ] for team in match_data["teams"]
                ],
            }
        
        
            # sort players by combat score
            payload["players"] = [sorted(team, key=lambda k: k["combat_score"], reverse=True) for team in payload["players"]]

            # sort teams by red/blue
            backup = payload["teams"].copy()

            team_blue = [team for team in backup if team["team_name"] == "Blue"]
            team_red = [team for team in backup if team["team_name"] == "Red"]
            payload["teams"] = [team_red[0],team_blue[0]]
            #payload["teams"] = [team_blue[0], team_red[0]]



        

        #print(payload)
        return payload