import requests

HOST = 'http://localhost:8000'

def create_device(name: str, key: str):
    url = HOST + '/api/device/'
    data = {"name": name, "key": key}

    r = requests.post(url, json=data)
    print(r.text)
    return r.json()

def login_device(name: str, key: str):
    url = HOST + '/api/login/'
    data = {"name": name, "key": key}
    r = requests.post(url, json=data)
    print(r.text)
    return r.json()['Authorization']

def upload_key(auth: str, key_name: str, pk: str):
    url = HOST + '/api/key/'
    headers = {'Authorization': auth}
    data = {"name": key_name, "pk": pk}
    r = requests.post(url, headers=headers, json=data)
    print(r.text)
    return r.json()

def create_invitation(auth: str, from_key: str, to_device: str):
    url = HOST + '/api/invitation/sent'
    headers = {'Authorization': auth}
    data = {"from_key": { "name": from_key }, "to_device": {"name": to_device}}
    r = requests.post(url, headers=headers, json=data)
    print(r.status_code, r.text)
    return r.json()

def list_recv_invitations(auth: str):
    url = HOST + '/api/invitation/received'
    headers = {'Authorization': auth}
    r = requests.get(url, headers=headers)
    print(r.text)
    return r.json()

def list_friends(auth: str):
    url = HOST + '/api/friend/'
    headers = {'Authorization': auth}
    r = requests.get(url, headers=headers)
    print(r.text)
    return r.json()

def accept_invitation(auth: str, invitation_id: int, shared_key: str):
    url = HOST + '/api/invitation/received/accept'
    headers = {'Authorization': auth}
    data = {"id": invitation_id, "shared_key": {"name": shared_key}}

    r = requests.post(url, headers=headers, json=data)
    print(r.text)
    return r.json()

def delete_friend(auth: str, id: int):
    url = HOST + '/api/friend/'
    headers = {'Authorization': auth}
    data = { "id": id }
    r = requests.delete(url, headers=headers, json=data)
    print(r.text)
    return r.json()


create_device('device1', 'key1')
create_device('device2', 'key2')

auth1 = login_device('device1', 'key1')
auth2 = login_device('device2', 'key2')

upload_key(auth1, 'testkeyname1', 'pk1')
upload_key(auth2, 'testkeyname2', 'pk2')
create_invitation(auth1, 'testkeyname1', 'device2')
print("List Invitation Before Accept: ", list_recv_invitations(auth2))
assert(len(list_recv_invitations(auth2)) == 1)
assert(len(list_recv_invitations(auth1)) == 0)
assert(len(list_friends(auth1)) == 0)
accept_invitation(auth2, 1, 'testkeyname2')
print("List Invitation After Accept: ", list_recv_invitations(auth2))
assert(len(list_recv_invitations(auth2)) == 0)
delete_friend(auth2, 1)
print(list_friends(auth1))
print(list_friends(auth2))
assert(len(list_friends(auth1)) == 0)
assert(len(list_friends(auth2)) == 0)
