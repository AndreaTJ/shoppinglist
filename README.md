# Shopping list web application

## Brief
The objectiv of this project is to create a web application in python that has functionality to create, read update and delete information.

## Project
in order to do this I have decided to create ana pplicaiton that will store shoppoing list, this will have a user model that allows users to login and view lists that have been create previously.

### Backend
in order to sore the information in the shopping list I have created three mySQL databases these are related as according to the following ERD diagram:

![ERD](images/ERD_diagram.draw.io.png)

the master table has been implemented to allow the app to query a database that contains both the user_id and the item_id this makes it possible to return only the items asscoiated with the suer that is currently logged in
