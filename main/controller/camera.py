import time

import win32com.client


# NEEDS TESTING

class Camera():
    def __init__(self):
        self.Camera = win32com.client.Dispatch("MaxIm.CCDCamera")  # Sets the camera connection path to the CCDCamera
        self.Camera.DisableAutoShutdown = True  # All of these settings are just basic camera setup settings.
        self.Camera.LockApp = True
        self.Camera.CoolerOn = True
        self.Camera.AutoDownload = True

        self.check_connection()
    
    T_0 = -30

    def check_connection(self):
        if self.Camera.LinkEnabled == True:
            print("Camera is connected")
        else:
            print("Camera is not connected")
    
    def coolerSet(self):
        global T_0
        self.Camera.SetCCDTemperature(T_0) #Can use as a method to set the CCD temp., or as a property to call the current setpoint
    
    def coolerAdjust(self): #Heavy wip to find the right way to adjust cooler temp. based on cooler power
        global T_0
        t1 = self.Camera.CCDTemperature #Property to find the current temp. rather than the setpoint
        time.sleep(10)
        t2 = self.Camera.CCDTemperature
        if abs(t1 - t2) > 0.1 or self.Camera.CoolerPower >= 95:
            self.Camera.SetCCDTemperature(T_0 + 5)

    def expose(self, exposure_time, filter, save_path, type="light"):
        if type == "light":
            type = 1
        elif type == "dark":
            type = 0
        else:
            print("ERROR: Invalid exposure type.")
            return
        self.Camera.SetFullFrame()
        self.Camera.Expose(exposure_time, type, filter) #In the pdf it says the method is called "StartExposure(duration,type)"??
        while Camera.ImageReady==False:
            time.sleep(1)
            if Camera.ImageReady:
                Camera.StartDownload
                #TODO: Automate image nomenclature 
                Camera.SaveImage(save_path)

    def set_gain(self):
        self.Camera.SetupDialog #Opens dialog box for user to input settings?  Couldn't find a gain method in the resources pdf.

    def set_binning(self):
        pass