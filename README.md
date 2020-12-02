# Django-Pizza_App_REST_API
This is solution for assignment given by moberries  made using Django,Django REST Framework(DRF),Docker and Test Driven Develoment(TDD).

## Some of the features of this API/project are :~

* Setup the project using Docker.

* Used PostgreSQL database.

* Two model created for storeing information about pizza and order.

* For customer information default django user model is used.

* User can order pizza with desired flavor and size.

* user can track order information.

* Order status only can be changed when it is not delivered.

* List, retrive and removing functionality added.

* Added listing and filtering by customer and delivery status.

* Followed Test Driven Development(TDD).


## How to setup and run this api

* As i have setup the project using Docker so there is not much difficulty on how to set up the project, make sure you have Docker installed on your system.


* Just go the project directory and enter command :~`docker-compose up -d --build `  This will build the docker image used to run the project.


* All tests should pass and then we can start the server using simply :~ `sudo docker-compose up`

* Once the server starts go to `http://127.0.0.1:8000/` for api endpoints.

* you can test using `docker-compose exec server python manage.py test orders` command.
