# Using SiteFab with Nginx

## Nginx installation

### OSX

1. update brew:

``` 
brew update
```

2. installing Nginx

```
brew install nginx
```

##  Configuring Nginx

This guide only covers the part of the configuration you need to run your site with pretty print URLs. There are a lot of other configuration
variables you should take care of that are outside of this guide as there are plenty of ressources for it (e.g HTTPS, HTTP2, Compression and Caching).

### Edit configuration.
OSX location: **/usr/local/etc/nginx/nginx.conf**
Replace the server block by the following configuration and make sure that **root** is pointing to where the site is (release directory)
```
    server {
        listen       8080;
        server_name  localhost;
	    rewrite ^(/.*)\.html(\?.*)?$ $1$2 permanent; 
	    rewrite ^/(.*)/$ /$1 permanent;
      	try_files $uri/index.html $uri.html $uri/ $uri =404; 

        root   /Users/elie/Sites/elie/generated/;
        index  index.html index.htm;
		    
    }
```

#### making pretty print urls working
To make pretty URL works the server configuation need to be changed to add in the server or location block:
```
        rewrite ^(/.*)\.html(\?.*)?$ $1$2 permanent; 
	    rewrite ^/(.*)/$ /$1 permanent;
      	try_files $uri/index.html $uri.html $uri/ $uri =404; 
```

### Launching Nginx
Simple Launch
```
nginx
```
Launching at startup
```
brew services start nginx
```

## Firewall
Firewall allow:
```
ufw allow 'Nginx Full'
```

Verify it works
```
systemctl status nginx
```


## Nginx useful commands

Reloading nginx:
```
nginx -s reload
```

Stop:
```
nginx -s quit
```