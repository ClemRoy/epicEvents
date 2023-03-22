# epicEvents

## Installation

This locally-executable API can be installed and executed from [http://localhost:8000//](http://localhost:8000/) using the following steps.


1. Clone this repository using `$ git clone clone https://github.com/ClemRoy/epicEvents.git` (you can also download the code using [as a zip file](https://github.com/ClemRoy/epicEvents/archive/refs/heads/master.zip))
2. Move to the epicEvents-api root folder
3. Create a virtual environment for the project with `$ py -m venv env` on windows or `$ python3 -m venv env` on macos or linux.
4. Activate the virtual environment with `$ env\Scripts\activate` on windows or `$ source env/bin/activate` on macos or linux.
5. Install project dependencies with `$ pip install -r requirements.txt`
6. Run the server with `$ python manage.py runserver`

When the server is running after step 7 of the procedure, the epicEvents-API can be requested from endpoints starting with the following base URL: http://localhost:8000/client/,http://localhost:8000/contract/,http://localhost:8000/event/ 
and http://localhost:8000/signup/ (which is limited to superuser for the account creation).

Steps 1-3 and 5 is only required for initial installation. For subsequent launches of the API, you only have to execute steps 4 and 6 from the root folder of the project.

## Usage and detailed endpoint documentation


The API provides multiple endpoint.You can access the postman documentation with the relevant endpoint here: https://documenter.getpostman.com/view/19443765/2s93RL2Ght.

- Client: Allow user to see the clients according to their respective attribution,allow the creation and modification of new client with post request, destroy request are limited to superuser.

- Search and filter for client: [http://localhost:8000/client/?]. The filters available are:

   - `email=<email>` to get client filter by exact email.
   - `full_name=<full_name>` to get client by giving part of their full name (ie first or last name or both).
   - `last_name=<last_name>` to get client with their exact last name.

- Contract: Allow user to see the clients according to their respective attribution,allow the creation and modification of new client with post request, destroy request are limited to superuser.

- Search and filter for client: [http://localhost:8000/contract/?]. The filters available are:

   - `client_email=<email>` to get contract filter by exact client email.
   - `client_full_name=<full_name>` to get contract by giving part of the client full name (ie first or last name or both).
   - `last_name=<last_name>` to get contract by giving the client exact last name.
   - `date_created=<date>` to get contract by creation date
   - `payment_due_date=<date>` to get contract by giving the payment date.
   - `amount=<amount>` to get contract by amount due.

- Event: Allow user to see the events according to their respective attribution,allow the creation and modification of new client with post request, destroy request are limited to superuser.

- Search and filter for client: [http://localhost:8000/event/?]. The filters available are:

   - `client_email=<email>` to get event filter by exact client email.
   - `client_full_name=<full_name>` to get event by giving part of the client full name (ie first or last name or both).
   - `last_name=<last_name>` to get event by giving the client exact last name.
   - `event_date=<date>` to get event by event date

