import contextvars
import types

request_global = contextvars.ContextVar(
    "request_global", default=types.SimpleNamespace()
)


# This is the only public API
def g():
    return request_global.get()
