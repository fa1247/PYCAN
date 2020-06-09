# PYCAN
利用 ctypes 和周立功提供的 dll 文件实现利用 Python 控制 ZLG USBCAN 的功能。
- CANstruct.py 为对照手册定义的相关结构体
- ControlCAN.py 为对照手册定义的相关函数
- 支持的 CAN 卡为 USBCAN1、USBCAN2、USBCAN2E-U,其他CAN卡应可使用但未经测试
- 支持的函数为 opendevice、initcan、startcan、resetcan、readboardinfo、receive、transmit、readerrinfo、setreference、getreceivenum
- 工程自带周立功官网提供的64位库文件，需要使用64位 Python 调用，如需32位 Python 调用32位库文件，请下载 [zlg-can CAN_lib.rar](http://www.zlg.cn/data/upload/software/Can/CAN_lib.rar) 并替换
- 如需CANFD功能，可使用Github上另一项目 [zlgcan_py](https://github.com/guochuangjian/zlgcan_py)

## 简单使用介绍
ControlCAN.py文件为核心，其中定义了名为 ControlCAN 的类，对于CAN卡的控制通过调用此类中的方法实现，在其他文件中 import 即可使用。
### 类的实例化
```python
from ControlCAN import ControlCAN

can = ControlCAN(can_devtype, can_devindex, can_canindex, can_baudrate, can_acccode, can_accmask)
```
通过以上代码可以实例化一个 ControlCAN 类，对 CAN 卡的所有控制函数都写在类的方法中，方法命名对应周立功手册内的函数，包括传入参数均与周立功手册相同。
实例化的过程中会自动调用 __init__ 方法，传入参数分别为 设备类型 can_devtype、设备号 can_devindex、端口号 can_canindex、波特率 baudrate、接收码 can_acccode、屏蔽码 can_accmask。
#### can_devtype
设备类型，由数字定义，如USBCAN-2E-U编号21，CANET-TCP编号17，目前此参数只接受设备编号，请自行查找对应编号传入。以后会完善代码接受字符串类型的CAN卡名称
#### can_devindex
设备序号，你控制的CAN卡是电脑上的第几个CAN卡，此参数就是几，默认为0，第一个CAN卡默认会是电脑上的第0个设备
#### can_canindex
CAN端口序号，你控制的是CAN卡上的第几个口，此参数就是几，默认为0，如果是2E-U，可能为0、1，如果4E-U，可能为0、1、2、3
#### baudrate
波特率，接受参数为整数，单位为Kbps。比如波特率为250K，则此参数为250
#### can_acccode
接收码，和屏蔽码一起决定了可以接收的ID，具体配置请查阅手册
#### can_accmask
同上

### 打开设备
```python
can.opendevice()
```
打开设备不需要传入参数，因为必须的参数已在实例化时确定
### 初始化设备
```python
can.initcan()
```
无需传入参数
### 启动CAN卡
```python
can.startcan()
```
无需传入参数
### 复位CAN卡
```python
can.resetcan()
```
无需传入参数
### 获取设备信息
```python
can.readboardinfo()
```
无需传入参数
### 获取缓存区帧数
```python
can.getreceivenum()
```
无需传入参数
### 读取错误
```python
can.readerrinfo()
```
无需传入参数
### 设定 E-U 波特率
```python
can.setreference()
```
无需传入参数，此函数只在设定 XE-U 型 CAN 卡的波特率时使用，此函数还有其他功能，请参考官方手册
### 关闭CAN卡
```python
del can
```
删除实例时会自动调用 __del__ 方法，此方法会关闭 CAN 卡
### 接收数据
 ```python
 res = can.receive()
 for i in range(res):
     print(can.receivebuf[i])
     print(can.receivebuf[i].getdata())
 ```
 无需传入参数，此函数的返回值为缓存区内的帧数，如果为0，说明缓存区没有新数据；如果为0xFFFFFFFF，说明有错误；如果为大于0的整数，说明缓存区内有数据，且数据会被存入 ControlCAN 的 receivebuf 这个实例变量中。在主程序中读取此变量即可获得新的数据。receivebuf 是一个 VCI_CAN_OBJ 结构体，其内部的 fields 包含了 CAN 帧的数据。
调用 VCI_CAN_OBJ 的 getdata 方法可以得到一个 list，元素为 CAN 帧数据，整数。
### 发送数据
```python
can.sendbuf[0].ID = 0x123
can.sendbuf[0].DataLen = 8
can.sendbuf[0].Data[0] = 0x00
can.sendbuf[0].Data[1] = 0x11
can.sendbuf[0].Data[2] = 0x22
can.sendbuf[0].Data[3] = 0x33
can.sendbuf[0].Data[4] = 0x44
can.sendbuf[0].Data[5] = 0x55
can.sendbuf[0].Data[6] = 0x66
can.sendbuf[0].Data[7] = 0x77

can.sendbuf[1].ID = 0x321
can.sendbuf[1].setdata([1,2,3,4,5,6,7,8])

can.transmit(frame_num=2)
```
在发送前应设置发送帧的 ID，数据等。 VCI_CAN_OBJ 同样有一个 setdata 方法，可以将传入的 list 分别赋值给 Data ，Datalen自动设定为 list 长度。transmit 方法有一个参数 frame_num，其值为想要发送的帧数，默认为1。
