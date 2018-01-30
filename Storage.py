import pymysql
from CANstruct import *


class StorageToSQL:

    def __init__(self, username='root', password='fanxinyuan', schema='candata', table='originaldata'):
        self.table = table
        self.db = pymysql.connect("localhost", username, password, schema)
        self.cursor = self.db.cursor()
        self.storagebuf = (VCI_CAN_OBJ * 50)()

    def copy(self, n, obj):
        for i in range(n):
            self.storagebuf[i] = obj[i]

    def storage(self, n):
        for i in range(n):
            sql = "INSERT INTO %s(ID,TimeStamp,DataLen,Data0,Data1,Data2,Data3,Data4,Data5,Data6,Data7)\
                                  VALUES('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" % \
                  (self.table,
                   self.storagebuf[i].ID,
                   self.storagebuf[i].TimeStamp,
                   self.storagebuf[i].DataLen,
                   self.storagebuf[i].Data[0],
                   self.storagebuf[i].Data[1],
                   self.storagebuf[i].Data[2],
                   self.storagebuf[i].Data[3],
                   self.storagebuf[i].Data[4],
                   self.storagebuf[i].Data[5],
                   self.storagebuf[i].Data[6],
                   self.storagebuf[i].Data[7])
            self.cursor.execute(sql)
        self.db.commit()

    def __del__(self):
        self.db.close()
