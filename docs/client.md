# Client

## Proxies

The Crux Python Client supports using HTTP(S) and SOCKS proxies.

The environment variables `HTTP_PROXY` and/or `HTTPS_PROXY` can be used to set HTTP/HTTPS proxies.

```bash
export HTTP_PROXY="http://10.10.1.10:3128"
export HTTPS_PROXY="http://10.10.1.10:1080"
```

The `proxies` argument can be used for more complex proxy scenarios or for SOCKS proxies.

```python
proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
conn = Crux(proxies=proxies)
print(conn.whoami())
```

See the [requests proxy documentation](http://docs.python-requests.org/en/master/user/advanced/#proxies) for full usage.

# Custom API calls

The Crux Python Client can make API calls apart from the methods incorporated. Custom calls can be initiated via `Crux().api_client.api_call()` method. Below example explains the implementation and usage:

```python
conn = Crux()
identity_object_1 = conn.whoami()
print(identity_object_1)

{
    'companyName': 'test Identity Name',
    'description': 'created using automation',
    'email': 'example@example.com',
    'firstName': 'test FirstName',
    'identityId': '1314151617',
    'landingPage': None,
    'lastName': 'test LastName',
    'parentIdentityId': None,
    'phone': '2021222324',
    'role': None,
    'type': 'user',
    'website': 'www.example.com'
}

# Above call with Crux().api_client.api_call()

identity_object_2 = conn.api_client.api_call("GET", ["identities", "whoami"], model=Identity)
print(identity_object_2)

{
    'companyName': 'test Identity Name',
    'description': 'created using automation',
    'email': 'example@example.com',
    'firstName': 'test FirstName',
    'identityId': '1314151617',
    'landingPage': None,
    'lastName': 'test LastName',
    'parentIdentityId': None,
    'phone': '2021222324',
    'role': None,
    'type': 'user',
    'website': 'www.example.com'
}
```

## Closing the connection

The Crux Python Client has facility to close the connection as per user requirement which can help in avoiding file/socket limits related errors at operating system level.

```python

conn = Crux()

try:
    dataset = conn.get_dataset(id="A_DATASET_ID")
except CruxAPIError as e:
    print("Client error getting dataset:", e.message)
except CruxClientError  as e:
    print("Client error getting dataset:", e.message)
    raise
finally:
    conn.close()
```
