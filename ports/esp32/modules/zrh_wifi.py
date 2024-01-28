from zrh_wifi_ap import doAp
from time import sleep
import network
from zrh_wifi_nvs import ZrhNvs
from zrh_domain import hostname


def do_connect():
    # 使用域名方式访问（esp.local）
    # wlan.config(dhcp_hostname=hostname)

    network.hostname(hostname)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("hostname:", hostname)
    while not wlan.active(True):
        print("wait wlan")

    if not wlan.isconnected():
        print('--- 开始连接网格 ---')
        global wifiConfig
        try:
            zrh_wifi_nvs = ZrhNvs()
            wifiConfig = zrh_wifi_nvs.get_wifi_nvs()
            print("wifiConfig:", wifiConfig)
            wlan.connect(wifiConfig['ssid'], wifiConfig['password'])
        except OSError as e:
            print("读取wifi配置信息失败")

        connTimeOut = 0
        while not wlan.isconnected():
            print("连接失败，正在重新连接...")
            sleep(1)
            connTimeOut += 1
            # 连接网络10秒超时
            if (connTimeOut >= 10):
                print("--- 连接超时 ---")
                break
        if wlan.isconnected():
            print('连网成功:', wlan.ifconfig())
        else:
            print("连接失败了,开启ap模式")
            doAp()
