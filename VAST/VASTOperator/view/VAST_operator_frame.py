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

# Standard Imports
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

#Third Party Imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


#Local Imports
from navigate.view.custom_widgets.hover import Hover
from navigate.view.custom_widgets.hovermixin import HoverButton
from navigate.view.custom_widgets.validation import ValidatedSpinbox, ValidatedCombobox
from navigate.view.custom_widgets.LabelInputWidgetFactory import LabelInput


class VastOperatorFrame(ttk.Labelframe):
    """Confocal Projection Acquisition Frame

    This frame contains the widgets for the confocal projection acquisition settings.
    """

    def __init__(self, settings_tab, *args, **kwargs):
        """Initilization of the Confocal Projection Frame

        Parameters
        ----------
        settings_tab : tkinter.ttk.Frame
            The frame that this frame will be placed in.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        # Init Frame
        text_label = (
            "VAST Operator"
        )
        ttk.Labelframe.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Dictionary for widgets and buttons
        #: dict: Dictionary of the widgets in the frame
        self.inputs = {}
        self.buttons = {}
        self.variables = []

        # Frames for widgets
        #: tkinter.Frame: The frame that holds the position settings
        self.interop_frame = ttk.LabelFrame(self, text="Interop Frame")
        #: tkinter.Frame: holds pre- and post-analysis images
        self.image_frame = ttk.LabelFrame(self, text = "Image Frame")
        #: frame that displays extraneous information
        self.data_frame = ttk.LabelFrame(self, text = "Data Frame")
        self.canvas_frame = tk.Frame(self, height=64, width=256)
        self.DorsalImage = tk.Canvas(self.canvas_frame,
        height = 32,
        width = 256,
        bd = 10,
        highlightthickness = 10,
        relief = "ridge")
        self.DorsalImage.create_oval(-50,50,-50,50)
        self.DorsalImage.place(x = 0, y = 0)
        # self.LateralImage = tk.Canvas(self.canvas_frame,
        # height = 1100,
        # width = 2200,
        # bd = 10,
        # highlightthickness = 0,
        # relief = "ridge")
        # self.LateralImage.place(x = 0, y = 0)

        #  #: int: The width of the canvas.
        # #: int: The height of the canvas.
        # self.canvas_width, self.canvas_height = 512, 512

        # #: tk.Canvas: The canvas that will hold the camera image.
        # self.canvas = tk.Canvas(
        #     width=self.canvas_width, height=self.canvas_height
        # )
        # self.canvas.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        # #: matplotlib.figure.Figure: The figure that will hold the camera image.
        # self.matplotlib_figure = Figure(figsize=[6, 6], tight_layout=True)

        # #: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg: The canvas that will
        # # hold the camera image.
        # self.matplotlib_canvas = FigureCanvasTkAgg(self.matplotlib_figure, self.canvas)




        # Grid Each Holder Frame
        self.interop_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.image_frame.grid(row=1, column=1, sticky=tk.NSEW)
        self.data_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.canvas_frame.grid(row=1,column=0,sticky=tk.NSEW)
        
        #Image path selection
        # self.variables["storage_dir"] = ""
        self.buttons["vast_storage_dir"] = HoverButton(
            self.interop_frame, text="Select Image Save Folder "
        )
        self.buttons["vast_storage_dir"].grid(row=3, column=1, sticky="N", pady=2, padx=(6, 0))
        print("running through")
        #Button for Initialization   
        self.buttons["start_VAST"] = HoverButton(
            self.interop_frame, text="Initialize LPS+VAST"
        )
        self.buttons["start_VAST"].grid(row=4, column=1, sticky="N", pady=2, padx=(6, 0))
        
        self.VASTsavedir_label = ttk.Label(self.data_frame, text="VAST Imaging Directory")
        self.VASTsavedir_label.grid(row=0, column=0, sticky="S")
        self.inputs["VASTsavedir"] = LabelInput(
            parent=self.data_frame,
            input_class=ttk.Entry,
            input_var=tk.StringVar()
        )
        self.inputs["VASTsavedir"].grid(row=0, column=1, sticky="N", padx=6)
        self.inputs["VASTsavedir"].label.grid(sticky="N")


        self.buttons["DsplayFluorChannel"] = tk.Radiobutton(self.image_frame)

        self.CommandLabel = ttk.Label(self.interop_frame, text="Command to be sent: ")
        self.CommandLabel.grid(row=1, column=2, sticky="S")
        self.inputs["VASTCommand"] = LabelInput(
            parent=self.interop_frame,
            input_class=ttk.Entry,
            input_var=tk.StringVar()
        )
        self.inputs["VASTCommand"].grid(row=1, column=2, sticky="N", padx=6)
        self.inputs["VASTCommand"].label.grid(sticky="N")
        
        self.buttons["send_VAST_command"] = HoverButton(
            self.interop_frame, text="Select Image Save Folder "
        )
    # Getters
    def get_variables(self):
        """Returns a dictionary of the variables for the widgets in this frame.

        The key is the widget name, value is the sia associated.

        Returns
        -------
        variables : dict
            Dictionary of the variables for the widgets in this frame.
        """
        variables = {}
        for key, widget in self.inputs.items():
            variables[key] = widget.get_variable()
        return variables

    def get_widgets(self):
        """Returns a dictionary of the widgets in this frame.

        The key is the widget name, value is the LabelInput class that has all the data.

        Returns
        -------
        self.inputs : dict
            Dictionary of the widgets in this frame.
        """
        return self.inputs
