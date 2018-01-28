from ControlCAN import *


def main2():
    for f, t in VCI_INIT_CONFIG._fields_:
        a = getattr(VCI_INIT_CONFIG, f)
        print(a)


def main():
    Opendevice()
    Initcan()
    Startcan()
    while 1:
        Receive()
    Closedevice()


if __name__ == "__main__":
    main()
