import os
import gc
import time
import socket
import network
import ntptime

#####Constant variable#####
lastPushData = 0

#####Connection section#####
def connWiFi(SSID,PASSWD):
    #Create wlan interface and connect to WiFi network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID,PASSWD)
    while (sta_if.isconnected() =='False'):
        sta_if.connect(SSID,PASSWD)
    try:
        ntptime.settime()
    except Exception as ex:
        writeDebug('[ERROR] sync')
    writeDebug('[DEBUG] Edge device is connected to Wifi '+ SSID)
    return 0
def pushDataViaTCP(IPDEST,PORT,MEASURMENT,ID_Location,timestamp):

    global lastPushData
    addr_info = socket.getaddrinfo(IPDEST, PORT)
    addr =addr_info[0][-1]
    s = socket.socket()
    try:
        s.connect(addr)
        print(str(MEASURMENT)+","+str(ID_Location)+","+str(timestamp))
        s.send(str(MEASURMENT)+","+str(ID_Location)+","+str(timestamp))
        s.close()
        lastPushData = time.ticks_ms()
    except Exception as ex:
        print('[ERROR] Error while try to connect to destination IP '+ IPDEST +"\nError msg: "+ ex)
        writeDebug('[ERROR] Error while try to connect to destination IP '+ IPDEST)
        s.close()
        return 1
    writeDebug('[DEBUG] Connection established with ' + IPDEST + ' on port ' + str(PORT))
    return 0
#####Local operation#####
def writeLocal(MEASURMENT,ID_Location,timestamp):
    file = open ("localTemporaryDB.txt","a+")
    file.seek(0,2)
    file.write(str(MEASURMENT)+","+str(ID_Location)+","+str(timestamp)+"\n")
    file.close()
    return 0
def removeDataFromDB():
    os.remove("localTemporaryDB.txt")
    file = open ("localTemporaryDB.txt","w")
    file.close()
    return 0
#####Acqisition#####
def ACQ(IPDEST,PORT,MEASURMENT,ID_Location,MODE,PUSHING_INTERVAL):
    #if connWiFi(SSID,PASSWD) == 0:
    try:
        global lastPushData
        curr_time = (str(time.localtime(time.time())[0]) +"-"+\
            str(time.localtime(time.time())[1])+"-"+\
            str(time.localtime(time.time())[2])+" "+\
            str(time.localtime(time.time())[3])+":"+\
            str(time.localtime(time.time())[4])+":"+\
            str(time.localtime(time.time())[5])\
        )
        if MODE == 'live':
            print("live")
            pushDataViaTCP(IPDEST,PORT,MEASURMENT,ID_Location,curr_time)
        elif MODE == 'eco':
            print("eco")
            writeLocal(MEASURMENT,ID_Location,curr_time)
            #conditionTime = time.ticks_add(lastPushData, PUSHING_INTERVAL)
            print("Curr: "+str(time.ticks_ms()))
            if time.ticks_ms() >  time.ticks_add(lastPushData, PUSHING_INTERVAL) :
                pushDataFromLocal(IPDEST,PORT)
    #else:
    except Exception as ex:
        return 1
    return 0
def pushDataFromLocal(IPDEST,PORT):
    global lastPushData
    with open("localTemporaryDB.txt") as file:
        for line in file:
            pushDataViaTCP(IPDEST,PORT,line.split(',')[0],line.split(',')[1],line.split(',')[2])
            time.sleep(0.1)
        lastPushData = time.ticks_ms()
        #removeDataFromDB()
    print("\nSend all stored data")#
    
    return 0
def asyncPushFromLocal(IPSerwer,MamagmentPORT):
    addr_info = socket.getaddrinfo(IPSerwer, MamagmentPORT)
    addr = addr_info[0][-1]
    s = socket.socket()
    try:
        s.connect(addr)
        data = s.recv(5)
        print("Hello_"+ str(data[0]) +"_-->")
        if int(data[0]) == 49:
            print("go in loop")
            pushDataFromLocal(IPSerwer,8889)
    except Exception as ex:
        print("[ERROR] TCP serwer is not present --> "+ str(ex))
#####Debug section#####
def free(full=False):
  s = os.statvfs('//')
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P)+"\n"+'{0} MB'.format((s[0]*s[3])/1048576))
def writeDebug(MSG):
    try:
        file = open ("localDebug.txt","a+")
        file.seek(0,2)
        file.write(MSG+"\n")
        file.close()
    except Exception as ex:
        print('[FATAL] Error while debug data')
        return 1
    return 0
def sendDebug(IPDEST,PORT,MSG):
    #deprecate
    try:
        addr_info = socket.getaddrinfo(IPDEST, PORT)
        addr =addr_info[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(MSG)
    except Exception as ex:
        print('Error while try to connect/sending data to destination IP '+ IPDEST)#error
        return 1
    else:
        print('Connection established with ' + IPDEST + ' on port ' + str(PORT))#debug
        return 0