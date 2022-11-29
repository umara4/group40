import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3
import decimal
import math
import serial
import serial.tools.list_ports
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#two variables that are subject to change based on the pacemaker.
#warning is a boolean to show that there is another pacemaker nearby
warning = True
#connection is a boolean to show that the connection with the pacemaker
connection = True

# class pacemakerSerial:
#
#     def __init__(self, UserID):
#         # Mac port, for windows you have to find the ports yourself lmao
#         self.frdm_port = "/dev/cu.usbmodem0000001234561"
#
#         # Windows port, check COM port in device manager
#         # win_port = "COM4"
#         #self.login = LoginDatabase()
#         self.AOO = AOOParameterDatabase()
#         self.VOO = VOOParameterDatabase()
#         self.AAI = AAIParameterDatabase()
#         self.VVI = VVIParameterDatabase()
#         self.AOOR = AOORParameterDatabase()
#         self.VOOR = VOORParameterDatabase()
#         self.AAIR = AAIRParameterDatabase()
#         self.VVIR = VVIRParameterDatabase()
#         self.userID = UserID
#         #self.cmode = self.login.ReturnMode(self.userID)[0][4]
#         self.modeDict = {
#             'AOO': 1,
#             'AOOR': 2,
#             'VOO': 3,
#             'VOOR': 4,
#             'AAI': 5,
#             'AAIR': 6,
#             'VVI': 7,
#             'VVIR': 8
#         }
#         self.ActivityThresholdDict = {
#             "V-Low": 1,
#             'Low': 2,
#             'Med-Low': 3,
#             'Med': 4,
#             'Med-High': 5,
#             'High': 6,
#             'V-High': 7
#         }
#
#         # B = uint8
#         # f = single
#         # H = uint16
#         # d = double ( 8 bytes)
#
#         # parameter values to send to pacemaker
#         self.Start = b'\x16'
#         self.SYNC = b'\x22'
#         self.Fn_set = b'\x55'
#         self.Pacing_mode = struct.pack("B", 1)
#         self.Pacing_mode = struct.pack("B", 1)
#         self.LRL = struct.pack("B", 1) #LRL
#         self.URL = struct.pack("B", 1) #URL
#         self.MSR = struct.pack("B", 1) #max sensor rate
#         self.A_PA = struct.pack("f", 1.0) #pulse amplitude
#         self.V_PA = struct.pack("f", 1.0) #pulse amplitude
#         self.A_PW = struct.pack("B", 1) #pulse width
#         self.V_PW = struct.pack("B", 1) #pulse width
#         self.A_Sense = struct.pack("f", 1) #sensitivity
#         self.V_Sense = struct.pack("f", 1) #sensitivity
#         self.A_R = struct.pack("H", 1) #ARP
#         self.V_R = struct.pack("H", 1) #VRP
#         self.PVARP = struct.pack("H", 1) #PVARP
#         self.Act_thres = struct.pack("B", 1) #activity threshold
#         self.React_time = struct.pack("B", 1) #reaction time
#         self.Response_factor = struct.pack("B", 1) #response factor
#         self.Recovery_time = struct.pack("H", 1) #recovery time
#
#         # values to read for ECG
#         self.Atr = 0.0
#         self.Vnt = 0.0
#
#     # send current parameter values to pacemaker
#     def send_param(self):
#         # create signal to send
#         Signal_set = self.Start + self.Fn_set + self.Pacing_mode + self.LRL + self.URL + self.MSR + self.A_PA + self.V_PA + self.A_PW + self.V_PW + self.A_Sense + self.V_Sense + self.A_R + self.V_R + self.PVARP + self.Act_thres + self.React_time + self.Response_factor + self.Recovery_time
#
#         with serial.Serial(self.frdm_port, 115200) as pacemaker:
#             pacemaker.write(Signal_set)
#
#     # recieve Atr and Vnt values from pacemaker for ECG
#     def get_echo(self):
#         # create signal to send
#         Signal_echo = self.Start + self.SYNC + self.Pacing_mode + self.LRL + self.URL + self.MSR + self.A_PA + self.V_PA + self.A_PW + self.V_PW + self.A_Sense + self.V_Sense + self.A_R + self.V_R + self.PVARP + self.Act_thres + self.React_time + self.Response_factor + self.Recovery_time
#
#         with serial.Serial(self.frdm_port, 115200) as pacemaker:
#             pacemaker.write(Signal_echo)
#             data = pacemaker.read(49)
#             self.Atr = struct.unpack("d", data[33:41])[0]
#             self.Vnt = struct.unpack("d", data[41:49])[0]
#
#             print(self.Atr)
#             print(self.Vnt)
#
#     def update(self):
#         self.login = LoginDatabase()
#         self.currentmode = self.login.ReturnMode(self.userID)[0][4]
#         if self.currentmode == "AOO":
#             self.AOO_receive = self.AOO.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.AOO_receive[0][1]))
#             self.URL = struct.pack("B", int(self.AOO_receive[0][2]))
#             self.MSR = struct.pack("B", 1) #max sensor rate
#             if self.AOO_receive[0][3] != 'Off':
#                 self.A_PA = struct.pack("f", float(self.AOO_receive[0][3]))  # pulse amplitude
#             else:
#                 self.A_PA = struct.pack("f", 0)
#             self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
#             self.A_PW = struct.pack("B", int(self.AOO_receive[0][4]))  # pulse width
#             self.V_PW = struct.pack("B", 1)  # pulse width
#             self.A_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.V_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.A_R = struct.pack("H", 1)  # ARP
#             self.V_R = struct.pack("H", 1)  # VRP
#             self.PVARP = struct.pack("H", 1)  # PVARP
#             self.Act_thres = struct.pack("B", 1)  # activity threshold
#             self.React_time = struct.pack("B", 1)  # reaction time
#             self.Response_factor = struct.pack("B", 1)  # response factor
#             self.Recovery_time = struct.pack("B", 1)  # recovery time
#         elif self.currentmode == "VOO":
#             self.VOO_receive = self.VOO.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.VOO_receive[0][1]))
#             self.URL = struct.pack("B", int(self.VOO_receive[0][2]))
#             self.MSR = struct.pack("B", 1) #max sensor rate
#             self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
#             if self.VOO_receive[0][3] != 'Off':
#                 self.V_PA = struct.pack("f", float(self.VOO_receive[0][3]))  # pulse amplitude
#             else:
#                 self.V_PA = struct.pack("f", 0)
#             self.A_PW = struct.pack("B", 1)  # pulse width
#             self.V_PW = struct.pack("B", int(self.VOO_receive[0][4]))  # pulse width
#             self.A_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.V_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.A_R = struct.pack("H", 1)  # ARP
#             self.V_R = struct.pack("H", 1)  # VRP
#             self.PVARP = struct.pack("H", 1)  # PVARP
#             self.Act_thres = struct.pack("B", 1)  # activity threshold
#             self.React_time = struct.pack("B", 1)  # reaction time
#             self.Response_factor = struct.pack("B", 1)  # response factor
#             self.Recovery_time = struct.pack("B", 1)  # recovery time
#         elif self.currentmode == "AAI":
#             self.AAI_receive = self.AAI.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.AAI_receive[0][1]))
#             self.URL = struct.pack("B", int(self.AAI_receive[0][2]))
#             self.MSR = struct.pack("B", 1) #max sensor rate
#             if self.AAI_receive[0][3] != 'Off':
#                 self.A_PA = struct.pack("f", float(self.AAI_receive[0][3]))  # pulse amplitude
#             else:
#                 self.A_PA = struct.pack("f", 0)  # pulse amplitude
#             self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
#             self.A_PW = struct.pack("B", int(self.AAI_receive[0][4]))  # pulse width
#             self.V_PW = struct.pack("B", 1)  # pulse width
#             self.A_Sense = struct.pack("f", float(self.AAI_receive[0][5]))  # sensitivity
#             self.V_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.A_R = struct.pack("H", int(self.AAI_receive[0][6]))  # ARP
#             self.V_R = struct.pack("H", 1)  # VRP
#             self.PVARP = struct.pack("H", int(self.AAI_receive[0][7]))  # PVARP
#             self.Act_thres = struct.pack("B", 1)  # activity threshold
#             self.React_time = struct.pack("B", 1)  # reaction time
#             self.Response_factor = struct.pack("B", 1)  # response factor
#             self.Recovery_time = struct.pack("B", 1)  # recovery time
#         elif self.currentmode == "VVI":
#             self.VVI_receive = self.VVI.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.VVI_receive[0][1]))
#             self.URL = struct.pack("B", int(self.VVI_receive[0][2]))
#             self.MSR = struct.pack("B", 1) #max sensor rate
#             self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
#             if self.VVI_receive[0][2] != 'Off':
#                 self.V_PA = struct.pack("f", float(self.VVI_receive[0][3]))  # pulse amplitude
#             else:
#                 self.V_PA = struct.pack("f", 0)
#             self.A_PW = struct.pack("B", 1)  # pulse width
#             self.V_PW = struct.pack("B", int(self.VVI_receive[0][4]))  # pulse width
#             self.A_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.V_Sense = struct.pack("f", float(self.VVI_receive[0][5]))  # sensitivity
#             self.A_R = struct.pack("H", 1)  # ARP
#             self.V_R = struct.pack("H", int(self.VVI_receive[0][6]))  # VRP
#             self.PVARP = struct.pack("H", 1)  # PVARP
#             self.Act_thres = struct.pack("B", 1)  # activity threshold
#             self.React_time = struct.pack("B", 1)  # reaction time
#             self.Response_factor = struct.pack("B", 1)  # response factor
#             self.Recovery_time = struct.pack("B", 1)  # recovery time
#         elif self.currentmode == "AOOR":
#             self.AOOR_receive = self.AOOR.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.AOOR_receive[0][1]))
#             self.URL = struct.pack("B", int(self.AOOR_receive[0][2]))
#             self.MSR = struct.pack("B", int(self.AOOR_receive[0][5])) #max sensor rate
#             if self.AOOR_receive[0][3] != 'Off':
#                 self.A_PA = struct.pack("f", float(self.AOOR_receive[0][3]))  # pulse amplitude
#             else:
#                 self.A_PA = struct.pack("f", 0)
#             self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
#             self.A_PW = struct.pack("B", int(self.AOOR_receive[0][4]))  # pulse width
#             self.V_PW = struct.pack("B", 1)  # pulse width
#             self.A_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.V_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.A_R = struct.pack("H", 1)  # ARP
#             self.V_R = struct.pack("H", 1)  # VRP
#             self.PVARP = struct.pack("H", 1)  # PVARP
#             self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.AOOR_receive[0][6]])  # activity threshold
#             self.React_time = struct.pack("B", int(self.AOOR_receive[0][7]))  # reaction time
#             self.Response_factor = struct.pack("B", int(self.AOOR_receive[0][8]))  # response factor
#             self.Recovery_time = struct.pack("B", int(self.AOOR_receive[0][9]))  # recovery time
#         elif self.currentmode == "VOOR":
#             self.VOOR_receive = self.VOOR.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.VOOR_receive[0][1]))
#             self.URL = struct.pack("B", int(self.VOOR_receive[0][2]))
#             self.MSR = struct.pack("B", int(self.VOOR_receive[0][5])) #max sensor rate
#             self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
#             if self.VOOR_receive[0][3] != 'Off':
#                 self.V_PA = struct.pack("f", float(self.VOOR_receive[0][3]))  # pulse amplitude
#             else:
#                 self.V_PA = struct.pack("f", 0)
#             self.A_PW = struct.pack("B", 1)  # pulse width
#             self.V_PW = struct.pack("B", int(self.VOOR_receive[0][4]))  # pulse width
#             self.A_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.V_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.A_R = struct.pack("H", 1)  # ARP
#             self.V_R = struct.pack("H", 1)  # VRP
#             self.PVARP = struct.pack("H", 1)  # PVARP
#             self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.VOOR_receive[0][6]])  # activity threshold
#             self.React_time = struct.pack("B", int(self.VOOR_receive[0][7]))  # reaction time
#             self.Response_factor = struct.pack("B", int(self.VOOR_receive[0][8]))  # response factor
#             self.Recovery_time = struct.pack("B", int(self.VOOR_receive[0][9]))  # recovery time
#         elif self.currentmode == "AAIR":
#             self.AAIR_receive = self.AAIR.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.AAIR_receive[0][1]))
#             self.URL = struct.pack("B", int(self.AAIR_receive[0][2]))
#             self.MSR = struct.pack("B", int(self.AAIR_receive[0][5])) #max sensor rate
#             if self.AAIR_receive[0][2] != 'Off':
#                 self.A_PA = struct.pack("f", float(self.AAIR_receive[0][3]))  # pulse amplitude
#             else:
#                 self.A_PA = struct.pack("f", 0)
#             self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
#             self.A_PW = struct.pack("B", int(self.AAIR_receive[0][4]))  # pulse width
#             self.V_PW = struct.pack("B", 1)  # pulse width
#             self.A_Sense = struct.pack("f", float(self.AAIR_receive[0][6]))  # sensitivity
#             self.V_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.A_R = struct.pack("H", int(self.AAIR_receive[0][7]))  # ARP
#             self.V_R = struct.pack("H", 1)  # VRP
#             self.PVARP = struct.pack("H", int(self.AAIR_receive[0][8]))  # PVARP
#             self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.AAIR_receive[0][9]])  # activity threshold
#             self.React_time = struct.pack("B", int(self.AAIR_receive[0][10]))  # reaction time
#             self.Response_factor = struct.pack("B", int(self.AAIR_receive[0][11]))  # response factor
#             self.Recovery_time = struct.pack("B", int(self.AAIR_receive[0][12]))  # recovery time
#         elif self.currentmode == "VVIR":
#             self.VVIR_receive = self.VVIR.Search(self.userID)
#             self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
#             self.LRL = struct.pack("B", int(self.VVIR_receive[0][1]))
#             self.URL = struct.pack("B", int(self.VVIR_receive[0][2]))
#             self.MSR = struct.pack("B", int(self.VVIR_receive[0][5])) #max sensor rate
#             self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
#             if self.VVIR_receive[0][2] != 'Off':
#                 self.V_PA = struct.pack("f", float(self.VVIR_receive[0][3]))  # pulse amplitude
#             else:
#                 self.V_PA = struct.pack("f", 0)  # pulse amplitude
#             self.A_PW = struct.pack("B", 1)  # pulse width
#             self.V_PW = struct.pack("B", int(self.VVIR_receive[0][4]))  # pulse width
#             self.A_Sense = struct.pack("f", 1.0)  # sensitivity
#             self.V_Sense = struct.pack("f", float(self.VVIR_receive[0][6]))  # sensitivity
#             self.A_R = struct.pack("H", 1)  # ARP
#             self.V_R = struct.pack("H", int(self.VVIR_receive[0][7]))  # VRP
#             self.PVARP = struct.pack("H", 0)  # PVARP
#             self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.VVIR_receive[0][8]])  # activity threshold
#             self.React_time = struct.pack("B", int(self.VVIR_receive[0][9]))  # reaction time
#             self.Response_factor = struct.pack("B", int(self.VVIR_receive[0][10]))  # response factor
#             self.Recovery_time = struct.pack("B", int(self.VVIR_receive[0][11]))  # recovery time
#
#     def getAtr(self):
#         return self.Atr
#
#     def getVnt(self):
#         return self.Vnt





