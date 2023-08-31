# sampleLinkedInFlask
This project sets up a basic Flask web application that allows users to log in using their LinkedIn accounts through OAuth 2.0, retrieves user data from LinkedIn's API, and restricts access to certain routes to authenticated users only. 

The core functionalities are user authentication, session management, and access control to different parts of the application.

## How to run

1. Clone from this repo

   `git clone (https://github.com/pdelteil/sampleLinkedInFlask.git)`
   
2. Install requirements
   `pip install -r requirements.txt`

3. Create and app, get client_ID and secret_id from Linkedin. [(Step by step guide)](https://www.linkedin.com/pulse/how-get-signin-linkedin-work-taric-andrade/)
   

# Screenshots 

## Chat 

When the user is not yet authenticated:

<img src="https://github.com/pdelteil/sampleLinkedInFlask/assets/20244863/d83b5e4a-ed21-483b-8cdc-6420a909685b" width="400">


## Linkedin Login
Login screen

<img src="https://github.com/pdelteil/sampleLinkedInFlask/assets/20244863/b38f2446-111c-45fc-bd6f-ed5e91d53cf8" width="400">

When the user is authenticated:

<img src="https://github.com/pdelteil/sampleLinkedInFlask/assets/20244863/964ea7f3-b0f3-438d-a3f5-0fa1e6d957fc" width="400">




## Details about the source code:

* Unauthorized Handler:

    Defines an unauthorized handler function that is executed when access is denied to a resource due to lack of authentication.

* Login Route:

    Defines a route /login that initiates the LinkedIn OAuth 2.0 authorization process. It constructs the authorization URL with required parameters and redirects the user to it.

* Logout Route:

    Defines a route /logout that clears the LinkedIn OAuth session, effectively logging the user out.

* Authorized Route:

    Defines a route /login/authorized where the user is redirected after successful LinkedIn OAuth authorization. This route handles the OAuth authorization code received and exchanges it for an access token. It then fetches user data using the LinkedIn API and stores some user details in the session. Finally, it logs the user into the Flask application using Flask-Login and redirects them to the chat route.

* Index Route:

    Defines a route / that serves as the index or homepage of the application.

* Chat Route:

    Defines a route /chat which represents a chat interface, accessible only to logged-in users. It uses the @login_required decorator from Flask-Login to ensure that only authenticated users can access this route.


  
