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

## Microservices and APIs

#### Appointments Microservice 

1. `/appointments/book_appointment` : POST request made by a patient. Accepts data for creating an appointment and creates a new appointment document in the appointments collection
2. `/appointments/show_appointments` : POST request made either by patient or doctor. Shows all the active and pass appointments, and sends the data as json
3. `/appointments/close_appointment` : POST request made by the doctor who sends his inputs on the appointment and then adds the prescription and description to the database 

#### Authentication Microservice 

1. `/authentication/username` : POST request made by any user. Checks if the username exists in the database or not
2. `/authentication/create_account` : POST request made by user to create a new user in the database
3. `/authentication/login` : POST request which accepts username and password, hashes the password and matches it in the database and then returns data.

#### Inventory Microservice 

1. `/inventory/medicines` : GET request which returns all the possible medicines and their descriptions
2. `/hospital/<hosp_id>/getall` : Accepts hospital id and returns details of all the doctors associated with that hospital
3. `/inventory/hospital/:hosp_id/getall` : POST request which accepts hospital id and returns all details of the doctors and their slots


 
