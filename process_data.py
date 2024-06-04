import sys
import json
from concurrent.futures import ThreadPoolExecutor
from rsi import RSI
from ovbv import OBV


def process_data(data):
    
    indicators = [
       RSI(),OBV()
    ]
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(indicator.process) for indicator in indicators]
        results = [future.result() for future in futures]
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No data provided")
        sys.exit(1)
    
    try:
        data = json.loads(sys.argv[1])
        results = process_data(data)
        for result in results:
            print(result)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing data: {e}")
        sys.exit(1)