class animateGraph:

    # pass in pacemakerSerial object on  init, assumes you already have on instantiated
    def __init__(self, pacemakerSerial, userID, loggedinwindow):
        # for serial com
        self.pacemaker = pacemakerSerial
        self.UserID = userID
        # for plot
        self.inc = 0
        self.time = 0
        self.fig = plt.figure()
        self.loggedin = loggedinwindow
        self.loggedin.withdraw()
        #self.fig.canvas.mpl_connect('close_event', self.on_close)
        print(plt.get_fignums())
        #print(self.fig.number)
        self.ax1 = self.fig.add_subplot(1, 1, 1)

    def addToFile(self):

        # saved as: time, Atr, Vnt
        f = open('sampleText.txt', 'r')
        self.time = f.readline().split(',')[0]  # pulls most recent time to increment
        self.inc += float(0.5)
        self.time += str(self.inc)
        f.close()

        # pulls new Atr and Vnt values from pacemaker... loop this to get more values , but keep animate interval in mind
        self.pacemaker.get_echo()

        f = open('EGRAM_vals.txt', 'a')
        writeVal = str(self.time) + ',' + str(self.pacemaker.getAtr()) + ',' + str(self.pacemaker.getVnt()) + '\n'
        f.write(writeVal)
        f.close()

    def animate(self, i):
        self.addToFile()  # update vals

        pullData = open("EGRAM_vals.txt", "r").read()  # must use txt file for input, else graph wont update

        # saved as: time, Atr, Vnt
        dataArray = pullData.split('\n')
        tar = []
        aar = []
        var = []
        for eachLine in dataArray[-21:-1]: # pulls last 20 lines from txt file
            if len(eachLine) > 1:
                t, a, v = eachLine.split(',')
                tar.append(str(t))
                aar.append(str(a))
                var.append(str(v))
        self.ax1.clear()
        self.ax1.plot(tar, aar, label="Atrial")
        self.ax1.plot(tar, var, label="Ventrical")
        self.ax1.legend()

    # run this to open the plot
    def showPlot(self):
        ani = animation.FuncAnimation(self.fig, self.animate, interval=10)  # refresh every 10ms
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        plt.show()

    def on_close(self, event):
        print('Closed Figure!')
        self.loggedin = LoggedInWindow(self.UserID)
        f = open("EGRAM_vals.txt","w")
        f.write('0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n0,0,0\n')


#stores the login creditals


class pacemakerSerial:
    def __init__(self, UserID):
        # Mac ports, for windows you have to find the ports yourself
        self.frdm_port = "/dev/cu.usbmodem0000001234561"

        # B = uint8
        # f = single
        # H = uint16
        # d = double ( 8 bytes)

        self.Start = b'\x16'
        self.SYNC = b'\x22'
        self.Fn_set = b'\x55'
        self.Pacing_mode = struct.pack("B", 1)
        self.LRL = struct.pack("B", 1)
        self.URL = struct.pack("B", 1)
        self.MSR = struct.pack("B", 1)
        self.A_PA = struct.pack("f", 1.0)
        self.V_PA = struct.pack("f", 1.0)
        self.A_PW = struct.pack("B", 1)
        self.V_PW = struct.pack("B", 1)
        self.A_Sense = struct.pack("f", 1)
        self.V_Sense = struct.pack("f", 1)
        self.A_R = struct.pack("H", 1)
        self.V_R = struct.pack("H", 1)
        self.PVARP = struct.pack("H", 1)
        self.Act_thres = struct.pack("B", 1)
        self.React_time = struct.pack("B", 1)
        self.Response_factor = struct.pack("B", 1)
        self.Recovery_time = struct.pack("H", 1)

        self.AOO = AOOParameterDatabase()
        self.VOO = VOOParameterDatabase()
        self.AAI = AAIParameterDatabase()
        self.VVI = VVIParameterDatabase()
        self.AOOR = AOORParameterDatabase()
        self.VOOR = VOORParameterDatabase()
        self.AAIR = AAIRParameterDatabase()
        self.VVIR = VVIRParameterDatabase()
        self.userID = UserID
        # self.cmode = self.login.ReturnMode(self.userID)[0][4]
        self.modeDict = {
            'AOO': 1,
            'AOOR': 2,
            'VOO': 3,
            'VOOR': 4,
            'AAI': 5,
            'AAIR': 6,
            'VVI': 7,
            'VVIR': 8
        }
        self.ActivityThresholdDict = {
            "V-Low": 1,
            'Low': 2,
            'Med-Low': 3,
            'Med': 4,
            'Med-High': 5,
            'High': 6,
            'V-High': 7
        }

    def send_param(self):
        Signal_set = self.Start + self.Fn_set + self.Pacing_mode + self.LRL + self.URL + self.MSR + self.A_PA + self.V_PA + self.A_PW + self.V_PW + self.A_Sense + self.V_Sense + self.A_R + self.V_R + self.PVARP + self.Act_thres + self.React_time + self.Response_factor + self.Recovery_time
        with serial.Serial(self.frdm_port, 115200) as pacemaker:
            pacemaker.write(Signal_set)

    def get_echo(self):
        # Start = b'\x16'
        # SYNC = b'\x22'
        # Fn_set = b'\x55'
        # Pacing_mode = struct.pack("B", 1)
        # LRL = struct.pack("B", 1)
        # URL = struct.pack("B", 1)
        # MSR = struct.pack("B", 1)
        # A_PA = struct.pack("f", 1.0)
        # V_PA = struct.pack("f", 1.0)
        # A_PW = struct.pack("B", 1)
        # V_PW = struct.pack("B", 1)
        # A_Sense = struct.pack("f", 1)
        # V_Sense = struct.pack("f", 1)
        # A_R = struct.pack("H", 1)
        # V_R = struct.pack("H", 1)
        # PVARP = struct.pack("H", 1)
        # Act_thres = struct.pack("B", 1)
        # React_time = struct.pack("B", 1)
        # Response_factor = struct.pack("B", 1)
        # Recovery_time = struct.pack("H", 1)
        Signal_echo = self.Start + self.SYNC + self.Pacing_mode + self.LRL + self.URL + self.MSR + self.A_PA + self.V_PA + self.A_PW + self.V_PW + self.A_Sense + self.V_Sense + self.A_R + self.V_R + self.PVARP + self.Act_thres + self.React_time + self.Response_factor + self.Recovery_time
        #Signal_echo = Start + SYNC + Pacing_mode + LRL + URL + MSR + A_PA + V_PA + A_PW + V_PW + A_Sense + V_Sense + A_R + V_R + PVARP + Act_thres + React_time + Response_factor + Recovery_time

        print(self.LRL)
        with serial.Serial(self.frdm_port, 115200) as pacemaker:
            pacemaker.write(Signal_echo)
            print("before read")
            data = pacemaker.read(49)
            #print(data)
            print("after read")
            Pacing_mode = data[0]
            LRL = data[1]
            URL = data[2]
            MSR = data[3]
            A_PA = struct.unpack("f", data[4:8])[0]
            V_PA = struct.unpack("f", data[8:12])[0]
            A_PW = data[12]
            V_PW = data[13]
            A_Sens = struct.unpack("f", data[14:18])[0]
            V_Sens = struct.unpack("f", data[18:22])[0]
            A_R = struct.unpack("H", data[22:24])[0]
            V_R = struct.unpack("H", data[24:26])[0]
            PVARP = struct.unpack("H", data[26:28])[0]
            Act_thres = data[28]
            React_time = data[29]
            Response_factor = data[30]
            Recovery_time = struct.unpack("H", data[31:33])[0]
            self.Atr = struct.unpack("d", data[33:41])[0]
            self.Vnt = struct.unpack("d", data[41:49])[0]

            print("From the board:")
            print("Pacing_mode = ", Pacing_mode)
            print("LRL = ", LRL)
            print("URL = ", URL)
            print("MSR = ", MSR)
            print("A_PA = ", A_PA)
            print("V_PA = ", V_PA)
            print("A_PW = ", A_PW)
            print("V_PW = ", V_PW)
            print("A_Sens = ", A_Sens)
            print("V_Sens = ", V_Sens)
            print("A_R = ", A_R)
            print("V_R = ", V_R)
            print("PVARP = ", PVARP)
            print("Act_thres = ", Act_thres)
            print("React_time = ", React_time)
            print("Response_factor = ", Response_factor)
            print("Recovery_time = ", Recovery_time)
            print("Atrial graph value = ", self.Atr)
            print("Ventrical graph value = ", self.Vnt)

    def getAtr(self):
        return self.Atr

    def getVnt(self):
        return self.Vnt

    def update(self):
        self.login = LoginDatabase()
        self.currentmode = self.login.ReturnMode(self.userID)[0][4]
        print(self.currentmode)
        if self.currentmode == "AOO":
            self.AOO_receive = self.AOO.Search(self.userID)
            print(self.AOO_receive)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.AOO_receive[0][1]))
            self.URL = struct.pack("B", int(self.AOO_receive[0][2]))
            self.MSR = struct.pack("B", 1) #max sensor rate
            if self.AOO_receive[0][3] != 'Off':
                self.A_PA = struct.pack("f", float(self.AOO_receive[0][3])*20)  # pulse amplitude
            else:
                self.A_PA = struct.pack("f", float(0))
            self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
            self.A_PW = struct.pack("B", int(self.AOO_receive[0][4]))  # pulse width
            self.V_PW = struct.pack("B", 1)  # pulse width
            self.A_Sense = struct.pack("f", 1.0)  # sensitivity
            self.V_Sense = struct.pack("f", 1.0)  # sensitivity
            self.A_R = struct.pack("H", 1)  # ARP
            self.V_R = struct.pack("H", 1)  # VRP
            self.PVARP = struct.pack("H", 1)  # PVARP
            self.Act_thres = struct.pack("B", 1)  # activity threshold
            self.React_time = struct.pack("B", 1)  # reaction time
            self.Response_factor = struct.pack("B", 1)  # response factor
            self.Recovery_time = struct.pack("H", 1)  # recovery time

        elif self.currentmode == "VOO":
            self.VOO_receive = self.VOO.Search(self.userID)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.VOO_receive[0][1]))
            self.URL = struct.pack("B", int(self.VOO_receive[0][2]))
            self.MSR = struct.pack("B", 1) #max sensor rate
            self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
            if self.VOO_receive[0][3] != 'Off':
                self.V_PA = struct.pack("f", float(self.VOO_receive[0][3])*20)  # pulse amplitude
            else:
                self.V_PA = struct.pack("f", float(0))
            self.A_PW = struct.pack("B", 1)  # pulse width
            self.V_PW = struct.pack("B", int(self.VOO_receive[0][4]))  # pulse width
            self.A_Sense = struct.pack("f", 1.0)  # sensitivity
            self.V_Sense = struct.pack("f", 1.0)  # sensitivity
            self.A_R = struct.pack("H", 1)  # ARP
            self.V_R = struct.pack("H", 1)  # VRP
            self.PVARP = struct.pack("H", 1)  # PVARP
            self.Act_thres = struct.pack("B", 1)  # activity threshold
            self.React_time = struct.pack("B", 1)  # reaction time
            self.Response_factor = struct.pack("B", 1)  # response factor
            self.Recovery_time = struct.pack("H", 1)  # recovery time
        elif self.currentmode == "AAI":
            self.AAI_receive = self.AAI.Search(self.userID)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.AAI_receive[0][1]))
            self.URL = struct.pack("B", int(self.AAI_receive[0][2]))
            self.MSR = struct.pack("B", 1) #max sensor rate
            if self.AAI_receive[0][3] != 'Off':
                self.A_PA = struct.pack("f", float(self.AAI_receive[0][3])*20)  # pulse amplitude
            else:
                self.A_PA = struct.pack("f", float(0))  # pulse amplitude
            self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
            self.A_PW = struct.pack("B", int(self.AAI_receive[0][4]))  # pulse width
            self.V_PW = struct.pack("B", 1)  # pulse width
            self.A_Sense = struct.pack("f", float(self.AAI_receive[0][5])*20)  # sensitivity
            self.V_Sense = struct.pack("f", 1.0)  # sensitivity
            self.A_R = struct.pack("H", int(self.AAI_receive[0][6]))  # ARP
            self.V_R = struct.pack("H", 1)  # VRP
            self.PVARP = struct.pack("H", int(self.AAI_receive[0][7]))  # PVARP
            self.Act_thres = struct.pack("B", 1)  # activity threshold
            self.React_time = struct.pack("B", 1)  # reaction time
            self.Response_factor = struct.pack("B", 1)  # response factor
            self.Recovery_time = struct.pack("H", 1)  # recovery time
        elif self.currentmode == "VVI":
            self.VVI_receive = self.VVI.Search(self.userID)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.VVI_receive[0][1]))
            self.URL = struct.pack("B", int(self.VVI_receive[0][2]))
            self.MSR = struct.pack("B", 1) #max sensor rate
            self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
            if self.VVI_receive[0][2] != 'Off':
                self.V_PA = struct.pack("f", float(self.VVI_receive[0][3])*20)  # pulse amplitude
            else:
                self.V_PA = struct.pack("f", float(0))
            self.A_PW = struct.pack("B", 1)  # pulse width
            self.V_PW = struct.pack("B", int(self.VVI_receive[0][4]))  # pulse width
            self.A_Sense = struct.pack("f", 1.0)  # sensitivity
            self.V_Sense = struct.pack("f", float(self.VVI_receive[0][5])*20)  # sensitivity
            self.A_R = struct.pack("H", 1)  # ARP
            self.V_R = struct.pack("H", int(self.VVI_receive[0][6]))  # VRP
            self.PVARP = struct.pack("H", 1)  # PVARP
            self.Act_thres = struct.pack("B", 1)  # activity threshold
            self.React_time = struct.pack("B", 1)  # reaction time
            self.Response_factor = struct.pack("B", 1)  # response factor
            self.Recovery_time = struct.pack("H", 1)  # recovery time
        elif self.currentmode == "AOOR":
            self.AOOR_receive = self.AOOR.Search(self.userID)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.AOOR_receive[0][1]))
            self.URL = struct.pack("B", int(self.AOOR_receive[0][2]))
            self.MSR = struct.pack("B", int(self.AOOR_receive[0][5])) #max sensor rate
            if self.AOOR_receive[0][3] != 'Off':
                self.A_PA = struct.pack("f", float(self.AOOR_receive[0][3])*20)  # pulse amplitude
            else:
                self.A_PA = struct.pack("f", float(0))
            self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
            self.A_PW = struct.pack("B", int(self.AOOR_receive[0][4]))  # pulse width
            self.V_PW = struct.pack("B", 1)  # pulse width
            self.A_Sense = struct.pack("f", 1.0)  # sensitivity
            self.V_Sense = struct.pack("f", 1.0)  # sensitivity
            self.A_R = struct.pack("H", 1)  # ARP
            self.V_R = struct.pack("H", 1)  # VRP
            self.PVARP = struct.pack("H", 1)  # PVARP
            self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.AOOR_receive[0][6]])  # activity threshold
            self.React_time = struct.pack("B", int(self.AOOR_receive[0][7]))  # reaction time
            self.Response_factor = struct.pack("B", int(self.AOOR_receive[0][8]))  # response factor
            self.Recovery_time = struct.pack("H", int(self.AOOR_receive[0][9])*60)  # recovery time
        elif self.currentmode == "VOOR":
            self.VOOR_receive = self.VOOR.Search(self.userID)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.VOOR_receive[0][1]))
            self.URL = struct.pack("B", int(self.VOOR_receive[0][2]))
            self.MSR = struct.pack("B", int(self.VOOR_receive[0][5])) #max sensor rate
            self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
            if self.VOOR_receive[0][3] != 'Off':
                self.V_PA = struct.pack("f", float(self.VOOR_receive[0][3])*20)  # pulse amplitude
            else:
                self.V_PA = struct.pack("f", float(0))
            self.A_PW = struct.pack("B", 1)  # pulse width
            self.V_PW = struct.pack("B", int(self.VOOR_receive[0][4]))  # pulse width
            self.A_Sense = struct.pack("f", 1.0)  # sensitivity
            self.V_Sense = struct.pack("f", 1.0)  # sensitivity
            self.A_R = struct.pack("H", 1)  # ARP
            self.V_R = struct.pack("H", 1)  # VRP
            self.PVARP = struct.pack("H", 1)  # PVARP
            self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.VOOR_receive[0][6]])  # activity threshold
            self.React_time = struct.pack("B", int(self.VOOR_receive[0][7]))  # reaction time
            self.Response_factor = struct.pack("B", int(self.VOOR_receive[0][8]))  # response factor
            self.Recovery_time = struct.pack("H", int(self.VOOR_receive[0][9])*60)  # recovery time
        elif self.currentmode == "AAIR":
            self.AAIR_receive = self.AAIR.Search(self.userID)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.AAIR_receive[0][1]))
            self.URL = struct.pack("B", int(self.AAIR_receive[0][2]))
            self.MSR = struct.pack("B", int(self.AAIR_receive[0][5])) #max sensor rate
            if self.AAIR_receive[0][2] != 'Off':
                self.A_PA = struct.pack("f", float(self.AAIR_receive[0][3])*20)  # pulse amplitude
            else:
                self.A_PA = struct.pack("f", float(0))
            self.V_PA = struct.pack("f", 1.0)  # pulse amplitude
            self.A_PW = struct.pack("B", int(self.AAIR_receive[0][4]))  # pulse width
            self.V_PW = struct.pack("B", 1)  # pulse width
            self.A_Sense = struct.pack("f", float(self.AAIR_receive[0][6])*20)  # sensitivity
            self.V_Sense = struct.pack("f", 1.0)  # sensitivity
            self.A_R = struct.pack("H", int(self.AAIR_receive[0][7]))  # ARP
            self.V_R = struct.pack("H", 1)  # VRP
            self.PVARP = struct.pack("H", int(self.AAIR_receive[0][8]))  # PVARP
            self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.AAIR_receive[0][9]])  # activity threshold
            self.React_time = struct.pack("B", int(self.AAIR_receive[0][10]))  # reaction time
            self.Response_factor = struct.pack("B", int(self.AAIR_receive[0][11]))  # response factor
            self.Recovery_time = struct.pack("H", int(self.AAIR_receive[0][12])*60)  # recovery time
        elif self.currentmode == "VVIR":
            self.VVIR_receive = self.VVIR.Search(self.userID)
            self.Pacing_mode = struct.pack("B", self.modeDict[self.currentmode])
            self.LRL = struct.pack("B", int(self.VVIR_receive[0][1]))
            self.URL = struct.pack("B", int(self.VVIR_receive[0][2]))
            self.MSR = struct.pack("B", int(self.VVIR_receive[0][5])) #max sensor rate
            self.A_PA = struct.pack("f", 1.0)  # pulse amplitude
            if self.VVIR_receive[0][2] != 'Off':
                self.V_PA = struct.pack("f", float(self.VVIR_receive[0][3])*20)  # pulse amplitude
            else:
                self.V_PA = struct.pack("f", float(0))  # pulse amplitude
            self.A_PW = struct.pack("B", 1)  # pulse width
            self.V_PW = struct.pack("B", int(self.VVIR_receive[0][4]))  # pulse width
            self.A_Sense = struct.pack("f", 1.0)  # sensitivity
            self.V_Sense = struct.pack("f", float(self.VVIR_receive[0][6])*20)  # sensitivity
            self.A_R = struct.pack("H", 1)  # ARP
            self.V_R = struct.pack("H", int(self.VVIR_receive[0][7]))  # VRP
            self.PVARP = struct.pack("H", 0)  # PVARP
            self.Act_thres = struct.pack("B", self.ActivityThresholdDict[self.VVIR_receive[0][8]])  # activity threshold
            self.React_time = struct.pack("B", int(self.VVIR_receive[0][9]))  # reaction time
            self.Response_factor = struct.pack("B", int(self.VVIR_receive[0][10]))  # response factor
            self.Recovery_time = struct.pack("H", int(self.VVIR_receive[0][11])*60)  # recovery time

        print('\n\n\n\n\n')
