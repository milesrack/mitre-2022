# web150

# Description
Hmm, but how do I login?

http://3.238.30.178:3021

## Solve
The description already gives me the idea we will be dealing with SQL injection.

The source of the page has this comment:
```html
<!--Todo: Fix password exploit-->
```

Lets try a simple payload such as `' OR 1=1/*` for the username and password...

This evaluates the SQL query to true and we are authenticated!
## Flag
```
MCA{d005d44e20921ec979306bfb8bdc8a9eef459c8d}
```