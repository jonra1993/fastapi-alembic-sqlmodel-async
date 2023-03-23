# Reference http://glenfant.github.io/flask-g-object-for-fastapi.html
import contextvars
import types

request_global = contextvars.ContextVar(
    "request_global", default=types.SimpleNamespace(blah=1)
)


# This is the only public API
def g():
    return request_global.get()
