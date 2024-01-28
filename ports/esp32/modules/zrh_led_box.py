from machine import Pin


class ZrhLedBox:
    pin = Pin(14, Pin.OUT, Pin.PULL_UP)

    def on_led_box(self):
        ZrhLedBox.pin.value(1)

    def off_led_box(self):
        ZrhLedBox.pin.value(0)
