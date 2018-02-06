import pymysql
from CANstruct import *


class StorageToSQL:

    def __init__(self, ip = 'localhost',username='root', password='fanxinyuan', schema='candata', rtable='originaldata',ttable='turedata', buffersize=1000):
        self.datanum = 0
        self.ip = ip
        self.buffersize = buffersize
        self.schema = schema
        self.rtable = rtable
        self.ttable = ttable
        self.db = pymysql.connect("localhost", username, password, schema)
        self.cursor = self.db.cursor()
        self.storagebuf = (VCI_CAN_OBJ * 50)()
        print('连接数据库成功')

    def createtable(self):
        sql = "DROP TABLE IF EXISTS %s" % self.rtable
        self.cursor.execute(sql)
        sql = "CREATE TABLE `%s`.`%s` (\
            `INDEX` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
            `RealTime` TIMESTAMP(6) NOT NULL,\
            `ID` INT UNSIGNED NOT NULL DEFAULT 0,\
            `TimeStamp` INT UNSIGNED NOT NULL DEFAULT 0,\
            `DataLen` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data0` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data1` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data2` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data3` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data4` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data5` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data6` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            `Data7` TINYINT(8) UNSIGNED NOT NULL DEFAULT 0,\
            PRIMARY KEY (`INDEX`));" % (self.schema, self.rtable)
        self.cursor.execute(sql)
        print('创建表格成功')

    def copy(self, obj):
        self.storagebuf = obj

    def storage(self, n):
        self.datanum = self.datanum + n
        for i in range(n):
            sql = "INSERT INTO %s(ID,TimeStamp,DataLen,Data0,Data1,Data2,Data3,Data4,Data5,Data6,Data7)\
                                  VALUES('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" % \
                  (self.rtable,
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

    def commit(self):
        if self.datanum > self.buffersize:
            self.db.commit()
            self.datanum = 0

    def __del__(self):
        self.db.close()
