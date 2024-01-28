import asyncio
from zrh_wifi import do_connect
from zrh_http_api import do_http_api
from zrh_mqtt_client import run_mqtt_client

do_connect()
run_mqtt_client()
loop = asyncio.get_event_loop()
loop.run_until_complete(do_http_api())
