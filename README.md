# MuSearch

-To run, go to terminal and run the command:

$python app.py

# Introduction:

This API allows you to perform searches for artists and songs on Twitter, Wikipedia, and Spotify. It can also show you a list of an artist's most popular tracks according to Spotify. Each method is accessible by a different endpoint.

**GET /twitter/<keyword>**
Get latest tweets about the keyword

Request parameters

| Request Parameter | Value Type | Value               |
|-------------------|------------|---------------------|
| URL ending        | String     | Artist or Song name |

Response  
This method returns a JSON object containing the following

| Reponse | Value Type | Value                                |
|---------|------------|--------------------------------------|
| Data    | List[]     | Latest tweets containing the keyword |

**GET /wikipedia/<keyword>**
Get the recommended Wikipedia article that corresponds to the keyword

Request parameters
| Request Parameter | Value Type | Value               |
|-------------------|------------|---------------------|
| URL ending        | String     | Artist or Song name |

Response  
This method returns a JSON object containing the following

| Reponse | Value Type | Value                               |
|---------|------------|-------------------------------------|
| Data    | String     | First section of the Wikipedia page |

**GET /spotify/artist/<keyword>**
Get the name and ID of the artist corresponding to the search keyword

Request parameters

| Request Parameter | Value Type | Value       |
|-------------------|------------|-------------|
| URL ending        | String     | Artist name |

Response  
This method returns a JSON object containing the following

| Reponse | Value Type | Value              |
|---------|------------|--------------------|
| Data    | String     | Artist name and ID |

**GET /spotify/artist/<keyword>**
Get the name and ID of the artist corresponding to the search keyword

Request parameters

| Request Parameter | Value Type | Value     |
|-------------------|------------|-----------|
| URL ending        | String     | Song name |

Response
This method returns a JSON object containing the following

| Reponse | Value Type | Value              |
|---------|------------|--------------------|
| Data    | String     | Artist name and ID |

**GET /spotify/playlist/<artist_id>**
Get the top ten tracks from a specific artist

Request parameters

| Request Parameter | Value Type | Value     |
|-------------------|------------|-----------|
| URL ending        | String     | Artist ID |

Response  
This method returns a JSON object containing the following

| Reponse | Value Type | Value              |
|---------|------------|--------------------|
| Data    | List[]     | Top ten song names |
