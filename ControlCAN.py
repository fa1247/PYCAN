from CANstruct import *
import time
import datetime
import sys


def issucceed(func_name):
    def deco(func):
        def wrapper(self,*args):
            if func(self,*args):
                print(func_name+"成功")
            else:
                print(func_name+"失败")
        return wrapper
    return deco


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
        self.sendbuf = (VCI_CAN_OBJ * 50)()
        self.emptynum = 0


    @issucceed("打开CAN卡")
    def opendevice(self):
        return self.CANdll.VCI_OpenDevice(self.devtype, self.devindex, 0)

    @issucceed("初始化CAN卡")
    def initcan(self):
        if self.devtype == 21:
            self.CANdll.VCI_SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))
        return self.CANdll.VCI_InitCAN(self.devtype, self.devindex, self.canindex, byref(self.initconfig))

    @issucceed("启动CAN卡")
    def startcan(self):
        return self.CANdll.VCI_StartCAN(self.devtype, self.devindex, self.canindex)

    @issucceed("复位CAN卡")
    def resetcan(self):
        return self.CANdll.VCI_ResetCAN(self.devtype, self.devindex, self.canindex)

    @issucceed("获取设备信息")
    def readboardinfo(self):
        return self.CANdll.VCI_ReadBoardInfo(self.devtype, self.devindex, byref(self.boardinfo))

    # 以下两个函数不加修饰器因为要重复调用，减少不必要输出

    def getreceivenum(self):
        return self.CANdll.VCI_GetReceiveNum(self.devtype, self.devindex, self.canindex)

    def receive(self):
        respond = self.CANdll.VCI_Receive(self.devtype, self.devindex, self.canindex, byref(self.receivebuf), 50, 10)
        if respond == 0xFFFFFFFF:
            print("读取数据失败")
            self.CANdll.VCI_ReadErrInfo(self.devtype, self.devindex, self.canindex, byref(self.errinfo))
        elif respond == 0:
            pass
            # print("无新数据")
            # if self.devtype == 3 or self.devtype == 4:
            #     self.emptynum = self.emptynum + 1
            #     temp = self.emptynum // 20
            #     sys.stdout.write('\r' + "无新数据" + "." * temp)
            #     sys.stdout.flush()
        elif respond > 0:
            pass
            # 写入自己的代码 处理接收到的CAN数据
        return respond

    @issucceed("发送CAN帧")
    def transmit(self,frame_num=1):
        return self.CANdll.VCI_Transmit(self.devtype, self.devindex, self.canindex, byref(self.sendbuf), frame_num)

    @issucceed("读取错误")
    def readerrinfo(self):
        return self.CANdll.VCI_ReadErrInfo(self.devtype, self.devindex, self.canindex, byref(self.errinfo))

    @issucceed("设定E-U波特率")
    def setreference(self):
        return self.CANdll.VCI_SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))

    @issucceed("关闭CAN卡")
    def __del__(self):
        return self.CANdll.VCI_CloseDevice(self.devtype, self.devindex)