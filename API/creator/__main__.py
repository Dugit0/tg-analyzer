"""Main API."""
import sys
from . import start_api

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please select login and path for the file with results")
    else:
        try:
            start_api(sys.argv[1], sys.argv[2])
        except Exception as e:
            print(f"Error: {e}")
