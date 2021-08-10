# AutoSpotify
# TODO:
    - [ ] Create a friendlier auth process, maybe use Oauth and redirect as in termcal?
    - [ ] Provide interface to enter artists names
        - search bar 
        - web app 
        - terminal func
        - desktop app (does it even make sense?)

* secrets.json contains json object with the following strcture:
 secrets = {"config:{
    "client_id": "here goes your user id",
    "client_secret": "here goes client secret",
    "access_token" : "here goes access token",
    "refresh_token" : "here goes refresh token"
 }, "artists":
    [artists_names]
    }
* web-api-auth-example https://github.com/spotify/web-api-auth-examples
