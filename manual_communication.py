import time
from Communication import Communication

communication = Communication()

def test():
    communication.simple_comm("4000", 2)
    # communication.simple_comm("3005", 3)
    time.sleep(16000)

test()