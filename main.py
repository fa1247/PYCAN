from ControlCAN import *
import pymysql


def main():
    db = pymysql.connect("localhost", "root", "fanxinyuan", "candata")
    cursor = db.cursor()
    Opendevice()
    Initcan()
    Startcan()
    num = Receive()

    for i in range(num):
        sql = "INSERT INTO %s(ID,TimeStamp,DataLen,Data0,Data1,Data2,Data3,Data4,Data5,Data6,Data7)\
                          VALUES('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" % \
              ('originaldata', \
               receivebuf[i].ID,\
               receivebuf[i].TimeStamp,\
               receivebuf[i].DataLen,\
               receivebuf[i].Data[0],\
               receivebuf[i].Data[1],\
               receivebuf[i].Data[2],\
               receivebuf[i].Data[3],\
               receivebuf[i].Data[4],\
               receivebuf[i].Data[5],\
               receivebuf[i].Data[6],\
               receivebuf[i].Data[7])
        cursor.execute(sql)
    db.commit()

    Closedevice()
    db.close()


def debug():
    for f, t in Req._fields_:
        a = getattr(VCI_INIT_CONFIG, f)
        print(a)

if __name__ == "__main__":
    main()
