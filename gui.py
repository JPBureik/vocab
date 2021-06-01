#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 11:45:22 2020

@author: jp
"""

# Standard library imports:

import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import csv
import pandas as pd


class VocabGUI:

    def __init__(self, root):

        # Flags:

        # GUI setup:
        self.root = root
        self.root.title('Vocab Learn Program')
        self.root.wm_attributes('-fullscreen', 1)

        # Create frames:
        self.mainframe = ttk.Frame(self.root, padding=(0, 0, 12, 12))

        # Language select:

        # Create a Tkinter variable
        self.lang_sel_var = tk.StringVar(root)

        self.lang_label = ttk.Label(self.mainframe, text="Language selection").grid(row=0, column=0)

        self.sel_english = ttk.Radiobutton(self.mainframe, text='English',
                                           variable=self.lang_sel_var, value='english')
        self.sel_french = ttk.Radiobutton(self.mainframe, text='French',
                                          variable=self.lang_sel_var, value='french')

        english.grid(column=0, row=1)
        french.grid(column=0, row=2)

        # Mainframe widgets:
        # self.load_data_button = ttk.Button(
        # self.mainframe, text='Load Data', command=self.load_data_callback)
        # self.show_grouping_button = ttk.Button(
        # self.mainframe, text='Show Enzyme Grouping', command=self.show_grouping_button_callback)
        # self.plot_correlation_matrix_button = ttk.Button(
        # self.mainframe, text='Plot Correlation Matrix', command=self.plot_correlation_data_callback)
        # self.plot_histogram_button = ttk.Button(
        # self.mainframe, text='Plot Histogram', command=self.plot_histogram_button_callback)
        # self.save_fig_button = ttk.Button(
        # self.mainframe, text='Save Figure', command=self.save_fig_button_callback)
        self.quit_button = ttk.Button(self.mainframe, text='Quit',
                                      command=self.quit_button_callback)
        self.grouping_label = tk.Text(root, height=10, width=150)

        # Mainframe grid management:
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        # self.load_data_button.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.W), pady=5, padx=5)
        # self.show_grouping_button.grid(column=0, row=1, sticky=(tk.N, tk.E, tk.W), pady=5, padx=5)
        # self.plot_correlation_matrix_button.grid(
        # column=0, row=2, sticky=(tk.N, tk.E, tk.W), pady=5, padx=5)
        # self.plot_histogram_button.grid(column=0, row=3, sticky=(
        # tk.N, tk.E, tk.W), pady=(5, 0), padx=5)
        # self.save_fig_button.grid(column=0, row=4, sticky=(tk.N, tk.E, tk.W), pady=(5, 0), padx=5)
        self.quit_button.grid(column=0, row=5, sticky=(tk.N, tk.E, tk.W), pady=(5, 0), padx=5)
        self.grouping_label.grid(column=1, row=0, columnspan=5,
                                 sticky=(tk.N, tk.E, tk.W), pady=5, padx=5)

        # Disable buttons until data has been loaded:
        # self.show_grouping_button["state"] = tk.DISABLED
        # self.plot_correlation_matrix_button["state"] = tk.DISABLED
        # self.plot_histogram_button["state"] = tk.DISABLED

        # Handle window resizing:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.mainframe.columnconfigure(0, weight=3)
        self.mainframe.rowconfigure(1, weight=0)
        self.mainframe.rowconfigure(2, weight=0)
        self.mainframe.rowconfigure(3, weight=0)
        self.mainframe.rowconfigure(4, weight=0)

    """
    DATA ANALYSIS
    """

    """
    GUI CALLBACKS
    """

    def load_data_callback(self):
        self.datapath = tk.filedialog.askopenfilename()
        self.import_data()
        self.compute_correlation_matrix()
        self.compute_histogram()
        self.sort_into_groups()
        # Enable buttons:
        self.show_grouping_button["state"] = tk.NORMAL
        self.plot_correlation_matrix_button["state"] = tk.NORMAL
        self.plot_histogram_button["state"] = tk.NORMAL

    def show_grouping_button_callback(self):
        grouping_display = ''
        grouping_display += "{:<8} {:<15}".format('Group', 'Enzymes')
        for k, v in self.grouping.items():
            a = str(v)
            b = a[1:-1].replace("'", '')
            grouping_display += '\n' + "{:<8} {:<15}".format(k, b)
        # Clear before inserting new text to avoid overflow:
        self.grouping_label.delete('1.0', tk.END)
        self.grouping_label.insert(tk.END, grouping_display)

    def plot_correlation_data_callback(self):

        fig = Figure(figsize=(19, 9))
        ax = fig.add_subplot(111)
        im = ax.imshow(self.enzyme_correlation_matrix, aspect='auto', cmap='bwr')
        im.set_clim(-1, 1)
        ax.grid(False)
        if self.plot_only_lt is True:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        ax.xaxis.set(ticks=tuple(np.arange(0, len(self.enzyme_list), 1)),
                     ticklabels=self.enzyme_matrix_columns)
        ax.tick_params(axis="x", rotation=45, labelsize=9)
        ax.yaxis.set(ticks=tuple(np.arange(0, len(self.enzyme_list), 1)),
                     ticklabels=self.enzyme_matrix_columns)
        ax.set_ylim(len(self.enzyme_list)-0.5, -0.5)
        for i in range(len(self.enzyme_list)):
            for j in range(len(self.enzyme_list)):
                if i < j:
                    if self.plot_only_lt is True:
                        color = 'white'
                    else:
                        color = 'black'
                else:
                    color = 'black'
                ax.text(j, i, self.enzyme_correlation_matrix[i][j], ha='center',
                        va='center', color=color, size=9)
        ax.figure.colorbar(im, ax=ax, format='% .2f')

        try:
            self.canvas.get_tk_widget().grid_forget()
        except AttributeError:
            pass
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().grid(columnspan=2, sticky=(tk.N, tk.E, tk.W), pady=5, padx=5)
        self.canvas.draw()

    def plot_histogram_button_callback(self):

        fig = Figure(figsize=(20, 5))
        ax = fig.add_subplot(111)

        N, bins, patches = ax.hist(self.hist_list, bins=self.hist_axis, color='steelblue', ec='k')
        for i in range(len(patches)-3, len(patches)):
            patches[i].set_facecolor('indianred')
        ax.set_xticks(self.hist_axis[::2])
        # plt.yticks(np.arange(0, 25, 2))
        ax.grid(True)
        ax.set_xlim([-1, 1])
        ax.grid(color='black', linestyle=':', linewidth=0.25)
        ax.set_xlabel('Correlation of activity between enzyme pairs')
        ax.set_ylabel('Occurrence')

        try:
            self.canvas.get_tk_widget().grid_forget()
        except AttributeError:
            pass
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().grid(columnspan=2, sticky=(tk.N, tk.E, tk.W), pady=5, padx=5)
        self.canvas.draw()

    def save_fig_button_callback(self):
        pass

    def quit_button_callback(self):
        self.root.destroy()


"""
PUBLIC METHODS
"""

"""
EXECUTION
"""

if __name__ == '__main__':

    root = tk.Tk()
    start = VocabGUI(root)
    root.mainloop()
