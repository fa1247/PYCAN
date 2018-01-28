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
                return '硬件版本号：%s,固件版本号：%s,驱动程序版本号：%s,接口库版本号：%s,中断号：%s,共有%s路CAN，序列号：%s,硬件类型：%s'%(self.hw_Version,self.fw_Version,self.dr_Version,self.in_Version,self.irq_Num,self.can_Num,self.str_Serial_Num,self.str_hw_Type)


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
        datalist = []
        for i in range(self.DataLen):
            datalist.append(self.Data[i])
        return 'ID:%08X,时间戳:%X,数据长度:%X,数据:%02X %02X %02X %02X %02X %02X %02X %02X'%(self.ID,self.TimeStamp,self.DataLen,self.Data[0],self.Data[1],self.Data[2],self.Data[3],self.Data[4],self.Data[5],self.Data[6],self.Data[7])


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