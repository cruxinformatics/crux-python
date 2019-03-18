# Authentication

The Crux Python Client interacts with the Crux API, which requires an API key. Your API key can be retrieved from your Profile within the [Crux web application](https://app.cruxinformatics.com/).

## Function arguments

For basic scripts you can set the API key with the `api_key` argument when instantiating the Crux client.

```python
from crux import Crux

conn = Crux(api_key="YOUR_API_KEY")
print(conn.whoami())
conn.close()
```

The optional argument `api_host` can be used to set a different API host, the default is `https://api.cruxinformatics.com`.

```python
from crux import Crux

conn = Crux(api_key="YOUR_API_KEY", api_host="https://api.cruxinformatics.com")
print(conn.whoami())
conn.close()
```

## Environment variables

In production environments, or on your workstation, you can an environment variable to set the API key.

Shell:

```bash
export CRUX_API_KEY="YOUR_API_KEY"
```

Python:

```python
from crux import Crux

conn = Crux()
print(conn.whoami())
conn.close()
```

The API host can optionally be set, it defaults to `https://api.cruxinformatics.com`.

Shell:

```bash
export CRUX_API_KEY="YOUR_API_KEY"
export CRUX_API_HOST="https://api.cruxinformatics.com"
```

Python:

```python
from crux import Crux

conn = Crux()
print(conn.whoami())
conn.close()
```

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
conn.close()
```

See the [requests proxy documentation](http://docs.python-requests.org/en/master/user/advanced/#proxies) for full usage.
