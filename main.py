# main.py
import machine
from machine import I2C,Pin
from bmp280 import *
import acqMP
import onewire
import time, ds18x20

pinOUT = machine.Pin(16, machine.Pin.OUT)
pinIN = machine.Pin(0, machine.Pin.IN)
print("Starting module")
for i in range(10):
        pinOUT.value(1)
        time.sleep(0.5)
        pinOUT.value(0)
        time.sleep(0.5)

SSID_glob = 'FunBox2-F514'
PASSWD_glob = '2C7DA5646F673E7FA34E3A379A'
IPDEST_glob = '192.168.0.99'
Port_glob = 8889
print("Module are initialized")

while ("_"):
        ow = onewire.OneWire(Pin(0))
        ds = ds18x20.DS18X20(ow)
        bus = I2C(scl=Pin(5), sda=Pin(4))
        bmp = BMP280(bus)
        roms = ds.scan()
        ds.convert_temp()

        acqMP.connWiFi(SSID_glob,PASSWD_glob)

        print("Mes 1")
        #Pushing interwal = 43200000 = 12h
        #Pushing interwal = 21600000 = 6h
        #Pushing interwal = 900000 = 15min = 0,25h
        #Pushing interwal = 1800000 = 30min = 0,5h
        acqMP.ACQ(IPDEST_glob,Port_glob,str(bmp.temperature),1,'live',43200000)
        pinOUT.value(0)
        time.sleep(0.5)
        pinOUT.value(1)

        print("Mes 2")
        acqMP.ACQ(IPDEST_glob,Port_glob,str(ds.read_temp(roms[0])),2,'eco',21600000)
        pinOUT.value(0)
        time.sleep(0.5)
        pinOUT.value(1)

        print("Mes 3")
        acqMP.ACQ(IPDEST_glob,Port_glob,str(ds.read_temp(roms[1])),3,'live',43200000)
        pinOUT.value(0)
        time.sleep(0.5)
        pinOUT.value(1)

        time.sleep(2)
        pinOUT.value(0)
        #Max measument stored in memory is 114 sample
        #measurmnet interval 1800 is 30min period 
        #measurmnet interval 900 is 15min period 
        #measurmnet interval 300 is 5min period 
        for x in range(300):
                #acqMP.asyncPushFromLocal('192.168.0.103',5500)
                time.sleep(1)


