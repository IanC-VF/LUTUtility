import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import matplotlib
from matplotlib import cm

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import numpy as np

import xlrd
from mpl_toolkits.mplot3d import Axes3D

import csv
#from scipy.optimize import curve_fit
#from sklearn.linear_model import LinearRegression

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Beta Laser Power Calibration App")
        tk.Button(self, text='Open File', command=self.open_files,
                  anchor="w").grid(row=0, column=0, sticky="W")
        tk.Label(self, text='File Path', font=('bold', 9), anchor='w').grid(
                row=0, column=2, sticky='E')

        self.option = tk.IntVar()
        self.optionList = ["Calculate ...", "Review ...", "Laser Records ...", "Deviation ..."]
        n = len(self.optionList)
        for i in range(n):
            tk.Radiobutton(self, text=self.optionList[i], variable=self.option,
                value=i).grid(row=1, column=i, sticky="W")

        self.para_Panel()

        cm_subsection = np.linspace(0, 1, self.laser_num)
        self.pltColorList = [cm.rainbow(x) for x in cm_subsection]

        self.initiateCanvas()
        #self.cmaps = ['hot', 'plasma', 'jet', 'rainbow', 'hsv']
        self.norm = matplotlib.colors.Normalize(vmin=0, vmax=4)
        self.cmap = plt.cm.coolwarm

        self.mainloop()

    def para_Panel(self):
        self.powerMax_Setup(3, 0)
        self.laser_Setup(4, 0)
        self.pulseDur_Setup(5, 0)
        self.nominalPower_Setup(6, 0)
        self.update_Setup(7, 1)

    def powerMax_Setup(self, row_pos, col_pos):
        tk.Label(self, text='Power Max', font=('bold', 10), anchor='w').grid(
                row=row_pos, column=col_pos, sticky='W')
        self.powerMaxString = tk.StringVar()
        self.entryPowerMax = tk.Entry(self, textvariable=self.powerMaxString, width=5)
        self.entryPowerMax.grid(row=row_pos, column=col_pos+1, pady=5, sticky="E")
        self.powerMaxString.set("300")
        tk.Label(self, text='W', anchor='w').grid(
                row=row_pos, column=col_pos+2, sticky='W')
        self.powerMaxUpdate()

    def laser_Setup(self, row_pos, col_pos):
        tk.Label(self, text='Number of Lasers', font=('bold', 10), anchor='w').grid(
                row=row_pos, column=col_pos, sticky='W')
        self.laserNumString = tk.StringVar()
        self.entryLaserNum = tk.Entry(self, textvariable=self.laserNumString, width=4)
        self.entryLaserNum.grid(row=row_pos, column=col_pos+1, pady=5, sticky="E")
        self.laserNumString.set("60")
        self.laserNumUpdate()

    def pulseDur_Setup(self, row_pos, col_pos):
        tk.Label(self, text='Pulse Duration', font=('bold', 10), anchor='w').grid(
                row=row_pos, column=col_pos, sticky='W')
        self.pulseDurString = tk.StringVar()
        self.entryPulseDur = tk.Entry(self, textvariable=self.pulseDurString, width=8)
        self.entryPulseDur.grid(row=row_pos, column=col_pos+1, pady=5, sticky="E")
        self.pulseDurString.set("0.004")
        self.pulseDuration = float(self.entryPulseDur.get())
        tk.Label(self, text='sec', anchor='w').grid(
                row=row_pos, column=col_pos+2, sticky='W')

    def nominalPower_Setup(self, row_pos, col_pos):
        tk.Label(self, text='Nominal Power', font=('bold', 10), anchor='w').grid(
                row=row_pos, column=col_pos, sticky='W')
        self.nomiPowerString = tk.StringVar()
        self.entrynomiPower = tk.Entry(self, textvariable=self.nomiPowerString, width=32)
        self.entrynomiPower.grid(row=row_pos, column=col_pos+1, pady=5, sticky="E")
        self.nomiPowerString.set("0.2, 0.3, 0.4, 0.5, 0.6, 0.7")
        self.nomiPowerUpdate()

    def update_Setup(self, row_pos, col_pos):
        self.updateButton = tk.Button(self, text = 'Update', command=self.update_click)
        self.updateButton.grid(row=row_pos, column=col_pos, pady=5, sticky='W')

    def update_click(self):
        self.powerMaxUpdate()
        self.laserNumUpdate()
        self.pulseDurUpdate()
        print(self.pulseDuration)
        self.nomiPowerUpdate()

    def powerMaxUpdate(self):
        self.power_max = float(self.entryPowerMax.get())

    def laserNumUpdate(self):
        self.laser_num = int(self.entryLaserNum.get())
        self.laser_id_list = ['Laser'+str(i+1) for i in range(self.laser_num)]
        self.caliMatrix = np.zeros((self.laser_num, 3))
        cm_subsection = np.linspace(0, 1, self.laser_num)
        self.pltColorList = [cm.rainbow(x) for x in cm_subsection]

    def pulseDurUpdate(self):
        self.pulseDuration = float(self.entryPulseDur.get())

    def nomiPowerUpdate(self):
        power_capture_string = self.entrynomiPower.get()
        power_capture = power_capture_string.split(',')
        self.power_perc = np.zeros(len(power_capture))
        for i in range(len(power_capture)):
            self.power_perc[i] = float(power_capture[i])

    def readCSV(self, filePath):
        with open (filePath) as csvFile:
            readCSV = csv.reader(csvFile, delimiter = ',')
            measure_id, measure_power, measure_std = [], [], []
            for row in readCSV:
                id = row[0]
                power = float(row[1])/self.pulseDuration
                measure_id.append(id)
                measure_power.append(power)
        return (measure_id, measure_power)

    def open_files(self):
        getCWD = os.getcwd()
        self.fileName = filedialog.askopenfilename(initialdir = getCWD,
                        filetypes = [('CSV', '.csv'), ('Excel', '.xlsx')])
        tk.Label(self, text = self.fileName, font=("bold", 10), foreground='blue',
                anchor='w', width=80, height=1, bg ='white').grid(row=0, column=1, columnspan=5)
        fileID = self.fileName.split('/')[-1]
        self.fileID = fileID.split('.')[0]

        csv_data = self.readCSV(self.fileName)
        self.measureID = csv_data[0]
        self.measurePower = csv_data[1]
        self.caliCSV()

        self.var = [tk.IntVar() for i in range(self.laser_num)]

        self.var_get = [0]*self.laser_num
        self.var_Dict = dict(zip(self.laser_id_list, self.var_get))

        self.initiatePlot()
        self.plotOption()

        self.subwindow = tk.Toplevel(self)
        self.newWindow(self.subwindow)

    def initiatePlot(self):
        self.ax1 = self.fig1.add_subplot(1, 2, 1)
        self.ax2 = self.fig1.add_subplot(1, 2, 2)
        #self.ax1.set_aspect("equal", 'box')
        self.fig1.subplots_adjust(right=0.88)
        self.cax = self.fig1.add_axes([0.92, 0.1, 0.03, 0.8])

    def plotOption(self):
        self.optionFrame = tk.Frame(self).grid(row=3, column=0)
        self.plot_Options = ['Selected Lasers (in app)', 'ALL Lasers (in app)', 'Each Laser (pop-out window)']
        tk.Label(self.optionFrame, text = 'Select Plot Options', font=("bold", 10),
                    relief="groove", anchor='w').grid(row=2, column=0, sticky='W')

        self.cbox = ttk.Combobox(self.optionFrame, values = self.plot_Options)
        self.cbox.grid(row=2, column=1, sticky='W')
        self.cbox.bind("<<ComboboxSelected>>", self.plotLasers)

    def plotLasers(self, event):
        #self.plot_option_selected = self.cbox.get()
        self.plot_ID = self.cbox.current()

        if self.plot_ID == 0:
            self.plotPower(self.laser_selected)

        if self.plot_ID == 1:
            self.plotPower(self.laser_id_list)

        if self.plot_ID == 2:
            self.plotOutApp()

    def newWindow(self, master):
        frame = tk.Frame(master)
        master.title('Select Laser ID')

        tk.Label(master, text = 'Select Laser ID', font=("bold", 10),
                    relief="groove", anchor='w').grid()

        for key in self.var_Dict:
            self.var_Dict[key] = tk.IntVar()
            tk.Checkbutton(master, text=key, variable=self.var_Dict[key],
                    onvalue=1, offvalue=0).grid()
        tk.Button(master, text = 'Apply', command = self.query_SheetSelection).grid()

    def query_SheetSelection(self):
        self.laser_selected = []
        for key, value in self.var_Dict.items():
            state = value.get()
            if state == 0:
                print (key, "Unselected")
            else:
                print (key, "Selected")
                self.laser_selected.append(key)

        if self.laser_num*len(self.power_perc) != len(self.measureID):
            print ('ERROR | Number of Tested Lasers is Incorrect')
        else:
            print ("***")
            print (self.laser_selected)
        #self.master.destroy()

    def plotPower(self, laser_list):
        self.ax1.cla()
        self.cax.cla()

        power_nominal = self.power_perc
        self.ax1.plot(power_nominal, power_nominal, linestyle='--', c='g', label='Nominal')
        self.ax2.plot(power_nominal, power_nominal, linestyle='--', c='g', label='Nominal')
        for i, element in enumerate(laser_list):
            id_power = np.zeros(len(self.power_perc))
            power_input_corr = np.zeros(len(self.power_perc))
            id = int(element.split('Laser')[1])-1
            for j in range(len(self.power_perc)):
                id_power[j] = self.measurePower[id*len(self.power_perc)+j]/self.power_max
                power_input_corr[j] = self.caliMatrix[id][0]*self.power_perc[j]**2+self.caliMatrix[id][1]*self.power_perc[j]+self.caliMatrix[id][2]

            power_fit_output = np.linspace(0.19, 0.71, 50)
            power_fit_input = self.caliMatrix[id][0]*power_fit_output**2+self.caliMatrix[id][1]*power_fit_output+self.caliMatrix[id][2]

            self.ax1.plot(power_nominal, id_power, '--o', markersize=7,
                        markerfacecolor=self.pltColorList[id],
                        c=self.pltColorList[id], markeredgecolor='gray',
                        markeredgewidth=1, label=element)

            self.ax2.plot(power_fit_input, power_fit_output, linestyle='--',
                        c=self.pltColorList[id], label='Fitted Curve')
            self.ax2.plot(power_nominal, id_power, 'o', markersize=7,
                        markerfacecolor=self.pltColorList[id],
                        c=self.pltColorList[id], markeredgecolor='gray',
                        markeredgewidth=1)
            self.ax2.plot(power_input_corr, self.power_perc, '*', markersize=12,
                        markerfacecolor='w',
                        c=self.pltColorList[id], markeredgecolor='gray',
                        markeredgewidth=1)

        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax1.set(xlabel='Control Power Setup (%)', ylabel='Measured Outcome (%)')
        self.ax2.set(xlabel='Control Power Setup (%)', ylabel='Measured Outcome (%)')
        self.ax1.legend(loc=4, frameon=True, fancybox=True, shadow=True)

        self.canvas.draw()

    def plotOutApp(self):
        power_fit_output = np.linspace(0.19, 0.71, 50)
        style = dict(size=10, color='black')
        for i in range(self.laser_num):
            fig, ax = plt.subplots(1, 2, figsize=(12, 6))
            power_nominal = self.power_perc
            id_power = np.zeros(len(self.power_perc))
            power_input_corr = np.zeros(len(self.power_perc))
            coeff = self.caliMatrix[i]
            for j in range(len(self.power_perc)):
                id_power[j] = self.measurePower[i*len(self.power_perc)+j]/self.power_max
                power_input_corr[j] = coeff[0]*self.power_perc[j]**2+coeff[1]*self.power_perc[j]+coeff[2]

            power_fit_input = coeff[0]*power_fit_output**2+coeff[1]*power_fit_output+coeff[2]

            ax[0].plot(power_nominal, power_nominal, linestyle='--', c='g', label='Nominal')
            ax[1].plot(power_nominal, power_nominal, linestyle='--', c='g', label='Nominal')

            ax[0].plot(power_nominal, id_power, '--o', markersize=7,
                        markerfacecolor=self.pltColorList[i],
                        c=self.pltColorList[i], markeredgecolor='gray',
                        markeredgewidth=1, label=self.laser_id_list[i]+' Raw')

            ax[1].plot(power_fit_input, power_fit_output, linestyle='--',
                        c=self.pltColorList[i], label='Fitted Curve')
            ax[1].plot(power_nominal, id_power, 'o', markersize=7,
                        markerfacecolor=self.pltColorList[i],
                        c=self.pltColorList[i], markeredgecolor='gray',
                        markeredgewidth=1, label=self.laser_id_list[i]+' Raw')
            ax[1].plot(power_input_corr, self.power_perc, '*', markersize=12,
                        markerfacecolor='w',
                        c=self.pltColorList[i], markeredgecolor='gray',
                        markeredgewidth=1, label=self.laser_id_list[i]+' Corrected')

            ax[0].text(0.2, 0.65, self.laser_id_list[i] + " Raw Measurements")
            txtstr = str('{:3.3f}'.format(coeff[0]))+'*x^2 + '+str('{:3.3f}'.format(coeff[1]))+'*x + '+str('{:3.3f}'.format(coeff[2]))
            ax[1].text(0.2, 0.65, txtstr, ha='left', **style)
            ax[0].set(xlabel='Control Power Setup (%)', ylabel='Measured Outcome (%)')
            ax[1].set(xlabel='Control Power Setup (%)', ylabel='Measured Outcome (%)')
            ax[0].grid(True)
            ax[1].grid(True)
            ax[0].legend(loc=4, frameon=True, fancybox=True, shadow=True)
            ax[1].legend(loc=4, frameon=True, fancybox=True, shadow=True)
            plt.show()

    def caliCSV(self):
        nominal_power = self.power_perc
        for i in range(self.laser_num):
            id_power = np.zeros(len(self.power_perc))
            for j in range(len(self.power_perc)):
                id_power[j] = self.measurePower[i*len(self.power_perc)+j]/self.power_max

            coeff, yvals = self.curvefit_1(id_power, nominal_power)
            for k in range(3):
                self.caliMatrix[i][k] = coeff[k]
        print (self.caliMatrix)
        csvName = self.fileID + '_calibration.csv'
        np.savetxt(csvName, self.caliMatrix, delimiter = ',', fmt = '%f')

    def initiateCanvas(self):
        self.fig1 = Figure(figsize = (13, 6), dpi = 100)
        self.canvas = FigureCanvasTkAgg(self.fig1, master = self)
        self.canvas.get_tk_widget().grid(row=3, column=3, rowspan=10, columnspan=10)

        self.toolbarFrame = tk.Frame(master = self)
        self.toolbarFrame.grid(row=13, column=0, rowspan=1, columnspan=10, sticky='ew')
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

    def curvefit_1(self, x, y):
        f1 = np.polyfit(x, y, 2)
        p1 = np.poly1d(f1)
        #yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
        yvals = np.polyval(f1, x)
        return (f1, yvals)

##########################################

    def loadNewCSV(self):
        getCWD = os.getcwd()
        csvNewName = filedialog.askopenfilename(initialdir = getCWD,
                        filetypes = [('CSV', '.csv')])
        self.caliNewFileName = os.path.splitext(os.path.basename(csvNewName))[0]
        self.loadNewMatrix = np.loadtxt(csvNewName, delimiter=',')

    def func(self, x, a, b, c):
        return (a*x*x + b*x + c)

    def curvefit_2(self, x, y):
        #popt, pcov = curve_fit(self.func, x, y)
        #yvals = self.func(x, popt[0], popt[1], popt[2])
        #return (popt, yvals)
        pass

if __name__ == "__main__":
    App()
