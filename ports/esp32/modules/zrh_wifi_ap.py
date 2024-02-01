import network
from zrh_wifi_nvs import ZrhNvs
from microdot_asyncio import Microdot
import asyncio
import json
import machine
from zrh_wifi_html import html
from zrh_response_json import ZrhResponseJson
from zrh_led import ZrhLedBoard

res_json = ZrhResponseJson()

app = Microdot()


@app.get("/wifi")
async def show_wifi_page(request):
    return html, 200, {'Content-Type': 'text/html'}


@app.post("/setWifi")
async def set_wifi(request):
    bodyJson = json.loads(request.body.decode())
    ssid = bodyJson['ssid']
    pwd = bodyJson["password"]
    zrh_wifi_nvs = ZrhNvs()
    zrh_wifi_nvs.set_wifi_nvs(ssid, pwd)
    res_json.success("配置wifi完成")
    asyncio.create_task(reboot())
    return res_json.json()


@app.get("/on_led")
def get_on_led(request):
    color_str = request.args.get("color")
    zrh_led_board = ZrhLedBoard()
    if color_str is not None:
        color_arr = color_str.split(',')
        color = tuple(list(map(int, color_arr)))
        zrh_led_board.on_led(color)
    else:
        zrh_led_board.on_led((100, 100, 100))
    res_json.success("成功")
    return res_json.json()


@app.get("/off_led")
def get_off_led(request):
    zrh_led_board = ZrhLedBoard()
    zrh_led_board.off_led()
    res_json.success("成功")
    return res_json.json()


# 设置wifi成功之后，延时1秒重启设备
async def reboot():
    await asyncio.sleep(1)
    machine.reset()


# 创建wifi热点，ssid=ESP-AP password=esp123456
def init_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP-AP', authmode=network.AUTH_WPA_WPA2_PSK,
              password='esp123456')

    while ap.active() == False:
        pass
    print('--- AP热点启动成功 ---')
    print(ap.ifconfig())


async def init_wifi_page():
    print("启动microdot服务....")
    await app.start_server(debug=True, port=80)


def doAp():
    print("开始启动ap.....")
    init_ap()
    asyncio.run(init_wifi_page())
