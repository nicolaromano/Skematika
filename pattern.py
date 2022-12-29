'''
pattern.py

A class to represent a knitting pattern, with methods to convert an image into a pattern
'''

import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cluster import KMeans
from skimage.transform import resize


class Pattern:
    def __init__(self, width: int, height: int, pattern_name: str = "") -> None:
        '''
        Initialize a pattern object

        Params:
        width (int)        -> the width of the pattern
        height (int)       -> the height of the pattern
        pattern_name (str) -> the name of the pattern

        Returns: None
        '''
        self.width = width
        self.height = height
        self.pattern_name = pattern_name
        self.pattern = np.zeros((height, width), dtype=np.uint8)
        # The palette is a 2D array of RGB values
        # Default palette is black (points) and white (background)
        self.palette = np.array(
            [[1.0, 1.0, 1.0], [0.0, 0.0, 0.0]], dtype=np.uint8)
        # The corresponding Matplotlib colormap
        self.cmap = ListedColormap(self.palette)

    def checkerboard(self) -> None:
        '''
        Create a checkerboard pattern

        Returns: None
        '''
        for row, col in itertools.product(range(self.height), range(self.width)):
            if (row + col) % 2 == 0:
                self.pattern[row][col] = 1

    def pattern_from_image(self, image_path: str, n_colors: int) -> None:
        '''
        Create a pattern from an image

        Params:
        image_path (str) -> the path to the image
        n_colors (int)   -> the number of colors to use

        Returns: None
        '''

        # Check that image exists
        try:
            image = plt.imread(image_path)
        except FileNotFoundError:
            print("File not found")
            return

        # Resize the image to the pattern's dimensions
        image = resize(image, (self.height, self.width), anti_aliasing=True)

        # Find the n_colors most common colors in the image using k-means clustering
        # Reshape the image to a 2D array of pixels
        image_array = image.reshape(
            (image.shape[0] * image.shape[1], image.shape[2]))
        # Use k-means clustering to find the n_colors most common colors
        kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array)
        # The palette is the n_colors most common colors
        self.palette = kmeans.cluster_centers_
        # The corresponding Matplotlib colormap
        self.cmap = ListedColormap(self.palette)

        # Create the pattern
        # For each pixel in the image, find the closest color in the palette
        for row, col in itertools.product(range(image.shape[0]), range(image.shape[1])):
            # The pixel's color
            pixel_color = image[row][col]
            # The index of the closest color in the palette
            closest_color_index = np.argmin(
                np.linalg.norm(self.palette - pixel_color, axis=1))
            # Set the pixel to the closest color
            self.pattern[row][col] = closest_color_index

    def plot_pattern(self) -> plt.Figure:
        '''
        Plot the pattern

        Returns: The matplotlib figure
        '''
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.imshow(self.pattern, cmap=self.cmap, vmin=0, vmax=1)

        return fig

    def plot_swatch(self, widht_sts: int, height_sts: int) -> plt.Figure:
        '''
        Plots a swatch

        Params:
        width_sts (int)  -> the number of stitches across the swatch
        height_sts (int) -> the number of stitches down the swatch

        Returns: the matplotlib figure
        '''

        fig, ax = plt.subplots(1, 1, figsize=(5, 5))

        # Plot a grid of white squares with black borders with a "V" written in the center
        for row, col in itertools.product(range(height_sts), range(widht_sts)):
            ax.add_patch(plt.Rectangle((col, row), 1, 1,
                         facecolor="white", edgecolor="black"))
            ax.text(col + 0.5, row + 0.5, "V", ha="center",
                    va="center", color="black")

        # Extend the limits to include the border
        ax.set_xlim(-0.2, widht_sts + 0.2)
        ax.set_ylim(-0.2, height_sts + 0.2)
        ax.set_xlabel("10 cm")
        ax.set_ylabel("10 cm")
        ax.set_xticks([])
        ax.set_yticks([])
        plt.subplots_adjust(left=0.05, bottom=0.05,
                            right=0.95, top=0.95, wspace=0, hspace=0)

        return fig

    def __str__(self):
        '''
        Print the pattern

        Returns: None
        '''

        print(self.pattern_name)
        for row in range(self.height):
            for col in range(self.width):
                if self.pattern[row][col] == 0:
                    print("o", end=" ")
                else:
                    print("x", end=" ")
            print()
