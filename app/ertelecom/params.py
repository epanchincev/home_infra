BASE_URL = 'https://myhome.proptech.ru'
AUTH_URL = BASE_URL + '/auth/v2/auth/720010149038/password'
AUTH_BODY = {
    'login': '720010149038',
    'timestamp': '2024-01-31T08:03:18.717Z',
    'hash1': 'KJ/qkGuaTIQDg4SjmZ8I60C3X8Y=',
    'hash2': '318b9c706d5b4e9d3c1aa47771b6e427'
}
AUTH_HEADERS = {
    "authorization": "Bearer uwxzq88x5yqbw20ex2wcjxsqb5tet7"
}
REST_URL = BASE_URL + '/rest'
ACCESSCONTROLS_URL = REST_URL + '/v1/places/3778773/accesscontrols/'
OPEN_DOOR_URL = ACCESSCONTROLS_URL + '{}/actions'
OPEN_DOOR_BODY = "accessControlOpen"
SNAPSHOT_URL = ACCESSCONTROLS_URL + '{}/videosnapshots'
GET_VIDEO_LINK_URL = REST_URL + '/v1/forpost/cameras/{}/video?LightStream=0'
