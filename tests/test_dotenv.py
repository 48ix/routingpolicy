"""Test DotEnv Loading."""

# Standard Library
import os
import json

# Project
from routingpolicy.dotenv import load_env

if __name__ == "__main__":
    load_env()
    print(json.dumps(dict(os.environ), indent=2))
