# Install Nginx
## OSX
1. update brew:
``` 
brew update
```

2. install Nginx
```
brew install nginx
```

#  Configure Nginx

## Dev version
### Edit configuration.
OSX location: **/usr/local/etc/nginx/nginx.conf**
Replace the server block by 
```
    server {
        listen       8080;
        server_name  localhost;
	    rewrite ^(/.*)\.html(\?.*)?$ $1$2 permanent; 
	    rewrite ^/(.*)/$ /$1 permanent;
      	try_files $uri/index.html $uri.html $uri/ $uri =404; 

        root   /Users/elie/Sites/elie/;
        index  index.html index.htm;
		    
    }
```

make sure that **root** is pointing to where the site is.


### Launching Nginx
Simple Launch
```
nginx
```
Launching at startup
```
brew services start nginx
```

# Prod install
Firewall allow:
```
ufw allow 'Nginx Full'
```

Verify it works
```
systemctl status nginx
```


# Useful commands

Reloading nginx:
```
nginx -s reload
```

Stop:
```
nginx -s quit
```

# Configuration detail
To make pretty URL works the server configuation need to be changed to add in the server or location block:
```
        rewrite ^(/.*)\.html(\?.*)?$ $1$2 permanent; 
	    rewrite ^/(.*)/$ /$1 permanent;
      	try_files $uri/index.html $uri.html $uri/ $uri =404; 
```
