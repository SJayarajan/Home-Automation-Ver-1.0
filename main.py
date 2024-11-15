import network
import Wifi_Config 
from machine import Pin, SoftI2C
import ssd1306
import uasyncio
from time import sleep

# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
# LINES CONFIGURATION

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height,i2c)

#SUPERVISORY LED
Sup_Led = Pin(2, mode=Pin.OUT)

#CONNECTING TO WIFI NETWORK AS STATAION
station = network.WLAN(network.STA_IF)
#  INTRODUCTION
oled.fill(0)
oled.show()
oled.text('Home', 0, 0)
oled.text('Automation', 0, 10)
oled.text('Ver 1.0', 0, 20)
oled.show()
sleep(5.0)


if station.active() == False:
    station.active(True)
    oled.fill(0)
    oled.show()
    oled.text('WiFi>Connecting..', 0, 0)
    oled.show()
    sleep(2.0)

if station.isconnected()==False:
    station.connect(Wifi_Config.SSID,Wifi_Config.Password)
    sleep(2.0)

async def Check_Network():
    while True:
        if station.isconnected()==True:
            oled.fill(0)
            oled.text('Wifi:Connected', 0, 0)
            oled.text('to:'+str(Wifi_Config.SSID), 0, 10)
            oled.show()
            await uasyncio.sleep_ms(100)
        else:
            station.active(False)
            station.active(True)
            station.connect(Wifi_Config.SSID,Wifi_Config.Password)
            oled.fill(0)
            await uasyncio.sleep_ms(2000)
            
            if station.isconnected()==True:
                oled.text('Wifi:Connected', 0, 0)
                oled.text('to:'+str(Wifi_Config.SSID), 0, 10)
                oled.show()
                await uasyncio.sleep_ms(100)
            else:
                oled.text('Wifi:DisConnected', 0, 0)
                oled.text('to:'+str(Wifi_Config.SSID), 0, 10)
                oled.show()
                await uasyncio.sleep_ms(100)

async def Sup_LED():
    while True:
        Sup_Led.value(not Sup_Led.value())
        await uasyncio.sleep_ms(100)

event_loop=uasyncio.get_event_loop()
event_loop.create_task(Check_Network())
event_loop.create_task(Sup_LED())
event_loop.run_forever()