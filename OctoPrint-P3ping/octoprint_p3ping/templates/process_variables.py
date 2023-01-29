import random

instantiated = False
logger = None
mqtt_client_id = "p3mqtt-client-{}".format(random.randrange(0, 65536, 2))
connected = False
name_or_ip = None
mqtt_client = None