class LoginDatabase:
    def __init__(self):
        #creates the table and put userID, firstname, lastname, password and mode as input stored variables
        #name the database
        self.dbConnection = sqlite3.connect("userlogin.db")
        #sets the cursor
        self.dbCursor = self.dbConnection.cursor()
        #the command of the cursor, creating a table where userID cannot be repeated
        self.dbCursor.execute(
            "CREATE TABLE IF NOT EXISTS Login_table (userID PRIMARYKEY text unique, firstname text, lastname text, password text, mode text)")

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()
    #insert the provided data into the database
    def Insert(self, userID, firstname, lastname, password, mode):
        self.dbCursor.execute("INSERT INTO Login_table VALUES (?, ?, ?, ?, ?)",
                              (userID, firstname, lastname, password, mode))
        self.dbConnection.commit()
    #search for any previous record of the provided lastname and password
    def Search(self,firstname, lastname, password):
        self.dbCursor.execute("SELECT * FROM Login_table WHERE firstname = ? and lastname = ? and password = ?",
                              (firstname, lastname,password))
        searchResults = self.dbCursor.fetchall()
        return searchResults
    #display the entire table
    def Display(self):
        self.dbCursor.execute("SELECT * FROM Login_table")
        records = self.dbCursor.fetchall()
        return records
    #check for how many rows there are in the database
    def Check(self):
        self.dbCursor.execute("SELECT COUNT(*) FROM Login_table")
        result = self.dbCursor.fetchone()
        return result
    #return information based on the userID, mostly the mode
    def ReturnMode(self, userID):
        self.dbCursor.execute("SELECT * FROM Login_table WHERE UserID = ?", (userID,))
        moderesult = self.dbCursor.fetchall()
        return moderesult
    #sets the command based on the input and the userID
    def setMode(self, command, userID):
        self.dbCursor.execute(command,userID)
        self.dbConnection.commit()
    #check for existance of the provided first and last name, returns boolean
    def CheckName(self, firstname, lastname):
        self.dbCursor.execute("SELECT EXISTS(SELECT * from Login_table WHERE firstname = ? and lastname = ?)",
                            (firstname, lastname))
        result = self.dbCursor.fetchall()
        return result


