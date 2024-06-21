# Standard Imports
import os
from pathlib import Path
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb

from threading import Thread
import time
import os
import struct
import subprocess


from navigate.tools.common_functions import load_module_from_file
from navigate.model.device_startup_functions import device_not_found

import subprocess;

DEVICE_TYPE_NAME = "LPS"  # Same as in configuraion.yaml, for example "stage", "filter_wheel", "remote_focus_device"...
DEVICE_REF_LIST = ["type"]  # the reference value from configuration.yaml


def load_device(configuration, is_synthetic=False):
    """Build device connection(In this case, the program begins a thread which manages this side of the Interoperator).
    
    Returns
    -------
    device_connection : object
    """
    #Asks if user would like to boot LPS/VAST on startup
    
    # res=mb.askquestion("Launch the LP Sampler and VAST BioImager?\n(You can disable this startup request off by going to config -> LPS and setting InitStartup to false)")

    
def start_device(microscope_name, device_connection, configuration, is_synthetic=False):
    """Start device.

    Returns
    -------
    device_object : object
    """
    if is_synthetic:
        device_type = "synthetic"
    else:
        device_type = configuration["configuration"]["microscopes"][microscope_name][
            "plugin_device"
        ]["hardware"]["type"]

    if device_type == "UnionBio":
        plugin_device = load_module_from_file(
            "plugin_device",
            os.path.join(Path(__file__).resolve().parent, "plugin_device.py"),
        )
        return plugin_device.PluginDevice(device_connection=device_connection)
    elif device_type == "synthetic":
        synthetic_LPS = load_module_from_file(
            "synthetic_device",
            os.path.join(Path(__file__).resolve().parent, "LPS_synthetic.py"),
        )
        return synthetic_LPS.SyntheticLPS(device_connection=device_connection)
    else:
        return device_not_found(microscope_name, device_type)

def Startup_Vinterop(subprocess_start):
    if(subprocess_start):    
        connection_init = False
        Holster = "E:\\TestAutoSampIntegration\\bin\\Debug\\TestAutoSampIntegration"
        LPSVAST = subprocess.Popen(Holster)
        time.sleep(3)
        while not connection_init:
            try:
                f = open(r'\\.\pipe\VASTInteropPipe', 'r+b', 0) 
                connection_init = True
            except:
                user_response = input("Could not connect to server, would you like to reboot the holster('boot') or try again('y'/'Y')?")
                if(user_response == "y" or user_response == "Y"):
                    time.sleep(1)
                elif user_response == "boot":
                    Holster = "E:\\TestAutoSampIntegration\\bin\\Debug\\TestAutoSampIntegration"
                    LPSVAST = subprocess.Popen(Holster)
                    time.sleep(2)
                else:
                    break;
    else:
        f = open(r'\\.\pipe\VASTInteropPipe', 'r+b', 0)
    return(f)
    
def senderthread(Response):
    if(Response == "y" or x == "Y"):        
        f = Startup_Vinterop(True)
    else:
        f = Startup_Vinterop(False) 
    while True:
            time.sleep(30)
            s = input("Enter a command:") 
            f.write(struct.pack('I', len(s)) + s.encode(encoding="ascii"))   # Write str length and str
            f.seek(0)                               # EDIT: This is also necessary
            print('Writing: ', s)
            n = struct.unpack('I', f.read(4))[0]    # Read str length
            s = f.read(n)                           # Read str
            f.seek(0)                               # Important!!!
            s.decode("ascii")
            print("Reloaded!")