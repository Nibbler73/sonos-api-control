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

    # My players
    players = jsonObj["players"]
    playerIds = []
    for player in players:
        playerIds.append(player["id"])

    #
    # Create a Group with all Players
    my_group_request = {'playerIds' : playerIds}
    random_player_id = playerIds[0]
    response = requests.post('https://api.ws.sonos.com/control/api/v1/households/' + household + '/groups/createGroup', json = my_group_request, headers=my_headers)
    jsonObj = response.json()

    # my new Group's ID
    new_group_id = jsonObj["group"]["id"]

    #
    # Set Group-Volume
    response = requests.post('https://api.ws.sonos.com/control/api/v1/groups/' + new_group_id + '/groupVolume', json = {"volume": "10"}, headers=my_headers)
    jsonObj = response.json()

    return {
        'statusCode': 200,
        'household': household,
        'my_group_request': my_group_request,
        'random_player_id': random_player_id,
        'new_group_id': new_group_id,
        'body': json.dumps(jsonObj)
    }

