import network
import Wifi_Config 
from machine import Pin, SoftI2C
import ssd1306
import uasyncio
from time import sleep
import dht
Wifi_Connected=False
Temp=0
Hum=0

# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
# LINES CONFIGURATION

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height,i2c)

#SUPERVISORY LED
Sup_Led_1 = Pin(2, mode=Pin.OUT)
Sup_Led_2 = Pin(5, mode=Pin.OUT)

#CONTROL RELAY
Relay_1 = Pin(12, mode=Pin.OUT)
Relay_2 = Pin(13, mode=Pin.OUT)
Relay_1 = Pin(14, mode=Pin.OUT)
Relay_2 = Pin(15, mode=Pin.OUT)

#DH22
DH22_Sensor = dht.DHT11(Pin(4))


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
            global Wifi_Connected
            Wifi_Connected=True
            await uasyncio.sleep_ms(100)
        else:
            station.active(False)
            station.active(True)
            station.connect(Wifi_Config.SSID,Wifi_Config.Password)
            oled.fill(0)
            await uasyncio.sleep_ms(2000)
            
            if station.isconnected()==True:
                global Wifi_Connected
                Wifi_Connected=True
                await uasyncio.sleep_ms(100)
            else:
                oled.text('Wifi:DisConnected', 0, 0)
                global Wifi_Connected
                Wifi_Connected=False
                await uasyncio.sleep_ms(100)

async def Sup_LED():
    while True:
        if Wifi_Connected==False:
            Sup_Led_2.value(0)
            Sup_Led_1.value(not Sup_Led_1.value())
         
        else:
            Sup_Led_2.value(1)
            
        await uasyncio.sleep_ms(50)
         
async def DH22_Check():
    while True:
        DH22_Sensor = dht.DHT11(Pin(18))
        DH22_Sensor.measure()
        await uasyncio.sleep_ms(1000)
        global Temp
        Temp = DH22_Sensor.temperature()
        global Hum
        Hum = DH22_Sensor.humidity()
        oled.text('Temp:'+str(Temp), 0, 20)
        print('Temperature: %3.1f C' %Temp)
        print('Humidity: %3.1f %%' %Hum)
        await uasyncio.sleep_ms(5000)

async def Display():
    while True:
        oled.fill(0)
        if Wifi_Connected==True:
             oled.text('Wifi:Connected', 0, 0)
        else:
             oled.text('Wifi:DisConnect', 0, 0)
             oled.show()
        oled.text('Temp:'+str(Temp), 0, 10)
        oled.text('Humidity:'+str(Hum), 0, 20)
        oled.show()
        await uasyncio.sleep_ms(6000)
            
event_loop=uasyncio.get_event_loop()
event_loop.create_task(Check_Network())
event_loop.create_task(Sup_LED())
#event_loop.create_task(DH22_Check())
event_loop.create_task(Display())

event_loop.run_forever()