import dht
from machine import Pin


class ZrhDHT:
    dht_pin = dht.DHT11(Pin(15))
    
    # 对人体比较适宜的相对湿度为：夏季室温25℃时，相对湿度控制在 40%－50%比较舒适；
    # 冬季室温20℃时，相对湿度控制在60%－70%
    def get_dht_data(self):
        self.dht_pin.measure()
        # print("温度: %s℃ 温度: %sRH" %
        #       (ZrhDHT.dht_pin.temperature(), ZrhDHT.dht_pin.humidity()))
        return ZrhDHT.dht_pin.temperature(), ZrhDHT.dht_pin.humidity()