#stores the AAI parameters
class AAIParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("AAIparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS AAIparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, AtrialAmplitude text, AtrialWidth text, AtrialSensitivity text, ARP text, PVARP text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()

    def Insert(self, userID, LRL, URL,Atrial_Amplitude, Atrial_Pulse_Width, Atrial_Sensitivity, ARP, PVARP):
        self.Cursor.execute("INSERT INTO AAIparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width,Atrial_Sensitivity, ARP, PVARP))
        self.connection.commit()

    def Display(self):
        self.Cursor.execute("SELECT * FROM AAIparameter_table")
        records = self.Cursor.fetchall()
        return records

    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM AAIparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults

    def Update(self, LRL, URL,Atrial_Amplitude, Atrial_Pulse_Width, Atrial_Sensitivity, ARP, PVARP, userID):
        self.Cursor.execute(
            "UPDATE AAIparameter_table SET LRL = ?, URL = ?, AtrialAmplitude = ?, AtrialWidth = ?, AtrialSensitivity = ?, ARP = ?, PVARP = ? WHERE userID = ?",
            (LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width,Atrial_Sensitivity, ARP, PVARP, userID))
        self.connection.commit()

    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from AAIparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


#stores the VVI parameters
class VVIParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("VVIparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS VVIparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, VentricularAmplitude text, VentricularWidth text, VentricularSensitivity text, VRP text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()

    def Insert(self, userID, LRL, URL,Ventricular_Amplitude, Ventricular_Pulse_Width, Ventricular_Sensitivity, VRP):
        self.Cursor.execute("INSERT INTO VVIparameter_table VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Ventricular_Amplitude,Ventricular_Pulse_Width,Ventricular_Sensitivity, VRP))
        self.connection.commit()

    def Display(self):
        self.Cursor.execute("SELECT * FROM VVIparameter_table")
        records = self.Cursor.fetchall()
        return records

    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM VVIparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults

    def Update(self, LRL, URL,Ventricular_Amplitude, Ventricular_Pulse_Width, Ventricular_Sensitivity, VRP, userID):
        self.Cursor.execute(
            "UPDATE VVIparameter_table SET LRL = ?, URL = ?, VentricularAmplitude = ?, VentricularWidth = ?, VentricularSensitivity = ?, VRP = ? WHERE userID = ?",
            (LRL, URL, Ventricular_Amplitude,Ventricular_Pulse_Width,Ventricular_Sensitivity, VRP, userID))
        self.connection.commit()

    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from VVIparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


#stores the AOO parameters
class AOOParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("AOOparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS AOOparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, AtrialAmplitude text, AtrialWidth text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()

    def Insert(self, userID, LRL, URL,Atrial_Amplitude, Atrial_Pulse_Width):
        self.Cursor.execute("INSERT INTO AOOparameter_table VALUES (?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width))
        self.connection.commit()

    def Display(self):
        self.Cursor.execute("SELECT * FROM AOOparameter_table")
        records = self.Cursor.fetchall()
        return records

    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM AOOparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults

    def Update(self, LRL, URL, Atrial_Amplitude, Atrial_Pulse_Width, userID):
        self.Cursor.execute(
            "UPDATE AOOparameter_table SET LRL = ?, URL = ?, AtrialAmplitude = ?, AtrialWidth = ? WHERE userID = ?",
            (LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width, userID))
        self.connection.commit()

    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from AOOparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


#stores the VOO parameters
class VOOParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("VOOparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS VOOparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, VentricularAmplitude text, VentricularWidth text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()
        #insert into the database
    def Insert(self, userID, LRL, URL,Ventricular_Amplitude, Ventricular_Pulse_Width):
        self.Cursor.execute("INSERT INTO VOOparameter_table VALUES (?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Ventricular_Amplitude,Ventricular_Pulse_Width))
        self.connection.commit()
    #display the parameters
    def Display(self):
        self.Cursor.execute("SELECT * FROM VOOparameter_table")
        records = self.Cursor.fetchall()
        return records
    #search based on the userID
    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM VOOparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults
    #update the database
    def Update(self, LRL, URL, Ventricular_Amplitude, Ventricular_Pulse_Width, userID):
        self.Cursor.execute(
            "UPDATE VOOparameter_table SET LRL = ?, URL = ?, VentricularAmplitude = ?, VentricularWidth = ? WHERE userID = ?",
            (LRL, URL, Ventricular_Amplitude,Ventricular_Pulse_Width, userID))
        self.connection.commit()
    #checking if there is anything using the userID in the database, returns boolean
    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from VOOparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


class AOORParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("AOORparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS AOORparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, AtrialAmplitude text, AtrialWidth text, MaxSensorRate text, ActivityThreshold text, ReactionTime text, ResponseFactor text, RecoveryTime text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()
        #insert into the database
    def Insert(self, userID, LRL, URL,Atrial_Amplitude, Atrial_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time):
        self.Cursor.execute("INSERT INTO AOORparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Atrial_Amplitude,Atrial_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time))
        self.connection.commit()
    #display the parameters
    def Display(self):
        self.Cursor.execute("SELECT * FROM AOORparameter_table")
        records = self.Cursor.fetchall()
        return records
    #search based on the userID
    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM AOORparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults
    #update the database
    def Update(self, LRL, URL,Atrial_Amplitude, Atrial_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID):
        self.Cursor.execute(
            "UPDATE AOORparameter_table SET LRL = ?, URL = ?, AtrialAmplitude = ?, AtrialWidth = ?, MaxSensorRate = ?, ActivityThreshold = ?, ReactionTime = ?, ResponseFactor = ?, RecoveryTime = ? WHERE userID = ?",
            (LRL, URL,Atrial_Amplitude, Atrial_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID))
        self.connection.commit()
    #checking if there is anything using the userID in the database, returns boolean
    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from AOORparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


class VOORParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("VOORparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS VOORparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, VentricularAmplitude text, VentricularWidth text, MaxSensorRate text, ActivityThreshold text, ReactionTime text, ResponseFactor text, RecoveryTime text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()
        #insert into the database
    def Insert(self, userID, LRL, URL,Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time):
        self.Cursor.execute("INSERT INTO VOORparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time))
        self.connection.commit()
    #display the parameters
    def Display(self):
        self.Cursor.execute("SELECT * FROM VOORparameter_table")
        records = self.Cursor.fetchall()
        return records
    #search based on the userID
    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM VOORparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults
    #update the database
    def Update(self, LRL, URL,Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID):
        self.Cursor.execute(
            "UPDATE VOORparameter_table SET LRL = ?, URL = ?, VentricularAmplitude = ?, VentricularWidth = ?, MaxSensorRate = ?, ActivityThreshold = ?, ReactionTime = ?, ResponseFactor = ?, RecoveryTime = ? WHERE userID = ?",
            (LRL, URL,Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID))
        self.connection.commit()
    #checking if there is anything using the userID in the database, returns boolean
    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from VOORparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


class AAIRParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("AAIRparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS AAIRparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, AtrialAmplitude text, AtrialWidth text, MaxSensorRate text, AtrialSensitivity text, ARP text, PVARP text, ActivityThreshold text, ReactionTime text, ResponseFactor text, RecoveryTime text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()
        #insert into the database
    def Insert(self, userID, LRL, URL,Atrial_Amplitude, Atrial_Width, Max_Sensor_Rate, Atrial_Sensitivity, ARP, PVARP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time):
        self.Cursor.execute("INSERT INTO AAIRparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Atrial_Amplitude, Atrial_Width, Max_Sensor_Rate, Atrial_Sensitivity, ARP, PVARP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time))
        self.connection.commit()
    #display the parameters
    def Display(self):
        self.Cursor.execute("SELECT * FROM AAIRparameter_table")
        records = self.Cursor.fetchall()
        return records
    #search based on the userID
    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM AAIRparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults
    #update the database
    def Update(self, LRL, URL,Atrial_Amplitude, Atrial_Width, Max_Sensor_Rate, Atrial_Sensitivity, ARP, PVARP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID):
        self.Cursor.execute(
            "UPDATE AAIRparameter_table SET LRL = ?, URL = ?, AtrialAmplitude = ?, AtrialWidth = ?, MaxSensorRate = ?, AtrialSensitivity = ?, ARP = ?, PVARP = ?, ActivityThreshold = ?, ReactionTime = ?, ResponseFactor = ?, RecoveryTime = ? WHERE userID = ?",
            (LRL, URL,Atrial_Amplitude, Atrial_Width, Max_Sensor_Rate, Atrial_Sensitivity, ARP, PVARP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID))
        self.connection.commit()
    #checking if there is anything using the userID in the database, returns boolean
    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from AAIRparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


class VVIRParameterDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("VVIRparameter.db")
        self.Cursor = self.connection.cursor()
        self.Cursor.execute(
            "CREATE TABLE IF NOT EXISTS VVIRparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, VentricularAmplitude text, VentricularWidth text, MaxSensorRate text, VentricularSensitivity text, VRP text, ActivityThreshold text, ReactionTime text, ResponseFactor text, RecoveryTime text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()
        #insert into the database
    def Insert(self, userID, LRL, URL,Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Ventricular_Sensitivity, VRP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time):
        self.Cursor.execute("INSERT INTO VVIRparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Ventricular_Sensitivity, VRP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time))
        self.connection.commit()
    #display the parameters
    def Display(self):
        self.Cursor.execute("SELECT * FROM VVIRparameter_table")
        records = self.Cursor.fetchall()
        return records
    #search based on the userID
    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM VVIRparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults
    #update the database
    def Update(self, LRL, URL,Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Ventricular_Sensitivity, VRP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID):
        self.Cursor.execute(
            "UPDATE VVIRparameter_table SET LRL = ?, URL = ?, VentricularAmplitude = ?, VentricularWidth = ?, MaxSensorRate = ?, VentricularSensitivity = ?, VRP = ?, ActivityThreshold = ?, ReactionTime = ?, ResponseFactor = ?, RecoveryTime = ? WHERE userID = ?",
            (LRL, URL,Ventricular_Amplitude, Ventricular_Width, Max_Sensor_Rate, Ventricular_Sensitivity, VRP, Activity_Threshold, Reaction_Time, Response_Factor, Recovery_Time, userID))
        self.connection.commit()
    #checking if there is anything using the userID in the database, returns boolean
    def Empty(self, userID):
        self.Cursor.execute("SELECT EXISTS(SELECT * from VVIRparameter_table WHERE UserID = ?)", (userID,))
        result = self.Cursor.fetchall()
        return result


#checking mechanism for the inputs
class Values:
    def __init__(self):
        self.login = LoginDatabase()
        self.num = self.login.Check()[0]

    def Validate(self, firstname, lastname, password, passwordreentry):
        if not (firstname.isalpha()):
            return "firstname"
        elif not (lastname.isalpha()):
            return "lastname"
        elif password != passwordreentry:
            return "password does not match"
        #checking if the first and last name have been registered in the system
        elif self.login.CheckName(firstname, lastname)[0][0] == 1:
            return "user already exist"
        else:
            return "SUCCESS"


#opens and initializes the registration window
class RegisterationWindow:
    def __init__(self, userID, homewindow):
        self.window = tkinter.Tk()
        self.UserID = userID
        self.window.wm_title("Registration")
        self.homepage = homewindow
        if 'normal' == self.window.state():
            self.homepage.withdraw()
        bg_color = "Blue"
        fg_color = "white"
        cha_color = "black"
        self.mode = " "
        #sets the type of variable for the entries
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.passwordreentry = tkinter.StringVar()

        # Labels
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, text="First Name",
                      font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Last Name", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Password", width=25).grid(pady=5, column=1, row=4)
        tkinter.Label(self.window, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Password Reentry", width=25).grid(pady=5, column=1, row=5)
        #receives the entry
        self.firstnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.window, width=25, textvariable=self.lastname)
        self.passwordEntry = tkinter.Entry(self.window, width=25, textvariable=self.password)
        self.passwordreEntry = tkinter.Entry(self.window, width=25, textvariable=self.passwordreentry)
        #location of the entry box
        self.firstnameEntry.grid(pady=5, column=3, row=2)
        self.lastnameEntry.grid(pady=5, column=3, row=3)
        self.passwordEntry.grid(pady=5, column=3, row=4)
        self.passwordreEntry.grid(pady=5, column=3, row=5)

        # Button widgets
        tkinter.Button(self.window, width=10, fg=cha_color, bg=bg_color, font=("times new roman",10,"bold"),
                       text="Submit", command=self.Submit).grid(pady=15, padx=5, column=1,row=14)
        tkinter.Button(self.window, width=10, fg=cha_color, bg=bg_color, font=("times new roman",10,"bold"),
                       text="Reset", command=self.Reset).grid(pady=15, padx=5, column=2, row=14)
        tkinter.Button(self.window, width=10, fg=cha_color, bg=bg_color, font=("times new roman",10,"bold"),
                       text="Close", command=self.close).grid(pady=15, padx=5, column=3,row=14)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


    def on_closing(self):
        self.window.destroy()
        self.homepage.deiconify()

    def close(self):
        self.window.destroy()
        self.homepage.deiconify()

    def Submit(self):
        self.values = Values()
        self.database = LoginDatabase()
        #will use the validate function to check the inputs
        self.test = self.values.Validate(self.firstnameEntry.get(), self.lastnameEntry.get(),
                                         self.passwordEntry.get(),self.passwordreEntry.get())
        #if input is proper, will insert the inputs into the database
        if self.test == "SUCCESS":
            self.database.Insert(self.UserID, self.firstnameEntry.get(), self.lastnameEntry.get(),
                                 self.passwordEntry.get(), self.mode)
            tkinter.messagebox.showinfo("Inserted data", "Successfully registered. Please Log in now!")
            #closes the registration window
            self.window.destroy()
            self.homepage.deiconify()
            #return error message
        else:
            self.valueErrorMessage = "Invalid input in field " + self.test
            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)
            self.Reset()
        #resets the input boxes
    def Reset(self):
        self.firstnameEntry.delete(0, tkinter.END)
        self.lastnameEntry.delete(0, tkinter.END)
        self.passwordEntry.delete(0,tkinter.END)
        self.passwordreEntry.delete(0, tkinter.END)


#the database that will load when displaying the AAI parameters
class AAIparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("AAI Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "AtrialAmplitude", "AtrialWidth","AtrialSensitivity",
                                        "ARP", "PVARP")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("AtrialAmplitude", text="AtrialAmplitude")
        self.databaseView.heading("AtrialWidth", text="AtrialWidth")
        self.databaseView.heading("AtrialSensitivity", text="AtrialSensitivity")
        self.databaseView.heading("ARP", text="ARP")
        self.databaseView.heading("PVARP", text="PVARP")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("AtrialAmplitude", width=100)
        self.databaseView.column("AtrialWidth", width=100)
        self.databaseView.column("AtrialSensitivity", width=100)
        self.databaseView.column("ARP", width=100)
        self.databaseView.column("PVARP", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


#the database that will load when displaying the VVI parameters
class VVIparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("VVI Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "VentricularAmplitude", "VentricularWidth",
                                        "VentricularSensitivity", "VRP")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("VentricularAmplitude", text="VentricularAmplitude")
        self.databaseView.heading("VentricularWidth", text="VentricularWidth")
        self.databaseView.heading("VentricularSensitivity", text="VentricularSensitivity")
        self.databaseView.heading("VRP", text="VRP")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("VentricularAmplitude", width=100)
        self.databaseView.column("VentricularWidth", width=100)
        self.databaseView.column("VentricularSensitivity", width=100)
        self.databaseView.column("VRP", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


#the database that will load when displaying the AOO parameters
class AOOparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("AOO Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "AtrialAmplitude", "AtrialWidth")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("AtrialAmplitude", text="AtrialAmplitude")
        self.databaseView.heading("AtrialWidth", text="AtrialWidth")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("AtrialAmplitude", width=100)
        self.databaseView.column("AtrialWidth", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


#the database that will load when displaying the VOO parameters
class VOOparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("VOO Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "VentricularAmplitude", "VentricularWidth")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("VentricularAmplitude", text="VentricularAmplitude")
        self.databaseView.heading("VentricularWidth", text="VentricularWidth")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("VentricularAmplitude", width=100)
        self.databaseView.column("VentricularWidth", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()

#AOOR parameters database
class AOORparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("AOOR Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "AtrialAmplitude", "AtrialWidth", "MaxSensorRate", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("AtrialAmplitude", text="AtrialAmplitude")
        self.databaseView.heading("AtrialWidth", text="AtrialWidth")
        self.databaseView.heading("MaxSensorRate", text="MaxSensorRate")
        self.databaseView.heading("ActivityThreshold", text="ActivityThreshold")
        self.databaseView.heading("ReactionTime", text="ReactionTime")
        self.databaseView.heading("ResponseFactor", text="ResponseFactor")
        self.databaseView.heading("RecoveryTime", text="RecoveryTime")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("AtrialAmplitude", width=100)
        self.databaseView.column("AtrialWidth", width=100)
        self.databaseView.column("MaxSensorRate", width=100)
        self.databaseView.column("ActivityThreshold", width=100)
        self.databaseView.column("ReactionTime", width=100)
        self.databaseView.column("ResponseFactor", width=100)
        self.databaseView.column("RecoveryTime", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


class VOORparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("VOOR Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "VentricularAmplitude", "VentricularWidth", "MaxSensorRate", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("VentricularAmplitude", text="VentricularAmplitude")
        self.databaseView.heading("VentricularWidth", text="VentricularWidth")
        self.databaseView.heading("MaxSensorRate", text="MaxSensorRate")
        self.databaseView.heading("ActivityThreshold", text="ActivityThreshold")
        self.databaseView.heading("ReactionTime", text="ReactionTime")
        self.databaseView.heading("ResponseFactor", text="ResponseFactor")
        self.databaseView.heading("RecoveryTime", text="RecoveryTime")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("VentricularAmplitude", width=100)
        self.databaseView.column("VentricularWidth", width=100)
        self.databaseView.column("MaxSensorRate", width=100)
        self.databaseView.column("ActivityThreshold", width=100)
        self.databaseView.column("ReactionTime", width=100)
        self.databaseView.column("ResponseFactor", width=100)
        self.databaseView.column("RecoveryTime", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


class AAIRparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("AAIR Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "AtrialAmplitude", "AtrialWidth", "MaxSensorRate", "AtrialSensitivity", "ARP", "PVARP", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("AtrialAmplitude", text="AtrialAmplitude")
        self.databaseView.heading("AtrialWidth", text="AtrialWidth")
        self.databaseView.heading("MaxSensorRate", text="MaxSensorRate")
        self.databaseView.heading("AtrialSensitivity", text="AtrialSensitivity")
        self.databaseView.heading("ARP", text="ARP")
        self.databaseView.heading("PVARP", text="PVARP")
        self.databaseView.heading("ActivityThreshold", text="ActivityThreshold")
        self.databaseView.heading("ReactionTime", text="ReactionTime")
        self.databaseView.heading("ResponseFactor", text="ResponseFactor")
        self.databaseView.heading("RecoveryTime", text="RecoveryTime")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("AtrialAmplitude", width=100)
        self.databaseView.column("AtrialWidth", width=100)
        self.databaseView.column("MaxSensorRate", width=100)
        self.databaseView.column("AtrialSensitivity", width=100)
        self.databaseView.column("ARP", width=100)
        self.databaseView.column("PVARP", width=100)
        self.databaseView.column("ActivityThreshold", width=100)
        self.databaseView.column("ReactionTime", width=100)
        self.databaseView.column("ResponseFactor", width=100)
        self.databaseView.column("RecoveryTime", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


class VVIRparametersDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("VVIR Parameters Database View")

        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID", "LRL", "URL", "VentricularAmplitude", "VentricularWidth", "MaxSensorRate", "VentricularSensitivity", "VRP", "ActivityThreshold", "ReactionTime", "ResponseFactor", "RecoveryTime")
        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("VentricularAmplitude", text="VentricularAmplitude")
        self.databaseView.heading("VentricularWidth", text="VentricularWidth")
        self.databaseView.heading("MaxSensorRate", text="MaxSensorRate")
        self.databaseView.heading("VentricularSensitivity", text="VentricularSensitivity")
        self.databaseView.heading("VRP", text="VRP")
        self.databaseView.heading("ActivityThreshold", text="ActivityThreshold")
        self.databaseView.heading("ReactionTime", text="ReactionTime")
        self.databaseView.heading("ResponseFactor", text="ResponseFactor")
        self.databaseView.heading("RecoveryTime", text="RecoveryTime")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("VentricularAmplitude", width=100)
        self.databaseView.column("VentricularWidth", width=100)
        self.databaseView.column("MaxSensorRate", width=100)
        self.databaseView.column("VentricularSensitivity", width=100)
        self.databaseView.column("VRP", width=100)
        self.databaseView.column("ActivityThreshold", width=100)
        self.databaseView.column("ReactionTime", width=100)
        self.databaseView.column("ResponseFactor", width=100)
        self.databaseView.column("RecoveryTime", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()


#the database that will load when displaying the table
class LoginDatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.wm_title("Login Database View")

        # Label widgets
        tkinter.Label(self.databaseViewWindow, text="Database View Window", width=25).grid(pady=5, column=1, row=1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady=5, column=1, row=2)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("UserID","firstname", "lastname","Password", "Mode")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("firstname", text="First Name")
        self.databaseView.heading("lastname", text="Last Name")
        self.databaseView.heading("Password", text="Password")
        self.databaseView.heading("Mode", text="Mode")

        # Treeview columns
        self.databaseView.column("UserID", width=100)
        self.databaseView.column("firstname", width=100)
        self.databaseView.column("lastname", width=100)
        self.databaseView.column("Password",width=100)
        self.databaseView.column("Mode", width=100)

        for record in data:
            self.databaseView.insert('', 'end', values=(record))

        self.databaseViewWindow.mainloop()

#opens and initializes the login window
class LoginWindow:
    def __init__(self, homepagewindow):
        #creates the window
        self.loginwindow = tkinter.Tk()
        self.loginwindow.wm_title("Login")
        self.UserID = " "
        bg_color = "Blue"
        fg_color = "white"
        cha_color = "black"
        #creates an object of the homepage
        self.homescreen = homepagewindow
        if 'normal' == self.loginwindow.state():
            self.homescreen.withdraw()
        #sets the type of the input
        self.firstname = tkinter.StringVar()
        self.lastname = tkinter.StringVar()
        self.password = tkinter.StringVar()

        tkinter.Label(self.loginwindow, fg=fg_color, bg=bg_color, text="First Name",
                      font=("times new roman", 10, "bold"), width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.loginwindow, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Last Name", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.loginwindow, fg=fg_color, bg=bg_color, font=("times new roman", 10, "bold"),
                      text="Password", width=25).grid(pady=5, column=1, row=4)
        #stores the input
        self.firstnameEntry = tkinter.Entry(self.loginwindow, width=25, textvariable=self.firstname)
        self.lastnameEntry = tkinter.Entry(self.loginwindow, width=25, textvariable=self.lastname)
        self.passwordEntry = tkinter.Entry(self.loginwindow, width=25, textvariable=self.password)
        #locate the input box
        self.firstnameEntry.grid(pady=5, column=3, row=2)
        self.lastnameEntry.grid(pady=5, column=3, row=3)
        self.passwordEntry.grid(pady=5, column=3, row=4)
        #submit the login request
        submitbutton = tkinter.Button(self.loginwindow, width=10, fg=cha_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Submit", command=self.Submit)
        submitbutton.grid(pady=15, padx=5, column=1,row=14)
        submitbutton.bind('<KP_Enter>', self.Submit)
        tkinter.Button(self.loginwindow, width=10, fg=cha_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Back to Home", command=self.Home).grid(pady=15, padx=5, column=3, row=14)
        self.loginwindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.loginwindow.mainloop()

    def Home(self):
        self.loginwindow.destroy()
        self.homescreen.deiconify()

    def on_closing(self):
        self.loginwindow.destroy()
        self.homescreen.deiconify()

    def Submit(self):
        #opens the login database and check for users with the same last name and password
        self.values = Values()
        self.database = LoginDatabase()
        self.data = self.database.Search(self.firstnameEntry.get(),self.lastnameEntry.get(), self.passwordEntry.get())
        if self.data:
            #if found, you are logged in
            tkinter.messagebox.showinfo('Login success', "You are logged in!")
            #updates the userID
            self.UserID = self.data[0][0]
            self.logged_in(self.UserID)
        else:
            tkinter.messagebox.showerror("login fail", "Login info not correct! Please try again or register")
    #directs to the logged in welcome page
    def logged_in(self, userID):
        self.logged_in_window = LoggedInWindow(userID)
        #close the previous two windows
        self.loginwindow.destroy()
        self.homescreen.destroy()


#used to initialize and show the logged in page
class LoggedInWindow:
    def __init__(self, userID):
        #creates the window
        self.window = tkinter.Tk()
        self.window.wm_title("Welcome Page")
        self.UserID = userID
        self.serial = pacemakerSerial(self.UserID)
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        warning_color = "red"
        tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Welcome",
                      font=("times new roman", 20, "bold"), width=30).grid(pady=20, column=1, row=1)
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Mode",
                       font=("times new roman", 15, "bold"), command=self.Mode).grid(pady=15, column=1, row=4)
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Parameters",
                       font=("times new roman", 15, "bold"), command=self.Parameters).grid(pady=15, column=1, row=5)
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Load Graph",
                       font=("times new roman", 15, "bold"), command=self.Graph).grid(pady=15, column=1, row=6)
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Sign Out",
                       font=("times new roman", 15, "bold"), command=self.Signout).grid(pady=15, column=1, row=7)
        #if another pacemaker is nearby, it will trigger an alert on the window
        if warning:
            tkinter.Label(self.window, relief=tkinter.GROOVE, fg=warning_color, bg=bg_color,
                          text="Danger! Another Pacemaker nearby!",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
        #if the connection is on, it will display on the window, if not, it will also be on the window
        tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Status update: Connection with DCM is " + "ON" if (connection == True)
                      else "Status update: Connection with DCM is " + "OFF",font=("times new roman", 10, "bold"),
                      width=50).grid(pady=20, column=1, row=2)
    def Graph(self):
        self.graph = GraphWindow(self.UserID, self.window, self.serial)
    def Signout(self):
        self.window.destroy()
        self.homepage = HomePage()
    #directs to the mode window
    def Mode(self):
        self.modewindow = ModeWindow(self.UserID, self.window)

    #directs to the parameters window
    def Parameters(self):
        #creates an object for the login database class
        self.login = LoginDatabase()
        #find the current mode
        self.mode = self.login.ReturnMode(self.UserID)[0][4]
        #if the user never used the system before, will ask them to select mode first before going to the parameters page
        if self.mode == " ":
            tkinter.messagebox.showerror("Invalid Mode", "Select your mode first!")
        else:
            #storing the mode here
            self.logindata = LoginDatabase()
            self.cmode = self.logindata.ReturnMode(self.UserID)[0][4]
            #save the mode into the database
            self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
            #double security and prevents the mode not selected and goes to the parameters window
            try:
                self.parameterWindow = ParametersWindow(self.UserID, self.window, self.serial)
            except AttributeError:
                tkinter.messagebox.showerror("Invalid Mode", "Select your mode first!")


#opens and intializes the parameters window
class ParametersWindow:
    def __init__(self, userID, loggedinwindow, Serial):
        self.UserID = userID
        self.login = LoginDatabase()
        self.result = self.login.ReturnMode(self.UserID)
        self.currentmode = self.result[0][4]
        self.parameterwindow = tkinter.Tk()
        self.parameterwindow.wm_title("Current Parameters")
        self.loggedinpage = loggedinwindow
        #self.serial = pacemakerSerial(self.UserID)
        self.serial = Serial
        if 'normal' == self.parameterwindow.state():
            self.loggedinpage.withdraw()
        self.AAI = AAIParameterDatabase()
        self.VVI = VVIParameterDatabase()
        self.AOO = AOOParameterDatabase()
        self.VOO = VOOParameterDatabase()
        self.AOOR = AOORParameterDatabase()
        self.VOOR = VOORParameterDatabase()
        self.AAIR = AAIRParameterDatabase()
        self.VVIR = VVIRParameterDatabase()
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        self.parameterwindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        #restricts the input allowed in parameters page
        self.LRLtype = list(range(30,50,5))+list(range(50,90))+list(range(90,185,5))
        #print(self.LRLBox.get())
        self.URLtype = list(range(50,180,5)) #self.LRLBox.get() to 180
        #self.URLtype = []
        self.PulseAmplitudetype = ["Off"]+list(self.float_range(1, 5.1, '0.1'))
        self.PulseWidthtype = list(range(1,31,1))
        self.Sensitivitytype = list(self.float_range(0, 5.1, '0.1'))
        self.RPtype = list(range(150,510,10))
        self.PVARPtype = list(range(150,510,10))
        self.MaxSensorRate = list(range(50,180,5))
        self.ActivityThreshold = ["V-Low", 'Low', 'Med-Low', 'Med','Med-High', 'High', 'V-High']
        self.ReactionTime = list(range(10,60,10))
        self.ResponseFactor = list(range(1,17,1))
        self.RecoveryTime = list(range(2,17,1))


        #operational buttons
        self.generalbuttonsetup(bg_color, fg_color, cha_color)
        #the parameters shown when mode is AAI
        if self.currentmode == "AAI":
            self.AAIsetup(bg_color, fg_color)
            #search whether the database have any previous saved parameters
            self.search = []
            self.searchresult = self.AAI.Search(self.UserID)
            self.another = self.AAI.Empty(self.UserID)
            #if there are previous saved parameters load them onto the comboboxes
            if self.another[0][0] == 1:
                self.LRLBox.set(self.searchresult[0][1])
                self.URLBox.set(self.searchresult[0][2])
                self.PulseAmplitudeBox.set(self.searchresult[0][3])
                self.PulseWidthBox.set(self.searchresult[0][4])
                self.SensitivityBox.set(self.searchresult[0][5])
                self.ARPBox.set(self.searchresult[0][6])
                self.PVARPBox.set(self.searchresult[0][7])
            else:
                self.AAIdefaultSetting()

        elif self.currentmode == "VVI":
            self.VVIsetup(bg_color, fg_color)
            self.search = []
            self.searchresult = self.VVI.Search(self.UserID)
            self.another = self.VVI.Empty(self.UserID)
            if self.another[0][0] == 1:
                self.LRLBox.set(self.searchresult[0][1])
                self.URLBox.set(self.searchresult[0][2])
                self.PulseAmplitudeBox.set(self.searchresult[0][3])
                self.PulseWidthBox.set(self.searchresult[0][4])
                self.SensitivityBox.set(self.searchresult[0][5])
                self.VRPBox.set(self.searchresult[0][6])
            else:
                self.VVIdefaultSetting()

        elif self.currentmode == "AOO":
            self.AOOsetup(bg_color,fg_color)
            self.search = []
            self.searchresult = self.AOO.Search(self.UserID)
            self.another = self.AOO.Empty(self.UserID)
            if self.another[0][0] == 1:
                self.LRLBox.set(self.searchresult[0][1])
                self.URLBox.set(self.searchresult[0][2])
                self.PulseAmplitudeBox.set(self.searchresult[0][3])
                self.PulseWidthBox.set(self.searchresult[0][4])
            else:
                self.AOOVOOdefaultSetting()

        elif self.currentmode == "VOO":
            self.VOOsetup(bg_color,fg_color)
            self.search = []
            self.searchresult = self.VOO.Search(self.UserID)
            self.another = self.VOO.Empty(self.UserID)
            if self.another[0][0] == 1:
                self.LRLBox.set(self.searchresult[0][1])
                self.URLBox.set(self.searchresult[0][2])
                self.PulseAmplitudeBox.set(self.searchresult[0][3])
                self.PulseWidthBox.set(self.searchresult[0][4])
            else:
                self.AOOVOOdefaultSetting()

        elif self.currentmode == "AOOR":
            self.AOORVOORRepsetup(bg_color, fg_color)
            self.AOORsetup(bg_color, fg_color)
            self.search = []
            self.searchresult = self.AOOR.Search(self.UserID)
            self.another = self.AOOR.Empty(self.UserID)
            if self.another[0][0] == 1:
                self.AOORVOORinputrep()
            else:
                self.AOORVOORdefaultSetting()

        elif self.currentmode == "VOOR":
            self.AOORVOORRepsetup(bg_color, fg_color)
            self.VOORsetup(bg_color, fg_color)
            self.search = []
            self.searchresult = self.VOOR.Search(self.UserID)
            self.another = self.VOOR.Empty(self.UserID)
            if self.another[0][0] == 1:
                self.AOORVOORinputrep()
            else:
                self.AOORVOORdefaultSetting()

        elif self.currentmode == "AAIR":
            self.AAIRsetup(bg_color, fg_color)
            self.search = []
            self.searchresult = self.AAIR.Search(self.UserID)
            self.another = self.AAIR.Empty(self.UserID)
            if self.another[0][0] == 1:
                self.LRLBox.set(self.searchresult[0][1])
                self.URLBox.set(self.searchresult[0][2])
                self.PulseAmplitudeBox.set(self.searchresult[0][3])
                self.PulseWidthBox.set(self.searchresult[0][4])
                self.MaxSensorRateBox.set(self.searchresult[0][5])
                self.SensitivityBox.set(self.searchresult[0][6])
                self.ARPBox.set(self.searchresult[0][7])
                self.PVARPBox.set(self.searchresult[0][8])
                self.ActivityThresholdBox.set(self.searchresult[0][9])
                self.ReactionTimeBox.set(self.searchresult[0][10])
                self.ResponseFactorBox.set(self.searchresult[0][11])
                self.RecoveryTimeBox.set(self.searchresult[0][12])
            else:
                self.AAIRdefaultSetting()

        elif self.currentmode == "VVIR":
            self.VVIRsetup(bg_color, fg_color)
            self.search = []
            self.searchresult = self.VVIR.Search(self.UserID)
            self.another = self.VVIR.Empty(self.UserID)
            if self.another[0][0] == 1:
                self.LRLBox.set(self.searchresult[0][1])
                self.URLBox.set(self.searchresult[0][2])
                self.PulseAmplitudeBox.set(self.searchresult[0][3])
                self.PulseWidthBox.set(self.searchresult[0][4])
                self.MaxSensorRateBox.set(self.searchresult[0][5])
                self.SensitivityBox.set(self.searchresult[0][6])
                self.VRPBox.set(self.searchresult[0][7])
                self.ActivityThresholdBox.set(self.searchresult[0][8])
                self.ReactionTimeBox.set(self.searchresult[0][9])
                self.ResponseFactorBox.set(self.searchresult[0][10])
                self.RecoveryTimeBox.set(self.searchresult[0][11])
            else:
                self.VVIRdefaultSetting()

    def on_closing(self):
        self.parameterwindow.destroy()
        self.loggedinpage.deiconify()

    #save the currently entered parameter and disable the comboboxes from editing again until clicking edit again
    def Save(self):

        if int(self.LRLBox.get()) > int(self.URLBox.get()):
            tkinter.messagebox.showerror("Input Error", "Lower rate limit higher than upper rate limit, please re-enter")
            self.LRLBox.set(60)
            self.URLBox.set(120)
        else:
            self.AAIdatabase = AAIParameterDatabase()
            self.VVIdatabase = VVIParameterDatabase()
            self.AOOdatabase = AOOParameterDatabase()
            self.VOOdatabase = VOOParameterDatabase()
            self.AOORdatabase = AOORParameterDatabase()
            self.VOORdatabase = VOORParameterDatabase()
            self.AAIRdatabase = AAIRParameterDatabase()
            self.VVIRdatabase = VVIRParameterDatabase()
            if self.currentmode == "AAI":
                if int(self.ARPBox.get()) > 60000/int(self.URLBox.get()):
                    tkinter.messagebox.showerror("Input Error",
                                                 "Atrial Refractory Period must be lower than the respective heart rate, please re-enter")
                    self.ARPBox.set(250)
                    self.URLBox.set(120)
                elif int(self.PVARPBox.get()) > 60000/int(self.URLBox.get()):
                    tkinter.messagebox.showerror("Input Error",
                                                 "PVARP must be lower than the respective heart rate, please re-enter")
                    self.PVARPBox.set(250)
                    self.URLBox.set(120)
                elif int(self.ARPBox.get()) <= 60000/int(self.URLBox.get()) and int(self.PVARPBox.get()) <= 60000/int(self.URLBox.get()):
                    self.ARPBox.config(state='disabled')
                    self.PVARPBox.config(state='disabled')
                    self.SensitivityBox.config(state='disabled')
                    self.LRLBox.config(state='disabled')
                    self.URLBox.config(state='disabled')
                    self.PulseAmplitudeBox.config(state='disabled')
                    self.PulseWidthBox.config(state='disabled')
                    #try to insert the parameters, if failed because of previously saved parameters, update them
                    try:
                        self.AAIdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.SensitivityBox.get(),
                                                self.ARPBox.get(),self.PVARPBox.get())
                    except sqlite3.IntegrityError:
                        self.AAIdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(),self.SensitivityBox.get(),
                                                self.ARPBox.get(),self.PVARPBox.get(), self.UserID)
                    tkinter.messagebox.showinfo("Saved", "Saved")


                    self.serial.update()
                    self.serial.send_param()
                    self.serial.get_echo()
                    print("after upate")
                    self.EditButton.config(state='active')
                    self.SaveButton.config(state='disabled')
            elif self.currentmode == "VVI":
                if int(self.VRPBox.get()) <= 60000/int(self.URLBox.get()):
                    self.VRPBox.config(state='disabled')
                    self.SensitivityBox.config(state='disabled')
                    self.LRLBox.config(state='disabled')
                    self.URLBox.config(state='disabled')
                    self.PulseAmplitudeBox.config(state='disabled')
                    self.PulseWidthBox.config(state='disabled')
                    try:
                        self.VVIdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.SensitivityBox.get(), self.VRPBox.get())
                    except sqlite3.IntegrityError:
                        self.VVIdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(),self.SensitivityBox.get(), self.VRPBox.get(),
                                                self.UserID)
                    tkinter.messagebox.showinfo("Saved", "Saved")
                    self.serial.update()
                    self.serial.send_param()
                    self.serial.get_echo()
                    self.EditButton.config(state='active')
                    self.SaveButton.config(state='disabled')
                else:
                    tkinter.messagebox.showerror("Input Error", "Ventricular Refractory Period must be lower than the respective heart rate, please re-enter")
                    self.VRPBox.set(250)
                    self.URLBox.set(120)
            elif self.currentmode == "AOO":
                self.LRLBox.config(state='disabled')
                self.URLBox.config(state='disabled')
                self.PulseAmplitudeBox.config(state='disabled')
                self.PulseWidthBox.config(state='disabled')
                try:
                    self.AOOdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                            self.PulseWidthBox.get())
                except sqlite3.IntegrityError:
                    self.AOOdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                            self.PulseWidthBox.get(),self.UserID)
                tkinter.messagebox.showinfo("Saved", "Saved")

                self.serial.update()
                print("after update")
                self.serial.send_param()
                print("after send")
                self.serial.get_echo()
                print("after echo")

                self.EditButton.config(state='active')
                self.SaveButton.config(state='disabled')
            elif self.currentmode == "VOO":
                self.LRLBox.config(state='disabled')
                self.URLBox.config(state='disabled')
                self.PulseAmplitudeBox.config(state='disabled')
                self.PulseWidthBox.config(state='disabled')
                try:
                    self.VOOdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                            self.PulseWidthBox.get())
                except sqlite3.IntegrityError:
                    self.VOOdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                            self.PulseWidthBox.get(),self.UserID)
                tkinter.messagebox.showinfo("Saved", "Saved")
                self.serial.update()
                self.serial.send_param()
                self.serial.get_echo()
                self.EditButton.config(state='active')
                self.SaveButton.config(state='disabled')
            elif self.currentmode == "AOOR":
                if int(self.URLBox.get()) < int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error",
                                                 "Upper Rate Limit must be higher or equal to Max Sensor Rate, please re-enter")
                    self.MaxSensorRateBox.set(120)
                    self.URLBox.set(120)
                else:
                    self.ActivityThresholdBox.config(state='disabled')
                    self.RecoveryTimeBox.config(state='disabled')
                    self.ReactionTimeBox.config(state='disabled')
                    self.ResponseFactorBox.config(state='disabled')
                    self.MaxSensorRateBox.config(state='disabled')
                    self.LRLBox.config(state='disabled')
                    self.URLBox.config(state='disabled')
                    self.PulseAmplitudeBox.config(state='disabled')
                    self.PulseWidthBox.config(state='disabled')
                    try:
                        self.AOORdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(),self.MaxSensorRateBox.get(), self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                self.ResponseFactorBox.get(), self.RecoveryTimeBox.get())
                    except sqlite3.IntegrityError:
                        self.AOORdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.MaxSensorRateBox.get(), self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                self.ResponseFactorBox.get(), self.RecoveryTimeBox.get(), self.UserID)
                    tkinter.messagebox.showinfo("Saved", "Saved")
                    self.serial.update()
                    self.serial.send_param()
                    self.serial.get_echo()
                    self.EditButton.config(state='active')
                    self.SaveButton.config(state='disabled')
            elif self.currentmode == "VOOR":
                if int(self.URLBox.get()) < int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error",
                                                 "Upper Rate Limit must be higher or equal to Max Sensor Rate, please re-enter")
                    self.MaxSensorRateBox.set(120)
                    self.URLBox.set(120)
                else:
                    self.ActivityThresholdBox.config(state='disabled')
                    self.RecoveryTimeBox.config(state='disabled')
                    self.ReactionTimeBox.config(state='disabled')
                    self.ResponseFactorBox.config(state='disabled')
                    self.MaxSensorRateBox.config(state='disabled')
                    self.LRLBox.config(state='disabled')
                    self.URLBox.config(state='disabled')
                    self.PulseAmplitudeBox.config(state='disabled')
                    self.PulseWidthBox.config(state='disabled')
                    try:
                        self.VOORdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.MaxSensorRateBox.get(), self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                self.ResponseFactorBox.get(), self.RecoveryTimeBox.get())
                    except sqlite3.IntegrityError:
                        self.VOORdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.MaxSensorRateBox.get(), self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                self.ResponseFactorBox.get(), self.RecoveryTimeBox.get(), self.UserID)
                    tkinter.messagebox.showinfo("Saved", "Saved")
                    self.serial.update()
                    self.serial.send_param()
                    self.serial.get_echo()
                    self.EditButton.config(state='active')
                    self.SaveButton.config(state='disabled')
            elif self.currentmode == "AAIR":
                if int(self.URLBox.get()) < int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error", "Upper Rate Limit must be higher or equal to Max Sensor Rate, please re-enter")
                    self.MaxSensorRateBox.set(120)
                    self.URLBox.set(120)
                elif int(self.ARPBox.get()) > 60000/int(self.MaxSensorRateBox.get()) and int(self.PVARPBox.get()) > 60000/int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error",
                                                 "Atrial Refractory Period and PVARP must be lower than the respective heart rate, please re-enter")
                    self.MaxSensorRateBox.set(120)
                    self.ARPBox.set(250)
                    self.PVARPBox.set(250)
                elif int(self.ARPBox.get()) > 60000/int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error",
                                                 "Atrial Refractory Period must be lower than the respective heart rate, please re-enter")
                    self.MaxSensorRateBox.set(120)
                    self.ARPBox.set(250)
                elif int(self.PVARPBox.get()) > 60000/int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error", "PVARP must be lower than the respective heart rate, please re-enter")
                    self.MaxSensorRateBox.set(120)
                    self.PVARPBox.set(250)
                else:
                    self.MaxSensorRateBox.config(state='disabled')
                    self.ARPBox.config(state='disabled')
                    self.PVARPBox.config(state='disabled')
                    self.SensitivityBox.config(state='disabled')
                    self.ActivityThresholdBox.config(state='disabled')
                    self.RecoveryTimeBox.config(state='disabled')
                    self.ReactionTimeBox.config(state='disabled')
                    self.ResponseFactorBox.config(state='disabled')
                    self.LRLBox.config(state='disabled')
                    self.URLBox.config(state='disabled')
                    self.PulseAmplitudeBox.config(state='disabled')
                    self.PulseWidthBox.config(state='disabled')
                    try:
                        self.AAIRdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.MaxSensorRateBox.get(), self.SensitivityBox.get(),
                                                self.ARPBox.get(), self.PVARPBox.get(),
                                                self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                 self.ResponseFactorBox.get(), self.RecoveryTimeBox.get())
                    except sqlite3.IntegrityError:
                        self.AAIRdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.MaxSensorRateBox.get(), self.SensitivityBox.get(),
                                                self.ARPBox.get(), self.PVARPBox.get(),
                                                self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                self.ResponseFactorBox.get(), self.RecoveryTimeBox.get(), self.UserID)
                    tkinter.messagebox.showinfo("Saved", "Saved")
                    self.serial.update()
                    self.serial.send_param()
                    self.serial.get_echo()
                    self.EditButton.config(state='active')
                    self.SaveButton.config(state='disabled')
            elif self.currentmode == "VVIR":
                if int(self.URLBox.get()) < int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error",
                                                 "Upper Rate Limit must be higher or equal to Max Sensor Rate, please reenter")
                    self.MaxSensorRateBox.set(120)
                    self.URLBox.set(120)
                elif int(self.VRPBox.get()) > 60000/int(self.MaxSensorRateBox.get()):
                    tkinter.messagebox.showerror("Input Error","Ventricular Refractory Period must be lower than the respective heart rate, please re-enter")
                    self.MaxSensorRateBox.set(120)
                    self.VRPBox.set(250)
                else:
                    self.VRPBox.config(state='disabled')
                    self.SensitivityBox.config(state='disabled')
                    self.ActivityThresholdBox.config(state='disabled')
                    self.RecoveryTimeBox.config(state='disabled')
                    self.ReactionTimeBox.config(state='disabled')
                    self.ResponseFactorBox.config(state='disabled')
                    self.MaxSensorRateBox.config(state='disabled')
                    self.LRLBox.config(state='disabled')
                    self.URLBox.config(state='disabled')
                    self.PulseAmplitudeBox.config(state='disabled')
                    self.PulseWidthBox.config(state='disabled')
                    try:
                        self.VVIRdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.MaxSensorRateBox.get(), self.SensitivityBox.get(), self.VRPBox.get(),
                                                self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                self.ResponseFactorBox.get(), self.RecoveryTimeBox.get())
                    except sqlite3.IntegrityError:
                        self.VVIRdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                                self.PulseWidthBox.get(), self.MaxSensorRateBox.get(), self.SensitivityBox.get(), self.VRPBox.get(),
                                                self.ActivityThresholdBox.get(), self.ReactionTimeBox.get(),
                                                self.ResponseFactorBox.get(), self.RecoveryTimeBox.get(), self.UserID)
                    tkinter.messagebox.showinfo("Saved", "Saved")
                    self.serial.update()
                    self.serial.send_param()
                    self.serial.get_echo()
                    self.EditButton.config(state='active')
                    self.SaveButton.config(state='disabled')


    def AOORVOORinputrep(self):
        self.LRLBox.set(self.searchresult[0][1])
        self.URLBox.set(self.searchresult[0][2])
        self.PulseAmplitudeBox.set(self.searchresult[0][3])
        self.PulseWidthBox.set(self.searchresult[0][4])
        self.MaxSensorRateBox.set(self.searchresult[0][5])
        self.ActivityThresholdBox.set(self.searchresult[0][6])
        self.ReactionTimeBox.set(self.searchresult[0][7])
        self.ResponseFactorBox.set(self.searchresult[0][8])
        self.RecoveryTimeBox.set(self.searchresult[0][9])
    def float_range(self, start, stop, step):
        while start < stop:
            yield float(start)
            start += decimal.Decimal(step)

    def round_up_to_nearest_5(self, num):
        return math.ceil(num / 5) * 5

    #make the comboxes editable again
    def modified(self, event):
        self.LRLinput = int(self.LRLBox.get())
        if self.LRLinput % 5 == 1:
            self.inputs = self.round_up_to_nearest_5(self.LRLinput)
        else:
            self.inputs = self.LRLinput

        self.URLtype = list(range(self.inputs, 180, 5))

    def Edit(self):
        tkinter.messagebox.showinfo("Edit Mode on", "Edit Mode on")
        self.EditButton.config(state='disabled')
        self.SaveButton.config(state='active')
        self.LRLBox.config(state='readonly')
        self.URLBox.config(state='readonly')
        self.PulseAmplitudeBox.config(state='readonly')
        self.PulseWidthBox.config(state='readonly')
        if self.currentmode == "AAI":
            self.SensitivityBox.config(state='readonly')
            self.ARPBox.config(state='readonly')
            self.PVARPBox.config(state='readonly')
        elif self.currentmode == "VVI":
            self.SensitivityBox.config(state='readonly')
            self.VRPBox.config(state='readonly')
        elif self.currentmode == "AOOR":
            self.MaxSensorRateBox.config(state='readonly')
            self.ActivityThresholdBox.config(state='readonly')
            self.RecoveryTimeBox.config(state='readonly')
            self.ReactionTimeBox.config(state='readonly')
            self.ResponseFactorBox.config(state='readonly')
        elif self.currentmode == "VOOR":
            self.MaxSensorRateBox.config(state='readonly')
            self.ActivityThresholdBox.config(state='readonly')
            self.RecoveryTimeBox.config(state='readonly')
            self.ReactionTimeBox.config(state='readonly')
            self.ResponseFactorBox.config(state='readonly')
        elif self.currentmode == "AAIR":
            self.MaxSensorRateBox.config(state='readonly')
            self.ActivityThresholdBox.config(state='readonly')
            self.RecoveryTimeBox.config(state='readonly')
            self.ReactionTimeBox.config(state='readonly')
            self.ResponseFactorBox.config(state='readonly')
            self.SensitivityBox.config(state='readonly')
            self.ARPBox.config(state='readonly')
            self.PVARPBox.config(state='readonly')
        elif self.currentmode == "VVIR":
            self.MaxSensorRateBox.config(state='readonly')
            self.ActivityThresholdBox.config(state='readonly')
            self.RecoveryTimeBox.config(state='readonly')
            self.ReactionTimeBox.config(state='readonly')
            self.ResponseFactorBox.config(state='readonly')
            self.SensitivityBox.config(state='readonly')
            self.VRPBox.config(state='readonly')

        #display the saved parameters in the database

    def Display(self):
        if self.currentmode == "AAI":
            self.database = AAIParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = AAIparametersDatabaseView(self.data)
        elif self.currentmode == "VVI":
            self.database = VVIParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = VVIparametersDatabaseView(self.data)
        elif self.currentmode == "AOO":
            self.database = AOOParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = AOOparametersDatabaseView(self.data)
        elif self.currentmode == "VOO":
            self.database = VOOParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = VOOparametersDatabaseView(self.data)
        elif self.currentmode == "AOOR":
            self.database = AOORParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = AOORparametersDatabaseView(self.data)
        elif self.currentmode == "VOOR":
            self.database = VOORParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = VOORparametersDatabaseView(self.data)
        elif self.currentmode == "AAIR":
            self.database = AAIRParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = AAIRparametersDatabaseView(self.data)
        elif self.currentmode == "VVIR":
            self.database = VVIRParameterDatabase()
            self.data = self.database.Display()
            self.displayWindow = VVIRparametersDatabaseView(self.data)

    #default setting if no previous saved paramters
    def AAIdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(120)
        self.PulseAmplitudeBox.set(5.0)
        self.PulseWidthBox.set(1)
        self.SensitivityBox.set(2.5)
        self.ARPBox.set(250)
        self.PVARPBox.set(250)

    def VVIdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(120)
        self.PulseAmplitudeBox.set(5.0)
        self.PulseWidthBox.set(1)
        self.SensitivityBox.set(2.5)
        self.VRPBox.set(320)

    def generalbuttonsetup(self, bg_color, fg_color, cha_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="LRL: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="URL: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=2)
        self.EditButton = tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Edit",
                       font=("times new roman", 15, "bold"), command=self.Edit)
        self.EditButton.grid(pady=15, column=1, row=15)
        self.SaveButton = tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Save",
                       font=("times new roman", 15, "bold"), command=self.Save)
        self.SaveButton.grid(pady=15, column=2, row=15)

        # For demonstration ONLY
        tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
                       text="Display (Demo Only)", font=("times new roman", 15, "bold"), command=self.Display).grid(pady=15, column=3, row=15)
        tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
                       text="Back",
                       font=("times new roman", 15, "bold"), command=self.Back).grid(pady=15, column=4, row=15)

    def Back(self):
        self.parameterwindow.destroy()
        self.loggedinpage.deiconify()
    def AAIRdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(120)
        self.MaxSensorRateBox.set(120)
        self.PulseAmplitudeBox.set(5.0)
        self.PulseWidthBox.set(1)
        self.SensitivityBox.set(2.5)
        self.ARPBox.set(250)
        self.PVARPBox.set(250)
        self.ActivityThresholdBox.set('Med')
        self.ReactionTimeBox.set(30)
        self.ResponseFactorBox.set(8)
        self.RecoveryTimeBox.set(5)

    def VVIRdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(120)
        self.MaxSensorRateBox.set(120)
        self.PulseAmplitudeBox.set(5.0)
        self.PulseWidthBox.set(1)
        self.SensitivityBox.set(2.5)
        self.VRPBox.set(320)
        self.ActivityThresholdBox.set('Med')
        self.ReactionTimeBox.set(30)
        self.ResponseFactorBox.set(8)
        self.RecoveryTimeBox.set(5)
    def AOOVOOdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(120)
        self.PulseAmplitudeBox.set(5.0)
        self.PulseWidthBox.set(1)

    def AOORVOORdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(120)
        self.PulseAmplitudeBox.set(5.0)
        self.PulseWidthBox.set(1)
        self.MaxSensorRateBox.set(120)
        self.ActivityThresholdBox.set('Med')
        self.ReactionTimeBox.set(30)
        self.ResponseFactorBox.set(8)
        self.RecoveryTimeBox.set(5)

    def AAIsetup(self, bg_color, fg_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Pulse Width: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Sensitivity: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="ARP: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=2)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="PVARP: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=3)

        # creates the right hand side of the page consisting of comboboxes
        self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
        self.LRLBox.bind('<<ComboboxSelected>>', self.modified)
        self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
        self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                      state='disabled')
        self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                  state='disabled')
        self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                   state='disabled')
        self.ARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')
        self.PVARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PVARPtype, width=20, state='disabled')

        # location of the comboboxes
        self.LRLBox.grid(pady=5, column=2, row=1)
        self.URLBox.grid(pady=5, column=2, row=2)
        self.PulseAmplitudeBox.grid(pady=5, column=2, row=3)
        self.PulseWidthBox.grid(pady=5, column=2, row=4)
        self.SensitivityBox.grid(pady=5, column=4, row=1)
        self.ARPBox.grid(pady=5, column=4, row=2)
        self.PVARPBox.grid(pady=5, column=4, row=3)

    def VVIsetup(self, bg_color, fg_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Pulse Width: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Sensitivity: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=2)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="VRP: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=3)

        self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
        self.LRLBox.bind('<<ComboboxSelected>>', self.modified)
        self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
        self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                      state='disabled')
        self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                  state='disabled')
        self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                   state='disabled')
        self.VRPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')

        self.LRLBox.grid(pady=5, column=2, row=1)
        self.URLBox.grid(pady=5, column=2, row=2)
        self.PulseAmplitudeBox.grid(pady=5, column=2, row=3)
        self.PulseWidthBox.grid(pady=5, column=4, row=1)
        self.SensitivityBox.grid(pady=5, column=4, row=2)
        self.VRPBox.grid(pady=5, column=4, row=3)

    def AOOsetup(self, bg_color, fg_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=2)

        self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
        self.LRLBox.bind('<<ComboboxSelected>>', self.modified)
        self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
        self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                      state='disabled')
        self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                  state='disabled')
        self.LRLBox.grid(pady=5, column=2, row=1)
        self.URLBox.grid(pady=5, column=2, row=2)
        self.PulseAmplitudeBox.grid(pady=5, column=4, row=1)
        self.PulseWidthBox.grid(pady=5, column=4, row=2)
    def VOOsetup(self, bg_color, fg_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Pulse Width: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=2)

        self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
        self.LRLBox.bind('<<ComboboxSelected>>', self.modified)
        self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
        self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                      state='disabled')
        self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                  state='disabled')
        self.LRLBox.grid(pady=5, column=2, row=1)
        self.URLBox.grid(pady=5, column=2, row=2)
        self.PulseAmplitudeBox.grid(pady=5, column=4, row=1)
        self.PulseWidthBox.grid(pady=5, column=4, row=2)
    def AOORsetup(self, bg_color, fg_color):
        self.AOORVOORRepsetup(bg_color, fg_color)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Pulse Width: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
    def VOORsetup(self, bg_color, fg_color):
        self.AOORVOORRepsetup(bg_color, fg_color)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Pulse Width: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
    def AAIRsetup(self, bg_color, fg_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Pulse Width: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Maximum Sensor Rate: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=5)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Atrial Sensitivity: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=6)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="ARP: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="PVARP: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=2)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Activity Threshold: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Reaction Time: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=4)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Response Factor: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=5)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Recovery Time: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=6)

        # creates the right hand side of the page consisting of comboboxes
        self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
        self.LRLBox.bind('<<ComboboxSelected>>', self.modified)
        self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
        self.MaxSensorRateBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.MaxSensorRate, width=20, state='disabled')
        self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                      state='disabled')
        self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                  state='disabled')
        self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                   state='disabled')
        self.ARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')
        self.PVARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PVARPtype, width=20, state='disabled')
        self.ActivityThresholdBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ActivityThreshold, width=20,
                                                         state='disabled')
        self.ReactionTimeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ReactionTime, width=20,
                                                    state='disabled')
        self.ResponseFactorBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ResponseFactor, width=20,
                                                      state='disabled')
        self.RecoveryTimeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RecoveryTime, width=20,
                                                    state='disabled')
        # location of the comboboxes
        self.LRLBox.grid(pady=5, column=2, row=1)
        self.URLBox.grid(pady=5, column=2, row=2)
        self.PulseAmplitudeBox.grid(pady=5, column=2, row=3)
        self.PulseWidthBox.grid(pady=5, column=2, row=4)
        self.MaxSensorRateBox.grid(pady=5, column=2, row=5)
        self.SensitivityBox.grid(pady=5, column=2, row=6)
        self.ARPBox.grid(pady=5, column=4, row=1)
        self.PVARPBox.grid(pady=5, column=4, row=2)
        self.ActivityThresholdBox.grid(pady=5, column=4, row=3)
        self.ReactionTimeBox.grid(pady=5, column=4, row=4)
        self.ResponseFactorBox.grid(pady=5, column=4, row=5)
        self.RecoveryTimeBox.grid(pady=5, column=4, row=6)
    def VVIRsetup(self, bg_color, fg_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Amplitude: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricular Pulse Width: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Maximum Sensor Rate: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=5)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Ventricularl Sensitivity: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=6)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="VRP: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Activity Threshold: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=2)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Reaction Time: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Response Factor: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=4)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Recovery Time: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=5)

        # creates the right hand side of the page consisting of comboboxes
        self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
        self.LRLBox.bind('<<ComboboxSelected>>', self.modified)
        self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
        self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                      state='disabled')
        self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                  state='disabled')
        self.MaxSensorRateBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.MaxSensorRate, width=20,
                                                     state='disabled')
        self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                   state='disabled')
        self.VRPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')
        self.ActivityThresholdBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ActivityThreshold, width=20,
                                                         state='disabled')
        self.ReactionTimeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ReactionTime, width=20,
                                                    state='disabled')
        self.ResponseFactorBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ResponseFactor, width=20,
                                                      state='disabled')
        self.RecoveryTimeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RecoveryTime, width=20,
                                                    state='disabled')
        # location of the comboboxes
        self.LRLBox.grid(pady=5, column=2, row=1)
        self.URLBox.grid(pady=5, column=2, row=2)
        self.PulseAmplitudeBox.grid(pady=5, column=2, row=3)
        self.PulseWidthBox.grid(pady=5, column=2, row=4)
        self.MaxSensorRateBox.grid(pady=5, column=2, row=5)
        self.SensitivityBox.grid(pady=5, column=2, row=6)
        self.VRPBox.grid(pady=5, column=4, row=1)
        self.ActivityThresholdBox.grid(pady=5, column=4, row=2)
        self.ReactionTimeBox.grid(pady=5, column=4, row=3)
        self.ResponseFactorBox.grid(pady=5, column=4, row=4)
        self.RecoveryTimeBox.grid(pady=5, column=4, row=5)
    def AOORVOORRepsetup(self, bg_color, fg_color):
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Maximum Sensor Rate: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=5)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Activity Threshold: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Reaction Time: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=2)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Response Factor: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=3)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="Recovery Time: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=3, row=4)

        self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
        self.LRLBox.bind('<<ComboboxSelected>>', self.modified)
        self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
        self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                      state='disabled')
        self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                  state='disabled')
        self.MaxSensorRateBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.MaxSensorRate, width=20,
                                                     state='disabled')
        self.ActivityThresholdBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ActivityThreshold, width=20,
                                                         state='disabled')
        self.ReactionTimeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ReactionTime, width=20,
                                                    state='disabled')
        self.ResponseFactorBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.ResponseFactor, width=20,
                                                      state='disabled')
        self.RecoveryTimeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RecoveryTime, width=20,
                                                    state='disabled')
        self.LRLBox.grid(pady=5, column=2, row=1)
        self.URLBox.grid(pady=5, column=2, row=2)
        self.PulseAmplitudeBox.grid(pady=5, column=2, row=3)
        self.PulseWidthBox.grid(pady=5, column=2, row=4)
        self.MaxSensorRateBox.grid(pady=5, column=2, row=5)
        self.ActivityThresholdBox.grid(pady=5, column=4, row=1)
        self.ReactionTimeBox.grid(pady=5, column=4, row=2)
        self.ResponseFactorBox.grid(pady=5, column=4, row=3)
        self.RecoveryTimeBox.grid(pady=5, column=4, row=4)


