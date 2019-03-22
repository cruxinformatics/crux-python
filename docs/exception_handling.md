# Exception handling

The `crux` client will raise exceptions when errors are encountered. There are two base exception classes: `CruxAPIError` and `CruxClientError`.

## CruxAPIError

`CruxAPIError` will be raised when the API returns an error.

**Attributes:**

- **status_code:** The status code returned by the API
- **error_message:** The error message return by the API

## CruxClientError

`CruxClientError` will be raised when the client encounters an error prior to reserving a response from the API.

**Attributes:**

- **message:** The error reported by the client

## CruxClientHTTPError

`CruxClientHTTPError` is raised when client encounters HTTP related errors.

## CruxClientConnectionError

`CruxClientConnectionError` is raised when client encounters Proxy and SSL related errors.

## CruxClientTimeout

`CruxClientTimeout` is raised when client timeouts.

## Examples

```python
from crux import Crux

try:
    conn = Crux()
except CruxClientError as e:
    print("Error creating client:", e.message)
    raise
finally:
    conn.close()

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

