import struct
import pymodbus.client.sync
import time
import sys
import datetime
import sqlite3


def read_float_reg(client, unit=1):
    resp = client.read_input_registers(0x0c, 2, unit=1)
    if resp is None:
        return None
    # according to spec, each pair of registers returned
    # encodes a IEEE754 float where the first register carries
    # the most significant 16 bits, the second register carries the
    # least significant 16 bits.
    return struct.unpack('>f', struct.pack('>HH', *resp.registers))


def main():
    # if client is set to odd or even parity, set stopbits to 1
    # if client is set to 'none' parity, set stopbits to 2
    cl = pymodbus.client.sync.ModbusSerialClient(method='rtu', port='/dev/ttyUSB0',
                                                 baudrate=9600, parity='N',
                                                 stopbits=2, timeout=0.125)
    while True:
        value = read_float_reg(cl, unit=1)
        date = datetime.datetime.now()
        date_str = str(str(date.day)+'/'+str(date.month)+'/'+str(date.year))
        time_str = time.strftime('%H:%M:%S')
        print(date_str+' '+time_str+' '+(str(value[0])))
        write_bd(date_str, time_str, value[0])
        sys.stdout.flush()
        time.sleep(1)


def write_bd(date, tm, power):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute("INSERT into Electr values (?, ?, ?)", (date, tm, power))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
