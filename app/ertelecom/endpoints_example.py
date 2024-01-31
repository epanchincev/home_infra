AUTH_POST = "https://myhome.proptech.ru/auth/v2/auth/720010149038/password"
AUTH_POST_BODY = {
    "login": "720010149038",
    "timestamp": "2024-01-31T08:03:18.717Z",
    "hash1": "KJ/qkGuaTIQDg4SjmZ8I60C3X8Y=",
    "hash2": "318b9c706d5b4e9d3c1aa47771b6e427"
}
AUTH_POST_RESPONSE = {
    "operatorId": 40,
    "operatorName": "Тюмень",
    "tokenType": "Bearer",
    "accessToken": "uwxzq88x5yqbw20ex2wcjxsqb5tet7",
    "expiresIn": None,
    "refreshToken": "000000e4-08fc69d0-8c22-38f3-e063-0d0a020ae07e",
    "refreshExpiresIn": None
}


AUTH_HEADERS = {
    "authorization": "Bearer uwxzq88x5yqbw20ex2wcjxsqb5tet7"
}

GET_PLACE_URL = "https://myhome.proptech.ru/rest/v3/subscriber-places"
ANSWER_PLACE = {
    "data": [
        {
            "id": 2045436,
            "subscriberType": "owner",
            "subscriberState": "out",
            "place": {
                "id": 3778773,
                "address": {
                    "index": None,
                    "region": None,
                    "district": None,
                    "city": "Тюмень",
                    "locality": None,
                    "street": "краснооктябрьская ул",
                    "house": "14",
                    "building": None,
                    "apartment": "266",
                    "visibleAddress": "краснооктябрьская ул, д. 14, кв. 266",
                    "groupName": "Тюмень"
                },
                "location": {
                    "longitude": 65.521958,
                    "latitude": 57.1855
                },
                "autoArmingState": False,
                "autoArmingRadius": 50
            },
            "subscriber": {
                "id": 1389314,
                "name": "Епанчинцев Алексей Сергеевич",
                "accountId": "720010149038",
                "nickName": None
            },
            "guardCallOut": None,
            "payment": {
                "useLink": True
            },
            "blocked": None,
            "provider": "ERTH"
        }
    ]
}

GET_CAMERAS_URL = 'https://myhome.proptech.ru/rest/v1/places/3778773/cameras'
GET_ACCESSCONTROLS_URL = 'https://myhome.proptech.ru/rest/v1/places/3778773/accesscontrols'
ACCESS = {
    "data": [
        {
            "id": 29884,
            "operatorId": 40,
            "name": "Шлагбаум 1 - Краснооктябрьская 14",
            "forpostGroupId": "2528353",
            "forpostAccountId": None,
            "type": "BUP",
            "allowOpen": True,
            "openMethod": "ACCESS_CONTROL",
            "allowVideo": True,
            "allowCallMobile": False,
            "allowSlideshow": False,
            "previewAvailable": True,
            "videoDownloadAvailable": True,
            "timeZone": 18000,
            "quota": 604800,
            "externalCameraId": "73105585",
            "externalDeviceId": None,
            "entrances": []
        },
        {
            "id": 36934,
            "operatorId": 40,
            "name": "Краснооктябрьская Ул 14  (п. 4)",
            "forpostGroupId": "5030365",
            "forpostAccountId": None,
            "type": "SIP",
            "allowOpen": True,
            "openMethod": "ACCESS_CONTROL",
            "allowVideo": True,
            "allowCallMobile": True,
            "allowSlideshow": True,
            "previewAvailable": True,
            "videoDownloadAvailable": True,
            "timeZone": 18000,
            "quota": 604800,
            "externalCameraId": "73105645",
            "externalDeviceId": None,
            "entrances": []
        },
        {
            "id": 26981,
            "operatorId": 40,
            "name": "Калитка 2 - Краснооктябрьская 14",
            "forpostGroupId": "1638903",
            "forpostAccountId": None,
            "type": "SIP",
            "allowOpen": True,
            "openMethod": "ACCESS_CONTROL",
            "allowVideo": True,
            "allowCallMobile": True,
            "allowSlideshow": True,
            "previewAvailable": True,
            "videoDownloadAvailable": True,
            "timeZone": 18000,
            "quota": 604800,
            "externalCameraId": "73105657",
            "externalDeviceId": None,
            "entrances": []
        },
        {
            "id": 37197,
            "operatorId": 40,
            "name": "Калитка 3 - Краснооктябрьская 14",
            "forpostGroupId": "5109331",
            "forpostAccountId": None,
            "type": "SIP",
            "allowOpen": True,
            "openMethod": "ACCESS_CONTROL",
            "allowVideo": True,
            "allowCallMobile": True,
            "allowSlideshow": True,
            "previewAvailable": True,
            "videoDownloadAvailable": True,
            "timeZone": 18000,
            "quota": 604800,
            "externalCameraId": "73105633",
            "externalDeviceId": None,
            "entrances": []
        },
        {
            "id": 26980,
            "operatorId": 40,
            "name": "Калитка 1 - Краснооктябрьская 14",
            "forpostGroupId": "1638793",
            "forpostAccountId": None,
            "type": "SIP",
            "allowOpen": True,
            "openMethod": "ACCESS_CONTROL",
            "allowVideo": True,
            "allowCallMobile": True,
            "allowSlideshow": True,
            "previewAvailable": True,
            "videoDownloadAvailable": True,
            "timeZone": 18000,
            "quota": 604800,
            "externalCameraId": "73105649",
            "externalDeviceId": None,
            "entrances": []
        }
    ]
}
GET_SNAPSHOT_URL = "https://myhome.proptech.ru/rest/v1/places/3778773/accesscontrols/26980/videosnapshots"

POST_OPEN_DOOR_URL = "https://myhome.proptech.ru/rest/v1/places/3778773/accesscontrols/26980/actions"
POST_OPEN_DOOR_BODY = "accessControlOpen"
OPEN_DOOR_ANSWER = {    
    "data": {
        "status": True,
        "errorCode": None,
        "errorMessage": None
    }
}



AUTH_TOKEN = 'uwxzq88x5yqbw20ex2wcjxsqb5tet7'
