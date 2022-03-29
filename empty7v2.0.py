####################################################################################
# Version: January 2022
#
# Purpose: 
# This is a note-taking app, useful for people working on several projects at 
# the same time and who want to be able to update multiple documents at the same 
# time and from the same window. 
#
# Structure: 
# There are six text widgets in total: 5 corresponding to 5 different projects, 1
# ("Misc", from "Miscellaneous"for taking impromptu notes on anything else that is 
# not related to those 5 projects. 
# You write your notes on the desired text widget. Once you're done, you click on 
# the green tick button, which saves what you've written in a corresponding .txt 
# file, and automatically clears the text widget for you. On the txt file, entries 
# appear together with the date and time of writing, unless there is already an entry
# on that txt file with the same data, in which case only the time of writing is 
# indicated. Above every widget there's a button with the name of the corresponding
# project. If clicked, that button opens the .txt document associated with that
# widget. 
# The red cross button clears the text widget (note: I had that link to a function in 
# a previous version of this code, then I removed the function but left the button, 
# and I still haven't gotten around to linking it again)
#  
####################################################################################

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import ctypes
import functions
from functools import partial
import pdb; #pdb.set_trace()

ctypes.windll.shcore.SetProcessDpiAwareness(1) # this improves resolution of GUI 

root = tk.Tk()
root.title("Elena's Notes") 
#root.geometry('200x150') # this adjusts the size of the GUI to 200X150

# I want the border of the text widgets to change color if the cursor is over those widgets, 
# so I am using two base64-encoded gifs of a rounded-corner square, one is green (accent color), 
# the other one is black (no-selection color). 

# CALLING A FUNCTION TO USE A BASE64-ENCODED GIF OF A ROUNDED-CORNER SQUARE WITH A GREEN BORDER
focusBorderImageData = functions.focusborder_string()

# CALLING A FUNCTION TO USE A BASE64-ENCODED GIF OF A ROUNDED-CORNER SQUARE WITH A BLACK BORDER
borderImageData = functions.border_string()

style = ttk.Style()
borderImage = tk.PhotoImage("borderImage", data=borderImageData)
focusBorderImage = tk.PhotoImage("focusBorderImage", data=focusBorderImageData)

style.element_create("RoundedFrame", 
                    "image", borderImage, 
                    ("focus", focusBorderImage), 
                    border=20, sticky="nsew")

style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])

style.configure('TFrame', background= 'black') 

# CREATING 2 FRAMES, A LEFT AND A RIGHT FRAME, WHERE TO HOST 3 TEXT WIDGETS EACH
frameL = tk.Frame(root, bg="#BAD9D0")  # cD4F1B2 is a light green color
frameR = tk.Frame(root, bg="#BAD9D0")

# DECLARING LISTS TO POPULATE WITH OBJECTS THAT WILL BE ACCESSED LATER USING THE INDEX ("i")
frames = []
texts = []

# SETTING BUTTON IMAGES: MAIN BUTTON
img = functions.image(3)

# SETTING BUTTON IMAGES: SECONDARY BUTTONS
img_cross = Image.open('cross1.png') 
img_cross = img_cross.resize((30,30), Image.ANTIALIAS)
img_photo_crs = ImageTk.PhotoImage(img_cross)
img_check = Image.open('check1.png')
img_check = img_check.resize((30,30), Image.ANTIALIAS)
img_photo_chk = ImageTk.PhotoImage(img_check)

for i in range(6):
    # THE FIRST 3 SUBFRAMES GO TO THE LEFT
    if i <= 2:
        frame = ttk.Frame(frameL, style="RoundedFrame", padding=10)
    # THE LAST 3 SUBFRAMES GO TO THE RIGHT
    else:
        frame = ttk.Frame(frameR, style="RoundedFrame", padding=10)

    # APPEND EVERY SINGLE FRAME TO THE LIST TO ACCESS THEM LATER
    frames.append(frame)

    # CREATING THE TEXT WIDGETS (I.E. THE INPUT FIELDS)
    text = tk.Text(frames[i], borderwidth = 0, highlightthickness = 0, wrap = "word", width = 10, height = 5)
    text.pack(fill = "both", expand = True)
    text.bind("<FocusIn>", lambda event: frames[i].state(["focus"]))
    text.bind("<FocusOut>", lambda event: frames[i].state(["!focus"]))
    text.insert("end", "")
    texts.append(text)

    # CREATING THE BUTTONS FOLLOWING THE GIVEN ORDER CHECKING THE LOOP INDEX
    if i == 0:
        main_button = functions.create_buttons(frameL, functions.openprobus, "Probus", i)
    elif i == 1:
        main_button = functions.create_buttons(frameL, functions.opensage, "Sage", i)
    elif i == 2: 
        main_button = functions.create_buttons(frameL, functions.openJALL, "JALL", i)       #Journal African Languages & Linguistics
    elif i == 3:
        main_button = functions.create_buttons(frameR, functions.openheaviness, "Heavi", i) # Topicalization Study
    elif i == 4: 
        main_button = functions.create_buttons(frameR, functions.openacode, "ACoDe", i)
    elif i == 5: 
        main_button = functions.create_buttons(frameR, functions.openmisc, "MISC", i)

    main_button.config(image = img)
    main_button.pack(pady = 5)

    # SHOWING THE FRAMES (MOVE TO BOTTOM?)
    frames[i].pack(side = tk.TOP, fill = "both", expand = True, padx = 30)

    # ADDING THE BUTTONS INSIDE THE INPUT FIELDS
    # PARTIAL (IN "command") ALLOW US TO SET A COMMAND FOR THE BUTTON USING THE INDEX ("i") AS ARGUMENT
    button_check = tk.Button(frames[i], image = img_photo_chk, command = partial(functions.compile, texts , i), background = "white", borderwidth = 0, height = 30, width = 30)
    button_check.image = img_photo_chk
    button_check.pack(side = tk.LEFT)

    button_cross = tk.Button(frames[i], image = img_photo_crs, background = "white", borderwidth = 0, height = 30, width = 30)
    button_cross.image = img_photo_crs
    button_cross.pack(side = tk.RIGHT)

root.configure(background="#BAD9D0") #BAD9D0 #cfffff #D4F1B2
frameL.pack(side=tk.LEFT, fill="both", expand=True) # side=tk.LEFT places frames side by side
frameR.pack(side=tk.LEFT, fill="both", expand=True) # side=tk.LEFT places frames side by side

# SET FOCUS TO THE FIRST FRAME
frames[0].focus_set()

font_tuple = ("Garamond", 14)

root.mainloop()