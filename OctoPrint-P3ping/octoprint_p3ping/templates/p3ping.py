import random
import paho.mqtt.client as mqtt
import json
import process_variables as p3

def on_connect(client, userdata, flags, rc):
    info("Connected with result code "+str(rc))
    client.subscribe(f'{p3.mqtt_client_id}/response/#')
    p3.connected = True


def on_message(client, userdata, msg):
    pass

p3.mqtt_client = mqtt.Client(transport="websockets")
p3.mqtt_client.on_connect = on_connect
p3.mqtt_client.on_message = on_message


def create_log_message(msg, module='P3Ping'):
    return '{ "msg": "' + str(msg) + '", "module": "' + str(module) + '" }'


def info(s):
    if p3.logger is not None:
        p3.logger.info(create_log_message("---- {} ----".format(s)))


def warning(s):
    if p3.logger is not None:
        p3.logger.warning(create_log_message("---- {} ----".format(s)))


def error(s):
    if p3.logger is not None:
        p3.logger.error(create_log_message("---- {} ----".format(s)))


def connect():
    info("Connecting to P3 with address {}".format(p3_name_or_ip))
    p3.mqtt_client.connect(p3.name_or_ip, 8883, 30)
    p3.mqtt_client.loop_start()


def send_ping(length):
    info("PING at {}mm".format(length))

    topic = "simcoe/request/ping"
    packet = {
        'header': {
            'originID': p3.mqtt_client_id,
            'msgID': 0,
        },
        'payload': {
            'method': 'get',
            'query': {},
        }
    }

    p3.mqtt_client.publish(topic, payload=json.dumps(packet), qos=2, retain=False)

    return True


def start_print(self, file):
    info("Starting print {}".format(file))
    topic = "simcoe/request/start"
    packet = {
        'header': {
            'originID': p3.mqtt_client_id,
            'msgID': 0,
        },
        'payload': {
            'method': 'get',
            'query': {},
        }
    }

    p3.mqtt_client.publish(topic, payload=json.dumps(packet), qos=2, retain=False)
     # code for n sec waitloop for the ping to ack

    return True

# OMEGA COMMANDS

def gotOmegacommand(self, cmd):

    if "O70" in cmd:   # Connect to Palette 3
        if self.connected:
            self.error("O70 command may appear only once in a print")
        else:
            self.connect()

        return


    if "O31" in cmd:   # PING
        command = cmd.split(" ")
        try:
            ping_offset = float(command[1])
            self.sendPing(ping_offset)
        except KeyError:
            self.error("Command {} does not have the correct format".format(cmd))
        except ValueError:
            self.error("Command {} length is not a proper float number".format(cmd))
