# SliceBites

**Simple Pizza Ordering System**

- [SliceBites](#SliceBites)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
    - [Running Locally](#running-locally)
  - [Database](#database)
  - [Authors](#authors)


This is a pizza ordering system written in Django 3.1 (Only rest_framework) and python 3.8.5 on **Darwin based OS (MacOS Big Sur)**. It was never tested on any other OS. Major feature include following:

	* User can specify the desired flavors of pizza (margarita, marinara, salami), the number of pizzas and their size (small, medium, large). (Toppings and Sizes come from respective tables in database and needs to inserted into database beforehand, mock data can be setup later on)
	* Order contains info about customer, customer will be sent with order info and customer will be created or assigned accordingly.
	* It is possible to order same flavor in different sizes and quantity
	
	* All these info can be updated, order and order items are two separate tables so needs to be updated accordingly (read below in urls)
	* Order does contain status (pending, ready, dispatched, delivered)
	* Its possible to delete the order, and order items will be CASCADED

	* Retrieving order is also implemented (read below in urls) 
	* Listing orders will pull all orders except delivered ones, unless query param "delivered=true" is sent with order list. 
	* Orders can also be filtered by sending query parameter "status" with values "pending, ready, dispatched, delivered". 


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

* [Python 3.8.5](https://www.python.org/)
* [PostgreSQL](https://www.postgresql.org/download/)
  

### Installing

Clone or download the repository to your local machine.
Then run `conda create --name slicebites python=3.8` to create a conda environment called "slicebites" with the correct python version. The run `conda activate slicebites`. Since the requirements.txt is pip-syntaxed, run `pip install -r requirements.txt` after.

### Running Locally

To run a server run command `python manage.py runserver`. Server will start listening on port 8000 on localhost.


####  Urls:
##### ORDERS:

* To get all orders: http://127.0.0.1:8000/api/orders (GET)
* To create new order: [POST] http://127.0.0.1:8000/api/orders/ 
```
Sample JSON data to be sent:
{
    "id": 1,
    "customer": {
        "id": 1,
        "name": "test",
        "number": 976487387,
        "address": "test address of the user"
    },
    "status": "pending"
}
```

**Note**: Customer selection is automatic, if customer with this ID exist then order will be assigned to the customer, otherwise new customer will be created. 

* For order details: [GET] http://127.0.0.1:8000/api/orders/<order_id>
* To update order: [PUT] http://127.0.0.1:8000/api/orders/<order_id>/
* TO delete order: [DELETE] http://127.0.0.1:8000/api/orders/<order_id>/
* To get only Order Items: [GET] http://127.0.0.1:8000/api/<order_id>/order_items/

##### ORDER ITEMS:

* To get all order items: [GET] http://localhost:8000/api/order_item
* To add order item to an order: [POST] http://localhost:8000/api/order_item/
* Sample JSON Data to be sent:
```
{
	"order": 190,
    "size": {
        "id": 2,
        "name": "medium",
        "price": "12.00"
    },
    "topping": {
        "id": 1,
        "name": "marinara",
        "price": "2.00"
    },
    "quantity": 1,
    "notes": "medium order"
}
```
* To get order item details: [GET] http://localhost:8000/api/order_item/<order_item_id>
* To update order item details: [PUT] http://localhost:8000/api/order_item/<order_item_id>/


### Building the container manually

* Execute `docker build -t slicebites:\<buildnumber\> .` to build the container locally.


### Running the container (locally)

* Run Image: `docker run -p 5000:5000 divesolutions.azurecr.io/jellyfish:latest`

## Database

This app uses Postgres as default database, please use update `pizzeria.settings.py` to enter your database host, username, password, database name and port. Also if you want to use SQLite then change settings in DATABASES. 

If running in a container, by default it container sets database host to `host.docker.internal` which will point to postgres running in the host system. set following environment variables for database:
```
DB_HOST
DB_NAME
DB_PORT
DB_PW
DB_USER
```

Default set for container image:
```
ENV DB_HOST host.docker.internal
ENV DB_NAME postgres
ENV DB_PORT 5432
ENV DB_PW test
ENV DB_USER postgres

```

Default set for running locally without container image:
```
"DB_NAME": "postgres"
"DB_USER": "postgres"
"DB_PW": "test"
"DB_HOST": "localhost"
"DB_PORT": "5432"
```
## Authors

* **Kamran Ali** - *Masters Student* - [Hasso Plattner Institute, Potsdam Germany](kamran-ali@web.de)
