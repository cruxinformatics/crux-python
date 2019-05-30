# Logging

Log request and responses from Crux.

Provides `DEBUG` level logging in order to understand and troubleshoot problem.

```python
import logging

from crux import Crux


logging.basicConfig()
logging.getLogger("crux").setLevel(logging.DEBUG)


conn = Crux()

identity_object = conn.whoami()
```


## Trace Logging

Crux client provides `TRACE` level logging to understand and troubleshoot problems involving senstive information.

```python
import logging
from crux import Crux, TRACE
logging.basicConfig()
logging.getLogger("crux").setLevel(TRACE)
conn=Crux()
identity_object = conn.whoami()
```
