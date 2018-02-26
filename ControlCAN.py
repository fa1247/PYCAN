from CANstruct import *
import time
import datetime
import sys


class ControlCAN:

    def __init__(self, devtype=3, devindex=0, canindex=0, baudrate=250, acccode=0x00000000, accmask=0xFFFFFFFF):
        time0 = {100: 0x04, 125: 0x03, 250: 0x01, 500: 0x00, 1000: 0x00}
        time1 = {100: 0x1C, 125: 0x1C, 250: 0x1C, 500: 0x1C, 1000: 0x14}
        pData = {100: 0x160023, 125: 0x1C0011, 250: 0x1C0008, 500: 0x060007, 1000: 0x060003}
        self.CANdll = WinDLL("ControlCAN.dll")
        self.devtype = devtype
        self.devindex = devindex
        self.canindex = canindex
        self.baudrate = baudrate
        self.time0 = time0[self.baudrate]
        self.time1 = time1[self.baudrate]
        self.time1 = 0x1c
        self.acccode = acccode
        self.accmask = accmask
        self.initconfig = VCI_INIT_CONFIG(self.acccode, self.accmask, 0, 0, self.time0, self.time1, 0)
        self.pData = DWORD(pData[self.baudrate])
        self.errinfo = VCI_ERR_INFO()
        self.boardinfo = VCI_BOARD_INFO()
        self.receivebuf = (VCI_CAN_OBJ * 50)()
        self.sendbuf = VCI_CAN_OBJ()
        self.ctime = time.localtime()
        self.emptynum = 0
        self.receivenum = 0
        self.lasttime = 0
        self.timeinterval = 0
        # TODO 添加两次数据接收的时间差数据，送入sql

    def opendevice(self):
        respond = self.CANdll.VCI_OpenDevice(self.devtype, self.devindex, 0)
        if respond:
            print('打开CAN卡成功')
        else:
            print('打开CAN卡失败')
        return respond

    def initcan(self):
        if self.devtype == 21:
            self.CANdll.VCI_SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))
        respond = self.CANdll.VCI_InitCAN(self.devtype, self.devindex, self.canindex, byref(self.initconfig))
        if respond:
            print('初始化CAN卡成功')
        else:
            print('初始化CAN卡失败')
        return respond

    def startcan(self):
        respond = self.CANdll.VCI_StartCAN(self.devtype, self.devindex, self.canindex)
        if respond:
            print('启动CAN卡成功')
        else:
            print('启动CAN卡失败')
        return respond

    def resetcan(self):
        respond = self.CANdll.VCI_ResetCAN(self.devtype, self.devindex, self.canindex)
        if respond:
            print('复位CAN卡成功')
        else:
            print('复位CAN卡失败')
        return respond

    def readboardinfo(self):
        respond = self.CANdll.VCI_ReadBoardInfo(self.devtype, self.devindex, byref(self.boardinfo))
        if respond:
            print('获取设备信息成功')
        else:
            print('获取设备信息失败')
        return respond

    def receive(self):
        respond = self.CANdll.VCI_Receive(self.devtype, self.devindex, self.canindex, byref(self.receivebuf), 50, 10)
        if respond == 0xFFFFFFFF:
            print('读取数据失败')
            self.CANdll.VCI_ReadErrInfo(self.devtype, self.devindex, self.canindex, byref(self.errinfo))
        elif respond == 0:
            if self.devtype == 3 or self.devtype == 4:
                self.emptynum = self.emptynum + 1
                temp = self.emptynum // 20
                sys.stdout.write('\r' + "无新数据" + "." * temp)
                sys.stdout.flush()
        elif respond > 0:
            now = datetime.datetime.now()
            interval = (now - self.lasttime).total_seconds()
            self.lasttime = now
            if interval > 1:
                self.timeinterval = 0
            else:
                self.timeinterval = interval

            if self.devtype == 21:
                for i in range(respond):
                    for j in range(self.receivebuf[i].DataLen, 8):
                        self.receivebuf[i].Data[j] = 0

            if self.ctime != time.localtime():
                self.ctime = time.localtime()
                print(time.strftime("%Y-%m-%d %H:%M:%S", self.ctime), end=' ')
                print(self.receivebuf[0])
                self.emptynum = 0

                # f=open('pytxt.txt','a')
                # word = "%s %d\n"%(time.strftime("%Y-%m-%d %H:%M:%S", self.ctime),self.receivebuf[0].TimeStamp)
                # f.write(word)
                # f.close()
        self.receivenum = respond

    def transmit(self):
        respond = self.CANdll.VCI_Transmit(self.devtype, self.devindex, self.canindex, byref(self.sendbuf), 1)
        if respond == 1:
            print('发送CAN帧成功')
        else:
            print('发送CAN帧失败')
        return respond

    def readerrinfo(self):
        respond = self.CANdll.VCI_ReadErrInfo(self.devtype, self.devindex, self.canindex, byref(self.errinfo))
        if respond:
            print('读取错误成功')
        else:
            print('读取错误失败')
        return respond

    def setreference(self):
        respond = self.CANdll.VCI_SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))
        if respond:
            print('设定E-U波特率成功')
        else:
            print('设定E-U波特率失败')
        return respond

    def getreceivenum(self):
        respond = self.CANdll.VCI_GetReceiveNum(self.devtype, self.devindex, self.canindex)
        return respond

    def __del__(self):
        respond = self.CANdll.VCI_CloseDevice(self.devtype, self.devindex)
        if respond:
            print('关闭CAN卡成功')
        else:
            print('关闭CAN卡失败')
        return respond
