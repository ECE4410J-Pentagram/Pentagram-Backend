# Pentagram
## Getting Started

The entire project is consist of two part: frontend and backend. 
For backend, the system is going to be designed with:
- [Python Flask](https://flask.palletsprojects.com/en/2.3.x/): Web Framework.
- [Pydantic](https://docs.pydantic.dev/latest/): API datatype validation.
- [Peewee](https://docs.peewee-orm.com/en/latest/): Database ORM.
- [Hashlib](https://docs.python.org/3/library/hashlib.html): Cryptographic hashing library for user management.

## Model and Engine

## APIs and Controller

API Designs:

- GET /user: Get the information about the current user, including the username, avatar, etc.
- POST /user: Register a new user. The frontend should submit at least the username and the password through the API in JSON.
- PUT /user: Edit the user. This API supports changing all the user information exluding the passord.
- GET /login: Used to login. The backend will return with an Access token.
- GET /contact: Get the information about the contact list of the current user. The information includes all the public keys of the contact users.
- POST /contact/invitation: Create a new invitation to a new user. 
- GET /contact/invitation: This API will return all the invitation recieved by the user. Each invitation includes a ID.
- POST /contact/invitation/{id}: This API can accept or deny the recieved invitations.

## View UI/UX

## Team Roster

- Baichuan Li: Server Backend \& API Design
- Che Chen: Text Based Encryption
- Pingbang Hu: General Algorithms
- Jiajun Wang: Android Specific Coding
- Siwei Wang: PM \& Frontend
- Yiwen Yang: Algorithm Implementation
