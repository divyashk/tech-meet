# INSTRUCTIONS - 


### To run - 
```bash
docker-compose up --build --scale main=2 -d
```
The codebase right now is configured to run with the command shown above. 

Here we can vary the value of --scale flag from 'main=2' to any 'main=n' but then we also need to change then nginx.conf file. By default --scale main=2 will work.

In order to change the number of frontend server to something other than 2, we need to add the address of the newly created frontend servers in the load balancing part of nginx.conf as follows -

Finding the newly created load balancing server addresses 
```
docker ps --format '{{.Names}}'
```

The names of these containers act as addresses in docker's own network, and can therefore be added in to the nginx conf file ( as nginx is itself a docker container )

```
events {}
# Define which servers to include in the load balancing scheme.
http {
    upstream app {
        server main:5000;
#       server <add the address of new server here>:5000;
#       ...
    }
    # This server accepts all traffic to port 80 and passes it to the upstream.
    server {
            listen 80;
            server_name app.com;
            location / {
                proxy_pass http://app;
            }
        }
}
```
