from CANstruct import *
from collections import OrderedDict
from loguru import logger


def issucceed(func_name):
    def deco(func):
        def wrapper(self,*args):
            if func(self,*args):
                logger.info('{}成功',func_name)
                # print(func_name+"成功")
            else:
                logger.error('{}失败',func_name)
                # print(func_name+"失败")
        return wrapper
    return deco


class CANHandler:

    @logger.catch
    def __init__(self,dllpath='ControlCAN.dll'):
        self._CANdll = WinDLL(dllpath)
        self._CANdict = OrderedDict()
    
    def get_candict(self):
        return self._CANdict

    def get_can(self,channelname=None):
        if channelname is None:
            logger.warning('未指定通道名称，默认返回第一个通道')
            channelname = self._CANdict.keys()[0]
        return self._CANdict[channelname]

    def create_can(self,channelname=None ,devtype=3, devindex=0, canindex=0, baudrate=250, acccode=0x00000000, accmask=0xFFFFFFFF):
        channelname = f'CAN{len(self._CANdict)}' if channelname is None else channelname
        can = ControlCAN(CANdll=self._CANdll ,devtype=devtype, devindex=devindex, canindex=canindex, baudrate=baudrate, acccode=acccode, accmask=accmask)
        self._CANdict[channelname] = can
        return can

    def destroy_can(self,channelname=None):
        if channelname is None:
            logger.warning('未指定通道名称，默认关闭第一个通道')
            channelname = self._CANdict.keys()[0]
        self._CANdict[channelname].closedevice()
        self._CANdict = self._CANdict.pop(channelname)

    def destroy_all(self):
        for channelname, can in self._CANdict.items():
            can.closedevice()
            self._CANdict = self._CANdict.pop(channelname)
        if len(self._CANdict) == 0:
            logger.info('已关闭所有通道')
        else:
            logger.error('有未关闭通道')




class ControlCAN:

    def __init__(self,CANdll=None ,devtype=3, devindex=0, canindex=0, baudrate=250, acccode=0x00000000, accmask=0xFFFFFFFF):
        time0 = {100: 0x04, 125: 0x03, 250: 0x01, 500: 0x00, 1000: 0x00}
        time1 = {100: 0x1C, 125: 0x1C, 250: 0x1C, 500: 0x1C, 1000: 0x14}
        pData = {100: 0x160023, 125: 0x1C0011, 250: 0x1C0008, 500: 0x060007, 1000: 0x060003}
        if CANdll == None:
            self.CANdll = WinDLL('ControlCAN.dll')
        else:
            self.CANdll = CANdll
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
        elif respond > 0:
            pass
            # 写入自己的代码 处理接收到的CAN数据
        return respond

    @issucceed("发送CAN帧")
    def transmit(self,canid=None,candata=None,frame_num=1):
        if canid is None and candata is None:
            return self.CANdll.VCI_Transmit(self.devtype, self.devindex, self.canindex, byref(self.sendbuf), frame_num)
        else:
            assert isinstance(canid,int), 'CAN ID 需为整数'
            assert isinstance(candata,list), 'CAN DATA 需为list类型，内部数据为整数'
            assert frame_num==1, '使用此种方法只能发送一帧数据'
            self.sendbuf.ID = canid
            self.sendbuf.setdata(candata)
            return self.CANdll.VCI_Transmit(self.devtype, self.devindex, self.canindex, byref(self.sendbuf), 1)

    @issucceed("读取错误")
    def readerrinfo(self):
        return self.CANdll.VCI_ReadErrInfo(self.devtype, self.devindex, self.canindex, byref(self.errinfo))

    @issucceed("设定E-U波特率")
    def setreference(self):
        return self.CANdll.VCI_SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))

    @issucceed("关闭CAN卡")
    def closedevice(self):
        return self.CANdll.VCI_CloseDevice(self.devtype, self.devindex)

    def __del__(self):
        self.closedevice()