'''
The GUI for our program.  This is the main file that should be run.
'''

import PySimpleGUI as sg
from pattern import Pattern
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Skematika:
    def __init__(self) -> None:
        self.swatch_width_sts = 30
        self.swatch_height_sts = 20
        self.pattern_width_cm = 60
        self.pattern_height_cm = 80

        self.figure = None
        self.figure_canvas_agg = None
        self.pattern = Pattern(self.swatch_width_sts, self.swatch_height_sts)

        # Create the window
        self.window = self.create_GUI(page=0)

        self.canvas = self.window['pattern_canvas'].TKCanvas

        # Plot the swatch
        self.figure = self.pattern.plot_swatch(
            self.swatch_width_sts, self.swatch_height_sts)
        self.update_plot()

    def create_GUI(self, page: int = 0):
        '''
        Create the GUI

        Args:
            page: The page to display. 0 = swatch, 1 = pattern
        '''

        if page == 0:
            return self.__create_swatch_GUI()
        elif page == 1:
            return self.__create_pattern_GUI()

    def __create_swatch_GUI(self) -> sg.Window:
        '''
        Create the GUI for the swatch page

        Returns: The GUI window
        '''

        layout = [
            [
                [
                    sg.Text(
                        "1. Insert your gauge for a 10 x 10 cm swatch",
                        font=("Arial", 16),
                    )
                ],
                [sg.Canvas(size=(400, 400), key='pattern_canvas')],
                [
                    sg.Push(),
                    sg.Input(
                        key='swatch_width',
                        size=3,
                        font=("Arial", 16),
                        default_text=self.swatch_width_sts,
                    ),
                    sg.Text("x"),
                    sg.Input(
                        key='swatch_height',
                        size=3,
                        font=("Arial", 16),
                        default_text=self.swatch_height_sts,
                    ),
                    sg.Text("sts"),
                    sg.Push(),
                ],
                [
                    sg.Text(
                        "2. Insert the size of the pattern, in cm",
                        font=("Arial", 16),
                    ),
                    sg.Input(
                        key='pattern_width',
                        size=3,
                        font=("Arial", 16),
                        default_text=self.pattern_width_cm,
                    ),
                    sg.Text("x"),
                    sg.Input(
                        key='pattern_height',
                        size=3,
                        font=("Arial", 16),
                        default_text=self.pattern_height_cm,
                    ),
                ],
            ],
            [sg.Button('Continue >'), sg.Button('Exit')],
        ]

        # Create the window
        return sg.Window('Skematika', layout, finalize=True)

    def __create_pattern_GUI(self) -> sg.Window:
        # Remove everything from the window but the canvas
        for element in self.window.element_list():
            if element.Key != 'pattern_canvas':
                element.update(visible=False)

        return self.window

    def update_plot(self) -> None:
        '''
        Update the plot

        Args:
            canvas: The PySimpleGUI canvas

        Returns: None
        '''

        if self.figure_canvas_agg is not None:
            self.figure_canvas_agg.get_tk_widget().forget()

        self.figure_canvas_agg = FigureCanvasTkAgg(self.figure, self.canvas)
        self.figure_canvas_agg.draw()
        self.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    def plot_pattern(self) -> None:
        '''
        Plots the pattern            

        Returns: None
        '''
        self.figure = self.pattern.plot_pattern()
        self.update_plot()


# Create the GUI
main = Skematika()

# Display and interact with the Window using an Event Loop
while True:
    event, values = main.window.read()

    if event == 'Continue >':        
        # Create the pattern GUI
        main.window = main.create_GUI(page=1)
        # Update the pattern
        main.pattern = Pattern(round(int(values['swatch_width']) / 10 * int(values['pattern_width'])),
                               round(int(values['swatch_height']) / 10 * int(values['pattern_height'])))
        main.pattern.test_pattern()
        # Plot the pattern
        main.plot_pattern()
    # See if user wants to quit or window was closed
    if event in [sg.WIN_CLOSED, 'Exit']:
        break
