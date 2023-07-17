# Messaging system - Abra 

- [Description](#Description)
- [Guide](#Guide)
- [File Structure](#File-Structure)
- [Final Project](#Final)
    

    
### Description

The goal of this task is to develop a backend system with REST API that manages the exchange of messages among users.
<br>
The system will handle various operations such as sending, receiving, and managing messages between users.

<br>

### Guide


### To run the project, we'll perform the following actions:



1. First of all - we'll download PostgreSQL version 15 if it's not installed on the computer:

    ```
   Link: 
   
    https://www.postgresql.org/download/
    ```
   <br>

2. Open the PgAdmin to create and connect to the DB

    <br>

3. We'll open the Postman collection that I added in the project, to make it easier to send requests
    <br> <br>
4. To run the project, open the IDE, go to the path of the manage.py file and write the command:

    ```
    python manage.py runserver
    ```
    We write this command to bring the server live.
   
   <br>
5. Now we'll create superuser in the Django admin panel

   * By Django's Admin interface
   There is a tab named user, next to it there is a + sign, click on it and create a new user.

   <br>


6. Now logged into Postman to send one of the requests.
   * **Please note:** I have attached a file called "Messaging system.postman_collection.json" which is a collection that contains all the requests needed for the project. 

   <br>
7. Send a request from Postman.
   * **Firstly you need to generate a token, and perform the following steps according to the picture:**

![](/images/generate_token.png)

   * Choose the POST/DELETE/GET option
   * Enter the appropriate URL
   * Click on the Body label
   * Click on the raw label
   * Click on the Text label and change it to JSON
   * Enter username and password
   * Click Send
   
   <br>

8. Now according to the next picture we'll copy only the value of the access (without quotation marks)

![](/images/token_resp.png)



   <br>

9. Finaly we'll access the request that we want to send
     * Now we'll go to the Headers tab, we'll add the key word Authorization in the Key and write Bearer in the Value and paste the token we received earlier.
     * Now we'll access the Body, add the relevant content inside the JSON object and click Send, and the request will be sent.

<br>

### Walk Through

### File Structure

```sh
├── message_system
    ├── images
    ├── README.md
    ├── Messaging system.postman_collection.json
    ├── manage.py
    ├── requirements.txt
    ├── message_system
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │   
    └── user_messages
        ├── migrations
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── serializers.py
        ├── tests.py
        ├── urls.py
        └── views.py
```