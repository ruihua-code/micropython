from esp32 import NVS


class ZrhNvs:
    wifi_config = NVS("WIFI_CONFIG")

    # 读取持久存储wifi配置信息
    def get_wifi_nvs(self):
        ssidBuf = bytearray(12)
        passwordBuf = bytearray(12)
        ZrhNvs.wifi_config.get_blob("ssid", ssidBuf)
        ZrhNvs.wifi_config.get_blob("password", passwordBuf)
        return {
            "ssid": ssidBuf.decode(),
            "password": passwordBuf.decode()
        }

    # wifi配置信息持久存储
    def set_wifi_nvs(self, ssid, password):
        ZrhNvs.wifi_config = NVS("WIFI_CONFIG")
        ZrhNvs.wifi_config.set_blob("ssid", ssid)
        ZrhNvs.wifi_config.set_blob("password", password)
        ZrhNvs.wifi_config.commit()
        print("--- wifi配置信息存储完成 ---")

    # 清除wifi配置信息
    def erase_wifi_nvs(self):
        try:
            ZrhNvs.wifi_config.erase_key("ssid")
            ZrhNvs.wifi_config.erase_key("password")
        except OSError as e:
            print("清空wifi配置信息错误:", e)
