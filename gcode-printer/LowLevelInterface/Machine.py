import sys
import logging
import re
import serial
import time

__author__ = 'marcus'

_default_serial_port = "/dev/ttyO1"
_default_timeout = 5


def matcher(buff):
    pass


class MachineError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Machine():
    _commandEndMatcher = re.compile(";")    #needed to search for command ends

    def __init__(self, serialport=None):
        if serialport is None:
            serialport = _default_serial_port
        self.serialport = serialport

    def connect(self):
        self.machineSerial = serial.Serial(self.serialport, 115200, timeout=_default_timeout)
        line = self.doRead()   # read a ';' terminated line
        logging.info(line)
        command = MachineCommand(line)
        if not command.return_code is -128:
            raise MachineError("Machine does not seem ready")

    def doRead(self):
        buff = ""
        tic = time.time()
        buff += self.machineSerial.read(128)

        # you can use if not ('\n' in buff) too if you don't like re
        while ((time.time() - tic) < _default_timeout) and (not self._commandEndMatcher.search(buff)):
            print >> sys.stdout, (time.clock() - tic) * 60
            buff += self.machineSerial.read(128)

        return buff


class MachineCommand():
    def __init__(self, input_line):
        parts = input_line.strip().split(",")
        self.return_code = int(parts[0])
        self.arguments = parts[1:]