# Copyright (c) 2021-2022  The University of Texas Southwestern Medical Center.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted for academic and research use only (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:

#      * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#      * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.

#      * Neither the name of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived from this
#      software without specific prior written permission.

# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

#Standard Imports
import tkinter as tk
from tkinter import filedialog
import os

#Third-party imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import subprocess
import struct
from threading import Thread

#Local Imports
from navigate.controller.sub_controllers.gui_controller import GUIController

class VastOperatorController(GUIController):
    def __init__(self, view, parent_controller=None):
        super().__init__(view, parent_controller)
        # Get Widgets from view
        #: dict: The widgets in the VAST operator settings frame.
        self.vast_operator_widgets = view.get_widgets()
        #: dict: The values in the VAST operator settings frame.
        self.vast_operator_vals = view.get_variables()
        #Gets Buttons from view
        self.buttons = self.view.buttons

        # laser/stack cycling event binds
       
        
        self.populate_experiment_setting()

      

        # confocal-projection event binds

        #Assign our commands to their corresponding buttons
        self.buttons["vast_storage_dir"].configure(command=self.update_vast_imagefolder)
        self.buttons["start_VAST"].configure(command=self.start_VAST)
        self.buttons["send_VAST_command"].configure(command=self.command_VAST)
        # #: tkinter.Canvas: The tkinter canvas that displays the image.
        # self.canvas = self.view.canvas
        
        # #: int: The width of the canvas.
        # #: int: The height of the canvas.
        # self.width, self.height = 512, 512
        # self.canvas_width, self.canvas_height = (
        #     self.view.canvas_width,
        #     self.view.canvas_height,
        # )
        # self.canvas_width, self.canvas_height = 512, 512

        # self.menu = tk.Menu(self.canvas, tearoff=0)

    def populate_experiment_setting(self):
        """Populate experiment"""

        self.microscope_state_dict = self.parent_controller.configuration["experiment"][
            "MicroscopeState"
        ]
        

    def update_vast_imagefolder(self, *args):
        """Update autostore path for the VAST

        Parameters
        ----------
        *args
            Not used

        Examples
        --------
        self.update_vast_imagefolder()
        """
        vast_storage_dir = tk.StringVar()
        vast_storage_dir = filedialog.askdirectory()
        #self.vast_operator_vals["vast_image_folder"].set(vast_storage_dir)
        self.vast_operator_widgets["VASTsavedir"].config(label=vast_storage_dir)


    def initialize_LPS(self, *args):
        """Launch the Large Particle Sampler(LPS)

        Parameters
        ----------
        *args
            Not used

        Examples
        --------
        >>> self.initialize_LPS()
        """
        
        print("attempting initialization...")
        

    def start_VAST(self, *args):
        """Launch the Large Particle Sampler(LPS)

        Parameters
        ----------
        *args
            Not used

        Examples
        --------
        >>> self.initialize_LPS()
        """
        thread = Thread(target = VastOperatorController.senderthread, args = ("y"))
        thread.start()
        thread.join()
        print("attempting movement...")
        
    def command_VAST(self, *args):
        """Placeholder for eventual command structure. This will eventually set the "commandready variable to true, 
        and also send the command of interest"""
        
        
    def update_image_storage_path(self, *args):
        "Updates path to which files will be saved"
        self.microscope_state_dict[""]

    def update_cycling_setting(self, *args):
        """Update cycling setting"""
        self.microscope_state_dict["conpro_cycling_mode"] = (
            "per_stack"
            if self.vast_operator_vals["cycling"].get() == "Per Stack"
            else "per_plane"
        )

    def set_widget_value(self, widget_name):
        """Set widget value from experiment
        
        Parameters
        ----------
        widget_name : str
            widget name (same as in the experiment.yml)
        """
        try:
            widget_value = float(self.microscope_state_dict[widget_name])
        except:
            widget_value = 0

        self.vast_operator_vals[widget_name].set(widget_value)
    
    def senderthread(Response):
        if(Response == "y" or Response == "Y"):        
            f = VastOperatorController.Startup_Vinterop(True)
        else:
            f = VastOperatorController.Startup_Vinterop(False)
        while True:
                s = input("Enter a command:") 
                f.write(struct.pack('I', len(s)) + s.encode(encoding="ascii"))   # Write str length and str
                f.seek(0)                               # EDIT: This is also necessary
                print('Writing: ', s)
                n = struct.unpack('I', f.read(4))[0]    # Read str length
                s = f.read(n)                           # Read str
                f.seek(0)                               # Important!!!
                s.decode("ascii")
                print("Reloaded!")
    
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