import ajiledriver as aj
import numpy as np
import os
import cv2
import time
import sys

class AJ_DMD:
    def __init__(self):        
        self.aj_trig=aj.EXT_TRIGGER_OUTPUT_1
        self.frametime = 10
        self.Connect_DMD()
        self.timeout=20
        self.custom_xy = False
        
    def Connect_DMD(self):
        self.sequenceID = 1
        self.ajs = aj.HostSystem()#build object
        self.driver = self.ajs.GetDriver()#build object
        self.ajs.SetCommunicationInterface(aj.USB3_INTERFACE_TYPE)#setup connection
        if self.ajs.StartSystem() != aj.ERROR_NONE:#initiate connection
            print ("Error starting self.ajs.")
            sys.exit(-1)
    def Disconnect_DMD(self):
        self.ajs.StopSystem()
        
    def Get_Seq_RunState(self):
        return self.ajs.GetDeviceState(self.dmdIndex).RunState()
        
    def Init_Project(self):
        self.project = aj.Project("DMD_Stream")#create project
        self.project.SetComponents(self.ajs.GetProject().Components())#read device components
        self.dmdIndex = self.ajs.GetProject().GetComponentIndexWithDeviceType(aj.DMD_4500_DEVICE_TYPE)#copy list of components
        if self.dmdIndex < 0:
            self.dmdIndex = self.ajs.GetProject().GetComponentIndexWithDeviceType(aj.DMD_3000_DEVICE_TYPE)
        self.driver.LoadImageStorageSize(0x00001000, 0, -1)
        self.driver.LoadImageStorageSize(0x00001000, self.dmdIndex, -1)        
        time.sleep(1)
        self.controllerComponent = self.project.Components()[0]
        self.controllerComponent.SetImageMemorySize(0x00001000)#Hex value of data size (8-bit data with 912x1140 elements=1000 bytes)
        self.project.SetComponent(0, self.controllerComponent)
        self.dmdComponent = self.project.Components()[self.dmdIndex]
        self.dmdComponent.SetImageMemorySize(0x1ffff000)#holds up to 8000 8-bit images
        self.project.SetComponent(1, self.dmdComponent)
        self.driver.LoadImageStorageSize(self.controllerComponent.ImageMemorySize(), 0, -1)
        self.driver.LoadImageStorageSize(self.dmdComponent.ImageMemorySize(), self.dmdIndex, -1)
        time.sleep(1)
        self.driver.StopSequence(self.dmdIndex)
        while self.ajs.GetDeviceState(self.dmdIndex).RunState() != aj.RUN_STATE_STOPPED: pass
        for index, component in enumerate(self.project.Components()):
            self.deviceType = component.DeviceType().HardwareType()
            if self.deviceType == aj.AJILE_CONTROLLER_DEVICE_TYPE or \
               self.deviceType == aj.AJILE_2PORT_CONTROLLER_DEVICE_TYPE or \
               self.deviceType == aj.AJILE_3PORT_CONTROLLER_DEVICE_TYPE:
               controllerIndex = index
        inputTriggerSettings = self.project.Components()[controllerIndex].InputTriggerSettings()
        outputTriggerSettings = self.project.Components()[controllerIndex].OutputTriggerSettings()
        for index in range(len(outputTriggerSettings)):
            if self.frametime//2 <1:
                outputTriggerSettings[index] = aj.ExternalTriggerSetting(aj.RISING_EDGE, aj.FromUSec(self.frametime*500))
            else:
                outputTriggerSettings[index] = aj.ExternalTriggerSetting(aj.RISING_EDGE, aj.FromMSec(self.frametime*0.5))
        self.project.SetTriggerSettings(controllerIndex, inputTriggerSettings, outputTriggerSettings)
        dmdSeqItemStartedToExtTrigOut = aj.TriggerRule()
        dmdSeqItemStartedToExtTrigOut.AddTriggerFromDevice(aj.TriggerRulePair(self.dmdIndex, aj.FRAME_STARTED))
        dmdSeqItemStartedToExtTrigOut.SetTriggerToDevice(aj.TriggerRulePair(controllerIndex, self.aj_trig))
        self.project.AddTriggerRule(dmdSeqItemStartedToExtTrigOut)   
        self.imageWidth = self.ajs.GetProject().Components()[self.dmdIndex].NumColumns()
        self.imageHeight = self.ajs.GetProject().Components()[self.dmdIndex].NumRows()
        self.deviceType = self.ajs.GetProject().Components()[self.dmdIndex].DeviceType().HardwareType()
        self.project.AddSequence(aj.Sequence(self.sequenceID, "DMD_Stream", self.deviceType, aj.SEQ_TYPE_STREAM, 1, aj.SequenceItemList(), aj.RUN_STATE_STOPPED))
        self.driver.LoadProject(self.project)#load project onto board
        self.driver.WaitForLoadComplete(self.timeout)

    def Load_Streaming(self,H):
        print('Uploading Images')
        for k in range(H.shape[2]):
            streamingImage = aj.Image()#creat image object
            if H.shape[0] != self.imageWidth and H.shape[1] != self.imageHeight:
                img = H[:,:,k].astype(float)#pull the next hadamard matrix item
                if self.custom_xy:
                    imgp=(np.zeros(shape=(self.imageWidth,self.imageHeight))).astype(np.uint8)
                    temp = cv2.resize(img,(self.X,self.Y),interpolation=cv2.INTER_AREA)#resize it to the size of DMD
                    imgp[int((912-self.Y)//2):912-int((912-self.Y)//2),int((1140-self.X)//2):1140-int((1140-self.X)//2)]=temp
                else: 
                    imgp = cv2.resize(img,(912,1140),interpolation=cv2.INTER_AREA)#resize it to the size of DMD
            else: 
                imgp = H[:,:,k].astype(int)
            npz=(255*np.array(imgp).astype(int)).astype(np.uint8)
            timg = np.ascontiguousarray(np.expand_dims(npz,axis=2)).astype(np.uint8)
            streamingImage.ReadFromMemory(timg,8,aj.ROW_MAJOR_ORDER,self.deviceType)
            streamingSeqItem = aj.SequenceItem(self.sequenceID, 1)
            if self.frametime//2<1:    
                streamingFrame = aj.Frame(self.sequenceID, 0, aj.FromUSec(self.frametime*1e3), 0, 0, self.imageWidth, self.imageHeight)
            else:
                streamingFrame = aj.Frame(self.sequenceID, 0, aj.FromMSec(self.frametime), 0, 0, self.imageWidth, self.imageHeight)
            streamingFrame.SetStreamingImage(streamingImage)
            streamingSeqItem.AddFrame(streamingFrame)
            self.driver.AddStreamingSequenceItem(streamingSeqItem, self.dmdIndex)

