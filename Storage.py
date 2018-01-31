import pymysql
from CANstruct import *


class StorageToSQL:

    def __init__(self, username='root', password='fanxinyuan', schema='candata', table='originaldata'):
        self.schema=schema
        self.table = table
        self.db = pymysql.connect("localhost", username, password, schema)
        self.cursor = self.db.cursor()
        self.storagebuf = (VCI_CAN_OBJ * 50)()
        print('连接数据库成功')

    def createtable(self):
        sql="DROP TABLE IF EXISTS %s"%(self.table)
        self.cursor.execute(sql)
        sql = "CREATE TABLE `%s`.`%s` (\
            `INDEX` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
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
            PRIMARY KEY (`INDEX`));"%(self.schema,self.table)
        self.cursor.execute(sql)
        print('创建表格成功')

    def copy(self, obj):
        self.storagebuf = obj

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
