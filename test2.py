import time
from Communication import Communication

comunication = Communication()

while True:

    comunication.serializer_comunication("800")
    time.sleep(0.5)