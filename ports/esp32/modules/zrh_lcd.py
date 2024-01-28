from ili9341 import Display, color565
from machine import Pin, SPI
import asyncio
from xglcd_font import XglcdFont
import os
from micropython import const
import zrh_mpy_folder
from zrh_dht import ZrhDHT


class ZrhLcd:
    cs_pin = Pin(13)
    rst_pin = Pin(12)
    mosi_pin = Pin(5)
    dc_pin = Pin(4)
    sck_pin = Pin(19)
    led_pin = Pin(21)
    miso_pin = Pin(22)  # 这个是用来从屏幕读取数据，如果只用来显示，可以不用
    # 创建SPI对象
    spi = SPI(2, baudrate=10000000, polarity=0, phase=0, bits=8,
              firstbit=0, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)
    # 创建屏幕对象

    tft = Display(spi, cs=cs_pin, dc=dc_pin, rst=rst_pin,
                  width=320, height=240, rotation=90)

    task = None
    EspressoDolce18x24 = None
    is_font_file = False

    def __init__(self) -> None:
        font_file = const("EspressoDolce18x24.c")
        ZrhLcd.is_font_file = font_file in os.listdir("mpy_image_folder")

        if ZrhLcd.is_font_file:
            ZrhLcd.EspressoDolce18x24 = XglcdFont(
                "mpy_image_folder/EspressoDolce18x24.c", 18, 24)

    async def on_start_lcd():
        zrh_dht = ZrhDHT()
        while True:
            dht_data = zrh_dht.get_dht_data()
            ZrhLcd.tft.draw_image(
                "mpy_image_folder/temperature.raw", 10, 10, 32, 32)
            ZrhLcd.tft.draw_image(
                "mpy_image_folder/humidity.raw", 12, 50, 32, 32)
            if ZrhLcd.is_font_file:
                ZrhLcd.tft.draw_text(45, 15, "Temperature: " +
                                     str(dht_data[0]), ZrhLcd.EspressoDolce18x24, color565(0, 255, 0))
                ZrhLcd.tft.draw_text(48, 55, "Humidity: " +
                                     str(dht_data[1])+"%", ZrhLcd.EspressoDolce18x24, color565(0, 255, 0))
            else:
                ZrhLcd.tft.draw_text8x8(45, 15, "Temperature: " +
                                        str(dht_data[0]), color565(0, 255, 0))
                ZrhLcd.tft.draw_text8x8(48, 55, "Humidity: " +
                                        str(dht_data[1])+"%", color565(0, 255, 0))
            await asyncio.sleep(1)

    def on_lcd(self):
        ZrhLcd.task = asyncio.create_task(ZrhLcd.on_start_lcd())

    def off_lcd(self):
        ZrhLcd.tft.clear()
        ZrhLcd.task.cancel()
