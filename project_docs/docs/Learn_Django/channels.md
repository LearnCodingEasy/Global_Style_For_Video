## Install

```
pip install channels
```

## Setting

```
INSTALLED_APPS = [
    ...
    "channels",
]

ASGI_APPLICATION = "backend_django.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

## Consumers

```text
consumers.py
```

## Routing

```text
routing.py
```
