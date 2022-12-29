'''
The GUI for our program.  This is the main file that should be run.
'''

import PySimpleGUI as sg
from pattern import Pattern
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update_plot(fig, canvas):
    '''
    Update the plot

    Args:
        fig: The matplotlib figure
        canvas: The canvas the figure is drawn on

    Returns: None
    '''

    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

default_swatch_width_sts = 30
default_swatch_height_sts = 20

# Define the window's contents
layout = [
    [
         [sg.Text("1. Insert your gauge for a 10 x 10 cm swatch",
                  font=("Arial", 16))],
        [sg.Canvas(size=(400, 400), key='pattern_canvas')],
        [sg.Push(),
             sg.Input(key='swatch_width', size=3, font=(
                 "Arial", 16), default_text=default_swatch_width_sts),
             sg.Text("x"),
             sg.Input(key='swatch_height', size=3, font=(
                 "Arial", 16), default_text=default_swatch_height_sts), sg.Text("sts"), sg.Push()],
        [sg.Text("2. Insert the size of the pattern, in cm",
                 font=("Arial", 16)),
             sg.Input(key='pattern_width', size=3, font=(
                 "Arial", 16), default_text=80),
             sg.Text("x"),
             sg.Input(key='pattern_height', size=3, font=(
                 "Arial", 16), default_text=60)]
    ],
    [sg.Button('Continue >'),
     sg.Button('Exit')]
]

# Create the window
window = sg.Window('Skematika', layout, finalize=True)

# Create the Pattern object
pattern = Pattern(100, 100)

# Plot the swatch
fig = pattern.plot_swatch(default_swatch_width_sts, default_swatch_height_sts)
canvas = FigureCanvasTkAgg(fig, window['pattern_canvas'].TKCanvas)
update_plot(fig, canvas)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event in [sg.WIN_CLOSED, 'Exit']:
        break
