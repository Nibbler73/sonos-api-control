import json
import os
import requests
import base64

# Sonos API with Postman
# https://developer.sonos.com/code/sonos-with-postman/
# Sonos API
# https://developer.sonos.com/reference/control-api/group-volume/set-volume/

def lambda_handler(event, context):

    # Authorize and get access_token
    client_auth_token = base64.b64encode( (os.environ["client_key"] + ':' + os.environ["client_secret"]).encode('utf-8') )
    auth_headers = {'Authorization' : 'Basic ' + client_auth_token.decode('utf-8'), 'Content-Type' : 'application/x-www-form-urlencoded'}
    #
    response = requests.post('https://api.sonos.com/login/v3/oauth/access', data = {'grant_type': 'refresh_token', 'refresh_token': os.environ["refresh_token"]}, headers=auth_headers)
    jsonObj = response.json()
    # get access_token
    access_token = jsonObj["access_token"]

    # Authorization Token
    my_headers = {'Authorization' : 'Bearer ' + access_token, 'Content-Type' : 'application/json'}
    #print("Access Token: " + access_token)

    #
    # Lookup Household
    response = requests.get('https://api.ws.sonos.com/control/api/v1/households', headers=my_headers)
    jsonObj = response.json()

    # my Household-ID
    household = jsonObj["households"][0]["id"]

    #
    # Lookup Player-IDs
    response = requests.get('https://api.ws.sonos.com/control/api/v1/households/' + household + '/groups', headers=my_headers)
    jsonObj = response.json()

    # My Groups
    groups = jsonObj["groups"]
    # Stop if already multiple groups
    if(len(groups) > 1):
        print ('more than one group, exiting')
        return {
            'statusCode': 200,
            'household': household,
            'groups' : groups,
            'abort-reason': 'more than one group, exiting'
        }
    for group in groups:
        groupId = group["id"]
        groupPlaybackState = group["playbackState"]

    # Stop if playing
    if (groupPlaybackState != 'PLAYBACK_STATE_PAUSED') and (groupPlaybackState != 'PLAYBACK_STATE_IDLE'):
        print ('the group is currently playing, exiting')
        return {
            'statusCode': 200,
            'household': household,
            'groups' : groups,
            'abort-reason': 'the group is currently playing, exiting'
        }

    # My players
    players = jsonObj["players"]
    playerIds = []
    random_player_id = None
    for player in players:
        playerIds.append(player["id"])
        if player["name"] == os.environ["main_player_name"]:
            random_player_id = player["id"]

    if random_player_id is None:
        random_player_id = playerIds[0]

    # remove main ID from player-list as it should stay in the group
    playerIds.remove(random_player_id)

    #
    # Set Group-Volume
    response = requests.post('https://api.ws.sonos.com/control/api/v1/groups/' + groupId + '/groupVolume', json = {"volume": "10"}, headers=my_headers)
    jsonObj = response.json()

    #
    # Kick out all players from the group
    my_group_request = {'playerIdsToRemove' : playerIds}
    response = requests.post('https://api.ws.sonos.com/control/api/v1/groups/' + groupId + '/groups/modifyGroupMembers', json = my_group_request, headers=my_headers)
    jsonObj = response.json()


    return {
        'statusCode': 200,
        'household': household,
        'groups' : groups,
        'my_group_request': my_group_request,
        'random_player_id': random_player_id,
        'groupId': groupId,
        'body': json.dumps(jsonObj)
    }


