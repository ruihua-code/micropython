from zrh_wifi_ap import do_ap
from time import sleep
import network
from zrh_wifi_nvs import ZrhNvs
from zrh_domain import hostname
from machine import PWM, Pin

led2 = PWM(Pin(2))
led2.freq(500)
led2.duty(0)


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
        try:
            zrh_wifi_nvs = ZrhNvs()
            wifi_config = zrh_wifi_nvs.get_wifi_nvs()
            print("wifi_config:", wifi_config)
            wlan.connect(wifi_config['ssid'], wifi_config['password'])
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
            on_board_led()
        else:
            print("连接失败了,开启ap模式")
            led2.deinit()
            do_ap()


def on_board_led():
    led2.duty(800)