#opens and initializes the mode window
class ModeWindow:
    def __init__(self, userID, loggedinWindow):
        self.UserID = userID
        self.login = LoginDatabase()
        self.result = self.login.ReturnMode(self.UserID)
        #the current mode
        self.cmode = self.result[0][4]
        self.loggedin = loggedinWindow
        self.window = tkinter.Tk()
        self.window.wm_title("Pacemaker Modes")
        if 'normal' == self.window.state():
            self.loggedin.withdraw()
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        #the buttons on the page for the modes
        self.label1 = tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Current Mode: " + self.cmode,
                      font=("times new roman", 20, "bold"), width=30)
        self.label1.grid(pady=20, column=1, row=1)
        self.AOObutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="AOO",
                       font=("times new roman", 15, "bold"), command=self.AOO)
        self.AOObutton.grid(pady=15, column=1, row=2)
        self.VOObutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="VOO",
                       font=("times new roman", 15, "bold"), command=self.VOO)
        self.VOObutton.grid(pady=15, column=1, row=3)
        self.AAIbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="AAI",
                       font=("times new roman", 15, "bold"), command=self.AAI)
        self.AAIbutton.grid(pady=15, column=1, row=4)
        self.VVIbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="VVI",
                       font=("times new roman", 15, "bold"), command=self.VVI)
        self.VVIbutton.grid(pady=15, column=1, row=5)
        self.AOORbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
                                        text="AOOR",font=("times new roman", 15, "bold"), command=self.AOOR)
        self.AOORbutton.grid(pady=15, column=1, row=6)
        self.VOORbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
                                         text="VOOR", font=("times new roman", 15, "bold"), command=self.VOOR)
        self.VOORbutton.grid(pady=15, column=1, row=7)
        self.AAIRbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
                                         text="AAIR", font=("times new roman", 15, "bold"), command=self.AAIR)
        self.AAIRbutton.grid(pady=15, column=1, row=8)
        self.VVIRbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
                                         text="VVIR", font=("times new roman", 15, "bold"), command=self.VVIR)
        self.VVIRbutton.grid(pady=15, column=1, row=9)
        self.BackRbutton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
                                         text="Back", font=("times new roman", 15, "bold"), command=self.close)
        self.BackRbutton.grid(pady=15, column=1, row=10)

        self.CheckMode(self.cmode)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        self.window.destroy()
        self.loggedin.deiconify()

    def close(self):
        self.window.destroy()
        self.loggedin.deiconify()

    def CheckMode(self, currentmode):
        if currentmode == 'AOO':
            self.AOO()
        elif currentmode == 'VOO':
            self.VOO()
        elif currentmode == "AAI":
            self.AAI()
        elif currentmode == "VVI":
            self.VVI()
        elif currentmode == 'AOOR':
            self.AOOR()
        elif currentmode == 'VOOR':
            self.VOOR()
        elif currentmode == "AAIR":
            self.AAIR()
        elif currentmode == "VVIR":
            self.VVIR()
    #when mode is AOO
    def AOO(self):
        #updates the database for the new value of mode
        self.cmode = "AOO"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="disabled")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
        self.AOORbutton.config(state="active")
        self.VOORbutton.config(state="active")
        self.AAIRbutton.config(state="active")
        self.VVIRbutton.config(state="active")
    #when mode is VOO
    def VOO(self):
        # updates the database for the new value of mode
        self.cmode = "VOO"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="disabled")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
        self.AOORbutton.config(state="active")
        self.VOORbutton.config(state="active")
        self.AAIRbutton.config(state="active")
        self.VVIRbutton.config(state="active")
    #when mode is AAI
    def AAI(self):
        # updates the database for the new value of mode
        self.cmode = "AAI"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="disabled")
        self.VVIbutton.config(state="active")
        self.AOORbutton.config(state="active")
        self.VOORbutton.config(state="active")
        self.AAIRbutton.config(state="active")
        self.VVIRbutton.config(state="active")
    #when mdoe is VVI
    def VVI(self):
        # updates the database for the new value of mode
        self.cmode = "VVI"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="disabled")
        self.AOORbutton.config(state="active")
        self.VOORbutton.config(state="active")
        self.AAIRbutton.config(state="active")
        self.VVIRbutton.config(state="active")

    def AOOR(self):
        # updates the database for the new value of mode
        self.cmode = "AOOR"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
        self.AOORbutton.config(state="disabled")
        self.VOORbutton.config(state="active")
        self.AAIRbutton.config(state="active")
        self.VVIRbutton.config(state="active")

    def VOOR(self):
        # updates the database for the new value of mode
        self.cmode = "VOOR"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
        self.AOORbutton.config(state="active")
        self.VOORbutton.config(state="disabled")
        self.AAIRbutton.config(state="active")
        self.VVIRbutton.config(state="active")

    def AAIR(self):
        # updates the database for the new value of mode
        self.cmode = "AAIR"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
        self.AOORbutton.config(state="active")
        self.VOORbutton.config(state="active")
        self.AAIRbutton.config(state="disabled")
        self.VVIRbutton.config(state="active")

    def VVIR(self):
        # updates the database for the new value of mode
        self.cmode = "VVIR"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text="Current Mode: " + self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
        self.AOORbutton.config(state="active")
        self.VOORbutton.config(state="active")
        self.AAIRbutton.config(state="active")
        self.VVIRbutton.config(state="disabled")


