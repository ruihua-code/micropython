from umqtt.simple import MQTTClient
from micropython import const
from zrh_led_box import ZrhLedBox
import asyncio
from time import sleep
from machine import Timer, reset

bemfa_key = const('11dd1fbc5cbe353fafdc955210933b87')
bemfa_topic = const('woshideng002')
bemfa_host = const('bemfa.com')
bemfa_port = const('9501')


def ping(self):
    print("ping...")
    client.ping()


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()


async def on_start_mqtt():
    global client
    client = MQTTClient(bemfa_key, bemfa_host, bemfa_port, keepalive=30)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(bemfa_topic)
    # 开启定时器，定时发送心跳,如果不发送心跳，设备会掉线
    tim = Timer(-1)
    tim.init(period=30000, mode=Timer.PERIODIC, callback=ping)
    while True:
        await asyncio.sleep(1)
        client.check_msg()


def on_message(topic, msg):
    if msg.decode() == 'on':
        print("开灯了...")
        zrh_led_box = ZrhLedBox()
        zrh_led_box.on_led_box()

    elif msg.decode() == 'off':
        print("关灯了...")
        zrh_led_box = ZrhLedBox()
        zrh_led_box.off_led_box()


def run_mqtt_client():
    asyncio.create_task(on_start_mqtt())
