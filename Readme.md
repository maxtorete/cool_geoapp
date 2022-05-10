# Cool GeoAPP

Developer: Juan Francisco Fernández Rodríguez

## Assumptions and decisions
Ideally, we should have some deep conversation with stakeholders and business people about how to model our app domain.
But this is the real world, so let's assume this test's requirements come from a well known client that needs an instant
implementation for their mockups, and yet we are devoted to providing an efficient and sustainable solution in return.

Our client will provide us a new csv fileset to update data, so we will create the schema and import current csv content
on the service's boot time. We will use a Python script executed with a command in a Dockerfile. The updating process
will consist in a new instance deployment from the latest repo code.

Users will be provided too, so they will be imported during boot time as well. 
We will protect the application with a JWT based validating system using a third party library.

As the calculations are not so heavy, the team decided to move them to frontend, reducing the number of petitions to the
backend and the size of transferred bits.


## Frontend description
The frontend client will be responsible for getting, transforming and representing the data obtained from our REST API.

Main map widget needs one resource ```postal_code``` and a subresource ```paystat_aggregate```. 
With a GET request to the collection URL (```/postal_code```), we will get the list of zip codes with their geometry to draw 
them and their aggregated total turnover to apply the corresponding color. On a user click on the map, the client will 
send a request to the resource item URL (```/postal_code/<id>/paystat_aggregate```). 
If the response is a success, then a tooltip with the turnover by ages will be shown as in the mockup.
Both request data will be saved in the component's state so no new request will be sent on component rerendering 
or if the user clicks again on the same zip code area.

For every widget in the left bar we can use the same dataset as the required for the Time Series one. 
With the help of an App State Container system, like Redux, we can ensure that the data will be consistent on all 
of them. On component loads, if the state variable for our data is empty, our client will send a GET request to 
resource ```monthly_paystat_report``` collection endpoint (```/paystat_monthly_report```). 
We will use a isLoading flag on the store state variable to avoid duplicating initial requests.

Each component will be subscribed to that piece of state in the container, so if there is any change on it, the 
component will apply the needed logic to transform the new data, will save it on its own component's state to avoid 
recalculating it and will rerender accordingly.

Any change on the time frame selected by the user will invalidate all the APP and components state.

## Application Architecture

GeoAPP is split on two main layers, a high level ```domain``` layer and a low level ```application``` one. During next
sections both will be described briefly.

### Domain

It contains all the logic related to our business domain. It is free of any external dependency besides some core
language functions. Dependency inversion, through the Port/Adapter pattern, was used to protect our domain from external 
dependencies while providing an API to access advanced features from framework and libraries.

### Application

This layer makes use of all the power and advantages of frameworks and libraries. Domain's abstractions are implemented
in the adapter directory together with their related classes. Database access complies with no ORM requirement, 
so expect some quirks there :-). Flask-Caching SimpleCache is used to cache API responses.

## Deployment and execution

Docker and docker-compose are a requisite to run the GeoAPP service. You will need an internet connection too. To avoid
running the service as root, you can configure docker or even better, use safer implementations as podman.

### Instructions

Get the app:

```
git clone https://github.com/maxtorete/cool_geoapp.git
```

Run the service:

```
cd cool_geoapp
sudo docker-compose up
```

### Example requests

Get an authentication token:

```
curl --location --request POST 'http://127.0.0.1:5000/login' --header 'Content-type: application/json' --data-raw '{"username":"manuel_nogueira","password":"realsecretpassword"}'
```

Replace ```REPLACE_JWT``` with token get on previous request in next requests.

Get postal code listing:

```
curl --location --request GET 'http://127.0.0.1:5000/postal_code?date_from=2015-01-01&date_to=2015-12-31' \
--header 'Authorization: Bearer REPLACE_JWT'
```

Get paystat aggregate for postal code:

```
curl --location --request GET 'http://127.0.0.1:5000/postal_code/6055/paystat_aggregate?date_from=2015-01-01&date_to=2015-12-31' \
--header 'Authorization: Bearer REPLACE_JWT'
```

Get paystats monthly aggregates:

```
curl --location --request GET 'http://127.0.0.1:5000/paystat_monthly_report?date_from=2015-01-01&date_to=2015-12-31' \
--header 'Authorization: Bearer REPLACE_JWT'
```


## Next steps

1. Use environment variables for database connection and secret keys
2. Replace postal_code id with postal_code code on url parameters
3. Implement tests for domain and application layer
4. Enhance error handling in endpoints 
5. Implement a Redis or similar cache system

