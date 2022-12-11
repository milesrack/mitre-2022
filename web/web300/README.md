# web300

## Description
The country of Ubetchaman is at it again. We heard one of their noobie hackers, hackerman, has been storing a bunch of stolen data on this terrible website. Show them your superior 1337 hacker skills and find a way in!

http://44.197.231.105:3023

## Solve
When clicking around on the pages I noticed a `?page=` parameter in the URL followed by the name of the page. This looked like it would be LFI (local file inclusion). The web server is taking this `page` parameter and outputing the contents of the file.

Lets try and grab the flag at http://44.197.231.105:3023/index.php?page=flag.txt

Nope! We need to look a little further.

Entering http://44.197.231.105:3023/index.php?page=../../../etc/passwd as the URL moves up into the root directory and int `/etc/passwd` showing us a list of users. The `hackerman` user looks interesting... lets see if his home directory has the flag.

Visiting http://44.197.231.105:3023/index.php?page=../../../home/hackerman/flag.txt gives us the flag.

## Flag
```
MCA{c20643d936f1c1b373c530b94ce224176d24d1de}
```