class GraphWindow:
    def __init__(self, userID, loggedinwindow, Serial):
        self.UserID = userID
        self.login = LoginDatabase()
        # self.result = self.login.ReturnMode(self.UserID)
        # #the current mode
        # print(self.result)
        # self.cmode = self.result[0][4]
        # self.window = tkinter.Tk()
        # self.window.wm_title("Egram Graphs")
        self.loggedin = loggedinwindow
        # if 'normal' == self.window.state():
        #     self.loggedin.withdraw()
        #self.serial = pacemakerSerial(self.UserID)
        self.serial = Serial
        self.serial.get_echo()
        self.graph = animateGraph(self.serial, self.UserID, self.loggedin)
        self.graph.showPlot()
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        # create a figure

        # self.BackButton = tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color,
        #                                 text="Back",font=("times new roman", 15, "bold"), command=self.Back)
        # self.BackButton.grid(pady=15, column=1, row=2)
        #self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.window.mainloop()

    # def on_closing(self):
    #     self.window.destroy()
    #     self.loggedin.deiconify()

    # def Back(self):
    #     self.window.destroy()
    #     self.loggedin.deiconify()



#opens and initializes the home page
class HomePage:
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("Pacemaker Home Page")
        self.login = LoginDatabase()
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        #all the available userIDs
        self.UserIDALL = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
        #the buttons
        tkinter.Label(self.homePageWindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Home Page",
                      font=("times new roman",20,"bold"), width=30).grid(pady=20, column=1, row=1)
        self.registerbutton = tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Register",
                       font=("times new roman",15,"bold"), command=self.Register)
        self.registerbutton.grid(pady=15, column=1, row=2)
        self.loginbutton = tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Login",
                       font=("times new roman",15,"bold"), command=self.Login)
        self.loginbutton.grid(pady=15, column=1, row=3)

        #FOR DEMONSTRATION ONLY
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Display (demo only)",
                       font=("times new roman",15,"bold"), command=self.Display).grid(pady=15, column=1,row=4)
        tkinter.Button(self.homePageWindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Exit",
                       font=("times new roman",15,"bold"), command=self.homePageWindow.destroy).grid(pady=15,column=1,row=5)
        self.homePageWindow.mainloop()
    #checks for the current userID and if the user limit is not met, will be directed to the registration page
    def Register(self):
        self.num = self.login.Check()[0]
        self.userID = self.UserIDALL[self.num]
        if self.num < 10:
            self.registerWindow = RegisterationWindow(self.userID, self.homePageWindow)
        else:
            tkinter.messagebox.showerror("Registeration Full", "Registeration full, please log in")

    #directs to the login page
    def Login(self):
        self.loginWindow = LoginWindow(self.homePageWindow)

    # FOR DEMONSTRATION ONLY
    def Display(self):
        self.database = LoginDatabase()
        self.data = self.database.Display()
        self.displayWindow = LoginDatabaseView(self.data)


homepage = HomePage()
