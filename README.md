# LocationBot

## What this is

A quite simple Discord Bot I made before going on a bike trip with a friend. I wanted to be able to track our location but I didn't have a lot of time to setup something like [Hauk](https://github.com/bilde2910/Hauk), which is very cool but a bit more complicated to setup.

It fits my needs for now, it may evolve in the future, who knows ? As of now, you can use it until Heroku drops its free plan (November 2022 IIRC).

Be aware that I use a JSON file to store all data : it's extremely bad practice, unsecure, unethical and probably forbidden in several religions. Please don't sue me.

## Usage

`/storeloc 47.213921046474745, -1.5551546403457128`

Stores a location (lon/lat) to a .json file with your discord UID

`/getloc <User> `

Generates a Google Maps URL using the locations stored by the User (must be present in your server) : 
 - A single location will show the designated coordinates
 - Two locations will show directions between them
 - Every location between the first and the last stored will be added as waypoints

`/purge`

Remove every location stored by you

## URL

[Add him to your server](https://discord.com/api/oauth2/authorize?client_id=1024794133195399288&permissions=2048&scope=bot)