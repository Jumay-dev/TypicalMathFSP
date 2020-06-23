import sys
import time # for delay, simulating of backend answer
import json

mul = sys.argv[1]
parsed = json.loads(mul)


# time.sleep(3) # 3 sec delay

print(parsed['x'])
sys.stdout.flush()