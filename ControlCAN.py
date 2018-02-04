from CANstruct import *
import time
import sys


class ControlCAN:

    def __init__(self, devtype=3, devindex=0, canindex=0, time0=0x01, time1=0x1C, acccode=0x00000000,
                 accmask=0xFFFFFFFF):
        self.CANdll = WinDLL("ControlCAN.dll")
        self.devtype = devtype
        self.devindex = devindex
        self.canindex = canindex
        self.time0 = time0
        self.time1 = time1
        self.acccode = acccode
        self.accmask = accmask
        self.initconfig = VCI_INIT_CONFIG(self.acccode, self.accmask, 0, 0, self.time0, self.time1, 0)
        self.pData = DWORD(0x1c0008)
        self.errinfo = VCI_ERR_INFO()
        self.boardinfo = VCI_BOARD_INFO()
        self.receivebuf = (VCI_CAN_OBJ * 50)()
        self.sendbuf = VCI_CAN_OBJ()
        self.ctime = time.localtime()
        self.emptynum = 0


    def opendevice(self):
        respond = self.CANdll.VCI_OpenDevice(self.devtype, self.devindex, 0)
        if respond:
            print('打开成功')
        else:
            print('打开失败')
        return respond

    def initcan(self):
        if self.devtype == 21:
            self.CANdll.VCI_SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))
        respond = self.CANdll.VCI_InitCAN(self.devtype, self.devindex, self.canindex, byref(self.initconfig))
        if respond:
            print('初始化成功')
        else:
            print('初始化失败')
        return respond

    def startcan(self):
        respond = self.CANdll.VCI_StartCAN(self.devtype, self.devindex, self.canindex)
        if respond:
            print('启动成功')
        else:
            print('启动失败')
        return respond

    def resetcan(self):
        respond = self.CANdll.VCI_ResetCAN(self.devtype, self.devindex, self.canindex)
        if respond:
            print('复位成功')
        else:
            print('复位失败')
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

        return respond

    def transmit(self):
        respond = self.CANdll.VCI_Transmit(self.devtype, self.devindex, self.canindex, byref(self.sendbuf), 1)
        if respond == 1:
            print('发送成功')
        else:
            print('发送失败')
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
            print('关闭成功')
        else:
            print('关闭失败')
        return respond
