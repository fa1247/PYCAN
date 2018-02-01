from ControlCAN import *
from Storage import *
import msvcrt

def main():
    sql=StorageToSQL()
    sql.createtable()
    start=time.clock()
    i = 0
    while i<1000:
        sql.storage(3)
        i = i+1
        print(i)
    sql.commit()
    stop =time.clock()
    print(stop-start)
    del sql


def main2():
    sql = StorageToSQL()
    sql.createtable()
    can = ControlCAN()
    can.opendevice()
    can.initcan()
    can.startcan()
    while 1:
        if kbq(): break
        num = can.receive()
        sql.copy(can.receivebuf)
        sql.storage(num)
        sql.commit()
    del can
    del sql


def kbq():
    if msvcrt.kbhit():
        ret = ord(msvcrt.getch())
        if ret == 113 or ret == 81:  # q or Q
            return 1
    else:
        return 0


def inputpara():

    a = input("设备型号：1.USBCAN1(默认);2.USBCAN2;3.USBCAN2E-U;请输入:")
    if a == 1:
        devicetype = 3
    elif a == 2:
        devicetype = 4
    elif a == '':
        print(type(a))
        print(a)


if __name__ == "__main__":
    main()
