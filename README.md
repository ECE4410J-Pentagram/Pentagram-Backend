# Getting Started

For the backend, the system is going to be designed with:
- [Python FastAPI](https://fastapi.tiangolo.com/): Web Framework.
- [Pydantic](https://docs.pydantic.dev/latest/): API datatype validation.
- [Peewee](https://docs.peewee-orm.com/en/latest/): Database ORM.
- [Hashlib](https://docs.python.org/3/library/hashlib.html): Cryptographic hashing library for user management.

# Model and Engine

## Storymap:

![](https://cryptexstatics.patrickli.one/storymap.png)

## Backend Architecture:

![](https://cryptexstatics.patrickli.one/Backend.drawio.png)

- Step 1: Register the user. On registration, the client frontend will generate a pair of public and private keys. The public keys will be sent to the server along with the username and password.
- Step 2: Encryption: The user will provide the text to be encrypted. The frontend will use put the information through a list of encryption. The encryption needs the public key of the receiver from the server. The result is provided back to the user.
- Step 3: Information sent through 3rd party platform such as WeChat.
- Step 4: The receiver decrypts the information with his private key.

# APIs and Controller

Currently, all the API definitions are posted at our [Official Server](https://cryptex.software/api/docs).
