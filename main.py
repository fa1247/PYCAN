from ControlCAN import *
from multiprocessing import Process
import pymysql


def main():
    num = 1
    sql = SrorageToSQL()
    sql.storage(num)
    sql.disconnect()


def main2():
    opendevice()
    initcan()
    startcan()
    num = receive()
    closedevice()


class SrorageToSQL:

    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "fanxinyuan", "candata")
        self.cursor = self.db.cursor()

    def storage(self, n):
        for i in range(n):
            storagebuf[i] = receivebuf[i]
        for i in range(n):
            sql = "INSERT INTO %s(ID,TimeStamp,DataLen,Data0,Data1,Data2,Data3,Data4,Data5,Data6,Data7)\
                                  VALUES('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" % \
                  ('originaldata',
                   storagebuf[i].ID,
                   storagebuf[i].TimeStamp,
                   storagebuf[i].DataLen,
                   storagebuf[i].Data[0],
                   storagebuf[i].Data[1],
                   storagebuf[i].Data[2],
                   storagebuf[i].Data[3],
                   storagebuf[i].Data[4],
                   storagebuf[i].Data[5],
                   storagebuf[i].Data[6],
                   storagebuf[i].Data[7])
            self.cursor.execute(sql)
        self.db.commit()

    def disconnect(self):
        self.db.close()


def debug():
    for f, t in Req._fields_:
        a = getattr(VCI_INIT_CONFIG, f)
        print(a)


if __name__ == "__main__":
    main()
