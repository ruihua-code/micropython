import network
from zrh_wifi_nvs import ZrhNvs
from microdot_asyncio import Microdot
import asyncio
import json
import machine
from zrh_wifi_html import html
from zrh_response_json import ZrhResponseJson

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
    ap.active(False)
    asyncio.create_task(reboot())
    return res_json.json()


# 设置wifi成功之后，延时1秒重启设备
async def reboot():
    await asyncio.sleep(1)
    machine.reset()


# 创建wifi热点，ssid=ESP-AP password=esp123456
def init_ap():
    global ap
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


def do_ap():
    print("开始启动ap.....")
    init_ap()
    asyncio.run(init_wifi_page())
