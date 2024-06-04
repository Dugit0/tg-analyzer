"""Main API."""
import sys
from . import start_api

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please select login")
    else:
        start_api(sys.argv[1])
