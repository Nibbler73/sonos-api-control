import json
import os
import requests
import base64

# Sonos API with Postman
# https://developer.sonos.com/code/sonos-with-postman/
# Sonos API
# https://developer.sonos.com/reference/control-api/group-volume/set-volume/

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

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
    main_group_id = None
    for group in groups:
        if group["name"] == os.environ["main_player_name"]:
            main_group_id = group["id"]
    if main_group_id is None:
        main_group_id = groups[0]["id"]

    # My players
    players = jsonObj["players"]
    playerIds = []
    for player in players:
        playerIds.append(player["id"])

    #
    # Create a Group with all Players
    my_group_request = {'playerIds' : playerIds, 'musicContextGroupId' : main_group_id}
    response = requests.post('https://api.ws.sonos.com/control/api/v1/households/' + household + '/groups/createGroup', json = my_group_request, headers=my_headers)
    #dump( response )
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
        'main_group_id': main_group_id,
        'new_group_id': new_group_id,
        'body': json.dumps(jsonObj)
    }


