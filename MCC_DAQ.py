import numpy as np
import os
import sys
from ctypes import cast, POINTER, c_double, c_ushort, c_ulong
import shutil
import time
from mcculw import ul
from mcculw.enums import ScanOptions, FunctionType, Status, InterfaceType, ULRange, AnalogInputMode, TriggerSource, TriggerEvent, TriggerSensitivity
from mcculw.ul import ULError, a_input_mode
from mcculw.device_info import DaqDeviceInfo


class MCC_DAQ:
    def __init__(self):
        self.rate = 10e3
        self.Nsamp = int(5e4)
        self.board_num=0
        self.low_chan=0
        self.high_chan=1
        ul.ignore_instacal()#ignores their crappy software
        daqdevice = ul.get_daq_device_inventory(InterfaceType.USB)#find DAQ
        ul.create_daq_device(self.board_num, daqdevice[0])#create DAQ handle for python
        dev_info = DaqDeviceInfo(0)#for debugging
        ai_info = dev_info.get_ai_info()#for debugging
        ai_range = ai_info.supported_ranges[0]#for debugging
        self.memhandle = ul.scaled_win_buf_alloc(self.Nsamp)#buffer handle (direct access to buffer - be careful!)
        if not self.memhandle:
            print("Error: Failed to allocate DAQ memory")
            sys.exit(-1)
        self.buf_data = cast(self.memhandle,POINTER(c_double))#create buffer to copy data to
        self.scan_options = ScanOptions.CONTINUOUS | ScanOptions.BACKGROUND | ScanOptions.SCALEDATA

        def Start_DAQUISITION(self):
            ul.a_in_scan(self.board_num, self.low_chan, self.high_chan, self.Nsamp,
                self.rate, ULRange.BIP10VOLTS, self.memhandle, self.scan_options)#function to setup analog scan

        def Grab_Data(self):
            ul.scaled_win_buf_to_array(self.memhandle, self.buf_data, 0, int(self.Nsamp))#copy data from memhandle buffer to local buffer
            data = np.asarray(self.buf_data[0:int(self.N)])#turn data in buffer to a np array
            ul.stop_background(self.board_num, FunctionType.AIFUNCTION)#stop recording the DAQ
            ul.win_buf_free(self.memhandle)#release the buffer to prevent crashing system
            return data
        