# agent-py

## Requirements

- Python 3.X
- virtualenv [intall](https://virtualenv.pypa.io/en/latest/installation.html)

## Run project

```sh
make environment
make help
make run
#or
make debug
```

## Configuration

Environment variable:

- AGENT_ENV: local/production
- AGENT_VERSION: app version, default 1.0.0, endpoint /version
- AGENT_DESCRIPTION: app description
- AGENT_DEBUG: activate debug mode (boolean)

local : enable reload mode (default)
prod : no hot reload

## Usage

Run project with `make debug` and consult url in log for api doc at `/docs` or `/redoc`.

Application is running 2 threads, one for the API to expose metrics and one for collecting metrics.
