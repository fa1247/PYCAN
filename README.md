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
