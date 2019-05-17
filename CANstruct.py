from ctypes import *
from ctypes.wintypes import DWORD


class Req(Structure):
    _fields_ = [('uRouter', c_ubyte, 1),
                ('uSubNode', c_ubyte, 1),
                ('uCM', c_ubyte, 1),
                ('uCD', c_ubyte, 1),
                ('uLevel', c_ubyte, 4),
                ('uChannel', c_ubyte, 4),
                ('uErrBate', c_ubyte, 4),
                ('uResBytes', c_ubyte),
                ('uSpeed', c_ushort, 15),
                ('uUnit', c_ushort, 1),
                ('uReserve', c_ubyte)]


class VCI_BOARD_INFO(Structure):
    _fields_ = [('hw_Version', c_ushort),
                ('fw_Version', c_ushort),
                ('dr_Version', c_ushort),
                ('in_Version', c_ushort),
                ("irq_Num", c_ushort),
                ('can_Num', c_byte),
                ('str_Serial_Num', c_char * 20),
                ('str_hw_Type', c_char * 40),
                ('Reserved', c_ushort * 4)]

    def __str__(self):
        return '硬件版本号：%s,固件版本号：%s,驱动程序版本号：%s,接口库版本号：%s,中断号：%s,共有%s路CAN，序列号：%s,硬件类型：%s' % (
            self.hw_Version, self.fw_Version, self.dr_Version, self.in_Version, self.irq_Num, self.can_Num,
            self.str_Serial_Num, self.str_hw_Type)


class VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_ubyte * 8),
                ('Reserved', c_byte * 3)]

    def __str__(self):
        datastr = ''
        for i in range(self.DataLen):
            datastr += format(self.Data[i],'02X')+" "
        return 'ID:%08X,时间戳:%X,长度:%X,数据:%s'%(self.ID, self.TimeStamp, self.DataLen, datastr)

    def getdata(self):
        return [self.Data[i] for i in range(self.DataLen)]
    
    def setdata(self,datalist):
        self.DataLen = len(datalist)
        for i in range(self.DataLen):
            self.Data[i] = datalist[i]


class VCI_CAN_STATUS(Structure):
    _fields_ = [('ErrInterrupt', c_ubyte),
                ('regMode', c_ubyte),
                ('regStatus', c_ubyte),
                ('regALCapture', c_ubyte),
                ('regECCapture', c_ubyte),
                ('regEWLimit', c_ubyte),
                ('regRECounter', c_ubyte),
                ('regTRCounter', c_ubyte),
                ('Reserved', c_ulong)]


class VCI_ERR_INFO(Structure):
    _fields_ = [('ErrCode', c_uint),
                ('Passive_ErrData', c_byte * 3),
                ('ArLost_ErrData', c_byte)]


class VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', DWORD),
                ('AccMask', DWORD),
                ('Reserved', DWORD),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]


class CHGDESIPANDPORT(Structure):
    _fields_ = [('szpwd', c_char * 10),
                ('szdesip', c_char * 20),
                ('desport', c_int),
                ('blisten', c_byte)]


class VCI_FILTER_RECORD(Structure):
    _fields_ = [('ExtFrame', DWORD),
                ('Start', DWORD),
                ('End', DWORD)]

class VCI_AUTO_SEND_OBJ(Structure):
    _fields_ = [('Enable', c_byte),
                ('Index', c_byte),
                ('Interval', DWORD),
                ('Obj', VCI_CAN_OBJ)]

class VCI_INDICATE_LIGHT(Structure):
    _fields_ = [('Indicate', c_byte),
                ('AttribRedMode', c_byte, 2),
                ('AttribGreenMode', c_byte, 2),
                ('AttribReserved', c_byte, 4),
                ('FrequenceRed', c_byte, 2),
                ('FrequenceGreen', c_byte, 2),
                ('FrequenceReserved', c_byte, 4)]

class VCI_CAN_OJB_REDIRECT(Structure):
    _fields_ = [('Action', c_byte),
                ('DestCanIndex', c_byte)]

class DTUCOMCONFIG(Structure):
    _fields_ = [('dwLen', DWORD),
                ('pData', POINTER(c_byte))]
