# Logging

Log request and responses from Crux.

Provides `DEBUG` level logging in order to understand and troubleshoot problem.

```python

import logging

from crux import Crux


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


conn = Crux()

identity_object = conn.whoami()
```
