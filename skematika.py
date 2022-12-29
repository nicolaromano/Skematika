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


# Define the window's contents
layout = [
    [
         [sg.Push(), sg.Text("Insert your gauge for a 10 x 10 cm swatch",
                             font=("Arial", 16)), sg.Push()],
        [sg.Canvas(size=(500, 500), key='pattern_canvas')],
        [sg.Push(),
             sg.Input(key='swatch_width', size=3, font=(
                 "Arial", 16), default_text=30),
             sg.Text("x"),
             sg.Input(key='swatch_height', size=3, font=(
                 "Arial", 16), default_text=20), sg.Text("sts"), sg.Push()],
         [sg.Push(), sg.Text("Insert the size of the pattern, in cm",
                             font=("Arial", 16)), sg.Push()]
    ],
    [sg.Button('Continue >'),
     sg.Button('Exit')]
]

# Create the window
window = sg.Window('Skematika', layout, finalize=True)

# Create the Pattern object
pattern = Pattern(100, 100)

# Plot the swatch
fig = pattern.plot_swatch()
canvas = FigureCanvasTkAgg(fig, window['pattern_canvas'].TKCanvas)
update_plot(fig, canvas)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event in [sg.WIN_CLOSED, 'Exit']:
        break
