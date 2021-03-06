from RiotAPI import RiotAPI
import json
import operator

def main():
    api = RiotAPI('e6e27f9f-d47d-4b3f-96d4-3aab2c2b8cee')
    champs = 10
    data_dict = {}
    champList = []
    second_dict = {}
    champIdizzle = 11
    structured_data = {}
    champion_name = {}
       
    # Get summoner data
    summoner_response = api.get_summoner_by_name('KmancXC')
    
    # Parse the output
    temp = json.dumps(summoner_response)
    temp = json.loads(temp)
    summoner_id = (temp['kmancxc']['id'])
    summoner_name = (temp['kmancxc']['name'])
    
    # For troubleshooting
    #print (summoner_id, summoner_name)
    
    # Get all of a summoner's mastery data
    #response = api.get_summoner_mastery_data(summoner_id)
    #print (response)
    
    # Get a summoner's top X mastery data
    mastery_response = api.get_top_mastery_data(summoner_id, champs)
    
    # Compile the stuff I care about into a dictionary
    for x, val in enumerate(mastery_response):
        data_dict[val['championId']] = val['championPoints']
    
    # Find out what lane the champion is being played in
    for key in data_dict:
        champList.append(key)
        #structured_data[summoner_id][key].append()
    lane_response = api.get_champion_role(summoner_id, champList)
    
    # Figure out what roles the champion is being played in, and for how many games
    for x, val in enumerate(lane_response['matches']):
        key_test = val['champion']
        if (val['lane'] == 'BOTTOM'):
            role = val['role']
        else:
            role = val['lane']
        if key_test not in second_dict:
            second_dict[key_test] = {}
            second_dict[key_test][role] = 0
        else:
            if role in second_dict[key_test]:
                second_dict[key_test][role] += 1
            else:
                second_dict[key_test][role] = 0
                
    # Get percentage of games played in each role per champIdizzle
    for id_key in second_dict:
        role_games = 0
        for role_key in second_dict[id_key]:
            role_games += second_dict[id_key][role_key]
        for role_key in second_dict[id_key]:
            second_dict[id_key][role_key] /= role_games
        #print (second_dict[id_key]['lane'])
          
    #combined_dict = {}
    #for key in (data_dict.keys() | second_dict.keys()):
    #    if key in data_dict: combined_dict.setdefault(key, []).append(data_dict[key])
    #    if key in second_dict: combined_dict.setdefault(key, []).append(second_dict[key])
    
    # Get the champion name for later use
    for champIdizzle in data_dict:
        champion_response = api.get_champion_name(champIdizzle)
        champion_name[champIdizzle] = (champion_response['name'])
        
    # Put summoner id as a first level key
    structured_data[summoner_id] = {}
    
    # Put champion id as a second level key, with the name and another dictionary as the value
    for champion_id in champion_name:
        structured_data[summoner_id][champion_id] = [champion_name[champion_id]]
        
    # Put role as a third level key with mastery points * percentage of games in that role as the value
    for second_champ_id, data_champ_id in zip(second_dict, data_dict):
        for role_key in second_dict[second_champ_id]:
            structured_data[summoner_id][second_champ_id].append({'role goes here': 
                                                second_dict[second_champ_id][role_key] * data_dict[data_champ_id]})
    
    print (structured_data)
    #print (data_dict)
    #print ()
    #print (second_dict)
    
if __name__ == '__main__':
    main()