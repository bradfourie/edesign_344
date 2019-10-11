from tkinter import Tk, ttk, mainloop, Frame, Text, END
from connection import ConnectionStatus, BeetleConnection
from tkinter import *
import tkinter.messagebox
import tkinter as tk
from time import sleep

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class App(tk.Tk):
    connectframe = -1
    diagnosticframe = -1
    container_global = -1
    voltage_measurements = []
    current_measurements = []
    phase_measurements = []
    trip_status = -1
	
    def __init__(self, *args, **kwargs):    
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.grid(row=0, column = 0, sticky='nsew')

        self.__create_connection()
        self.container_global = container
		
        self.title("Smart Power Meter")
        self.call('wm', 'iconphoto', self.winfo_toplevel()._w, tk.PhotoImage(file='baseline_power_black_24dp.png'))
        
        self.geometry("655x660")
        self.resizable(False, False)

        self.connectframe= ConnectionFrame(container, self)
        self.connectframe.grid(row=1, column = 0, sticky='NEWS')	
		
        self.after(1000, self.sample_data)#self.printSerialReturn())
		
    def sample_data(self):
        if self.connection.is_connected():
           self.parse_input()
        self.after(1000, self.sample_data)#self.printSerialReturn())
		
    def parse_input(self):
        sleep(0.02)
        print(self.connection.receive() )

		
    def show_connection_frame(self):
        if self.diagnosticframe != -1:
            self.remove_grid_diagnostic_frame()
			
        self.setup_grid_connection_frame()
        self.connectframe.tkraise()	
		
    def show_diagnostic_frame(self):
        self.remove_grid_connection_frame()	
		
        if self.diagnosticframe == -1:
            self.diagnosticframe= DiagnosticFrame(self.container_global, self)
            self.diagnosticframe.grid(row=2, column = 0, sticky='nsew')		
            self.diagnosticframe.tkraise()
        else:
            self.setup_grid_diagnostic_frame()
            self.diagnosticframe.tkraise()	

    def setup_grid_connection_frame(self):
        self.config(menu=self.connectframe.menubar)
        self.connectframe.statusbar.grid(column=0, row=7, padx=5, pady=5, sticky="WES", columnspan=4)
        self.connectframe.page_title_label.grid(column=0, row=0, padx=100, pady=5, columnspan=4)			
        self.connectframe.device_picker.grid(column=2, row=1, padx=5, pady=5,  sticky="WE", columnspan=2)		
        self.connectframe.device_label.grid(column=0, row=1, padx=5, pady=5, sticky="W", columnspan=2)
        self.connectframe.connect_button.grid(column=0, row=2,padx=5, pady=5, sticky="WE", columnspan=4)
        self.connectframe.type_label.grid(column=0, row=3,padx=5, pady=5, sticky="W")	
        self.connectframe.type_entry.grid(column=1, row=3,padx=5, pady=5, sticky="E", columnspan=1)
        self.connectframe.port_label.grid(column=2, row=3,padx=5, pady=5, sticky="W")
        self.connectframe.port_entry.grid(column=3, row=3,padx=5, pady=5, sticky="E", columnspan=1)	
        self.connectframe.request_button.grid(column=0, row=4,padx=5, pady=5, sticky="WE", columnspan=4)
        self.connectframe.clear_button.grid(column=0, row=6,padx=5, pady=5, sticky="WE", columnspan=2)
        self.connectframe.Uptime_button.grid(column=2, row=6, padx=5, pady=5, sticky="WE", columnspan=2)
        self.connectframe.return_text.grid(column=0, row=5, padx=5, pady=5, sticky="WE", columnspan=4)	
		
    def remove_grid_connection_frame(self):
        self.connectframe.menubar.grid_forget()	
        self.connectframe.statusbar.grid_forget()
        self.connectframe.page_title_label.grid_forget()	
        self.connectframe.device_picker.grid_forget()		
        self.connectframe.device_label.grid_forget()
        self.connectframe.connect_button.grid_forget()
        self.connectframe.type_label.grid_forget()		
        self.connectframe.type_entry.grid_forget()	
        self.connectframe.port_label.grid_forget()
        self.connectframe.port_entry.grid_forget()		
        self.connectframe.request_button.grid_forget()
        self.connectframe.clear_button.grid_forget()
        self.connectframe.Uptime_button.grid_forget()
        self.connectframe.return_text.grid_forget()	 

    def setup_grid_diagnostic_frame(self):
        self.config(menu=self.diagnosticframe.menubar)
        self.diagnosticframe.page_title_label.grid(column=0, row=0, padx=230, pady=5,sticky="NSEW", columnspan=4)
        self.diagnosticframe.voltage_canvas.get_tk_widget().grid(column=0, row=1, padx=10, pady=0,sticky="WE", columnspan=4, rowspan=3)
        self.diagnosticframe.current_canvas.get_tk_widget().grid(column=0, row=4, padx=10, pady=0,sticky="WE", columnspan=4, rowspan=3)
        self.diagnosticframe.phase_canvas.get_tk_widget().grid(column=0, row=7, padx=10, pady=0,sticky="WE", columnspan=4, rowspan=3)
        self.diagnosticframe.statusbar.grid(column=0, row=13, padx=5, pady=0, sticky="WES", columnspan=4)
        self.diagnosticframe.reset_button.grid(column=0, row=12, padx=5, pady=5, sticky="WES", columnspan=4)	
		
    def remove_grid_diagnostic_frame(self):
        self.diagnosticframe.page_title_label.grid_forget()
        self.diagnosticframe.menubar.grid_forget()
        self.diagnosticframe.voltage_canvas.get_tk_widget().grid_forget()
        self.diagnosticframe.current_canvas.get_tk_widget().grid_forget()			
        self.diagnosticframe.phase_canvas.get_tk_widget().grid_forget()
        self.diagnosticframe.statusbar.grid_forget()
        self.diagnosticframe.reset_button.grid_forget() 				

    def __create_connection(self):
        self.connection = BeetleConnection()

        def connection_callback(state):
            if state == ConnectionStatus.DISCONNECTED:
                self.connectframe.event_disconnected(self)
            elif state == ConnectionStatus.CONNECTED:
                self.connectframe.event_connected(self)
            elif state == ConnectionStatus.FAILED_TO_CONNECT:
                self.connectframe.event_failed_to_connect(self)
            elif state == ConnectionStatus.DISCONNECTED_TIMEOUT:
                self.connectframe.event_disconnected_timeout(self)
            elif state == ConnectionStatus.DISCONNECTED_ERROR:
                self.connectframe.event_disconnected_error(self)
            else:
                raise Exception("Unhandled connection callback")

        self.connection.register_status_callback(connection_callback)
			
class ConnectionFrame(Frame):
    def __set_connected_button(self, controller):
        def connect_button_callback():
            controller.connection.disconnect()

        controller.connection.write(b"U")
        controller.connection.write(b"\n")

        self.connect_button["command"] = connect_button_callback
        self.connect_button["text"] = "Disconnect"
        self.device_picker["state"] = "disabled"

    def __set_disconnected_button(self, controller):
        def connect_button_callback():
            device = self.device_picker.get()
            controller.connection.connect(device)

        self.connect_button["command"] = connect_button_callback
        self.connect_button["text"] = "Connect"

        self.device_picker["state"] = "normal"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
		
        self.controller = controller
		#code for adding a submenu to swap frames
		#code for main connection frame)
		#create the menubar
        self.menubar = Menu(controller)
        controller.config(menu=self.menubar)	
	    #create the submenu
        self.subMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="Navigation",menu=self.subMenu)
        self.subMenu.add_command(label="Connection")
        self.subMenu.add_command(label="Diagnostic", command=lambda: controller.show_diagnostic_frame())
        self.subMenu.add_command(label="Exit", command= self.winfo_toplevel().destroy)
		
        def about_project():
            tkinter.messagebox.showinfo('About Project', 'This application is a connection and diagnostics viewer and was made by Bradley Fourie for the EDesign344 course at Stellenboch University.')
	
        self.subMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="Help",menu=self.subMenu)
        self.subMenu.add_command(label="About", command= about_project)
		
		#create the statusbar
        self.statusbar = Label(self.winfo_toplevel(), text="Connection Status: Disconnected", relief=SUNKEN)
        self.statusbar.grid(column=0, row=7, padx=5, pady=5, sticky="WES", columnspan=4)
		
		#create the page title
        self.page_title_label = ttk.Label(self.winfo_toplevel(), text="Connections Manager")
        self.page_title_label.grid(column=0, row=0, padx=100, pady=5, columnspan=4)		
        self.page_title_label.config(font=("Calibri", 18))	
   
		#create the device picker
		#row1
        self.device_picker = ttk.Combobox(self.winfo_toplevel(), values=())
        self.device_picker.grid(column=2, row=1, padx=5, pady=5,  sticky="WE", columnspan=2)
		#row2
        self.device_label = ttk.Label(self.winfo_toplevel(), text="Device : ")
        self.device_label.grid(column=0, row=1, padx=5, pady=5, sticky="W", columnspan=2)	
		
        self.connect_button = ttk.Button(self.winfo_toplevel(), text="Connect")
        self.connect_button.grid(column=0, row=2,padx=5, pady=5, sticky="WE", columnspan=4)
		#row3
        self.type_label = ttk.Label(self.winfo_toplevel(), text="Type : ")
        self.type_label.grid(column=0, row=3,padx=5, pady=5, sticky="W")

        self.type_entry = ttk.Entry(self.winfo_toplevel())
        self.type_entry.grid(column=1, row=3,padx=5, pady=5, sticky="E", columnspan=1)

        self.port_label = ttk.Label(self.winfo_toplevel(), text="Port : ")
        self.port_label.grid(column=2, row=3,padx=5, pady=5, sticky="W")

        self.port_entry = ttk.Entry(self.winfo_toplevel())
        self.port_entry.grid(column=3, row=3,padx=5, pady=5, sticky="E", columnspan=1)
		#row4
        self.request_button = ttk.Button(self.winfo_toplevel(),text="Send Request")
        self.request_button.grid(column=0, row=4,padx=5, pady=5, sticky="WE", columnspan=4)
		#row 5
		#see below 
		
		#row6
        self.clear_button = ttk.Button(self.winfo_toplevel(), text="Clear")
        self.clear_button.grid(column=0, row=6,padx=5, pady=5, sticky="WE", columnspan=2)		
		
        self.Uptime_button = ttk.Button(self.winfo_toplevel(), text="Uptime")
        self.Uptime_button.grid(column=2, row=6, padx=5, pady=5, sticky="WE", columnspan=2)
		
        self.return_text = Text(self.winfo_toplevel())
        self.return_text.config(state='disabled')
        self.return_text.grid(column=0, row=5, padx=5, pady=5, sticky="WE", columnspan=4)
        self.return_text.see("end")
        self.clear(controller)

        self.DEBUGMODE = False
        self.after(2000, self.refresh_debug)#self.printSerialReturn())
		
        def uptime_callback():
            self.UptimeReturn(controller)	
        def send_request_callback():
            self.SendRequest(controller)
        def clear_button_callback():
            self.clear(controller)

        self.clear_button["command"] = clear_button_callback
        self.request_button["command"] = send_request_callback		
        self.Uptime_button["command"] = uptime_callback
		
		
    def refresh_debug(self):
        if self.DEBUGMODE == True and self.controller.connection.is_connected():
            self.printSerialReturn(self.controller)
        self.after(2000, self.refresh_debug)#self.printSerialReturn())

    def event_connected(self, controller):
        self.statusbar["text"] = "Connection Status: Connected"

        self.__set_connected_button(controller)

    def event_disconnected(self, controller):
        self.statusbar["text"] = "Connection Status: Disconnected"

        self.__set_disconnected_button(controller)

    def event_disconnected_timeout(self, controller):
        self.statusbar["text"] = "Connection Status: Disconnected (Timeout)"

        self.__set_disconnected_button(controller)

    def event_disconnected_error(self, controller):
        self.statusbar["text"] = "Connection Status: Disconnected (Error)"

        self.__set_disconnected_button(controller)

    def event_failed_to_connect(self, controller):
        self.statusbar["text"] = "Connection Status: Disconnected (Failed to connect)"

        self.__set_disconnected_button(controller)

    def SendRequest(self, controller):
        CommandType = self.type_entry.get()  #String is saved in Command
        CommandPort = self.port_entry.get()

        if not controller.connection.is_connected():
            txt = "Cannot write when not connected"
            self.return_text.config(state='normal')
            self.return_text.insert(END,txt+"\n")
            self.return_text.config(state='disabled')
            self.return_text.see("end")
            return

        # Entry validation:
        if CommandType not in ['0','1','2','X','x', 'U', 'u']:
            txt = "Please enter valid type (0,1,2,X,U)"
            self.return_text.config(state='normal')
            self.return_text.insert(END,txt+"\n")
            self.return_text.config(state='disabled')
            self.return_text.see("end")
            return

        if CommandType == '1':
            if CommandPort not in ['0','1','2']:
                txt = "Please enter valid analogue port number (0,1,2)"
                self.return_text.config(state='normal')
                self.return_text.insert(END,txt+"\n")
                self.return_text.config(state='disabled')
                self.return_text.see("end")
                return

        elif CommandType == '2':
            if CommandPort not in ['0','1','2']:
                txt = "Please enter valid digital port number (0,1,2)"
                self.return_text.config(state='normal')
                self.return_text.insert(END,txt+"\n")
                self.return_text.config(state='disabled')
                self.return_text.see("end")
                return


        elif CommandType in ['x','X']:
            if CommandPort not in ['0','1']:
                txt = "Please enter 0 (debug off) or 1 (debug on) in port field"
                self.return_text.config(state='normal')
                self.return_text.insert(END,txt+"\n")
                self.return_text.config(state='disabled')
                self.return_text.see("end")
                return
            else:
                if CommandPort == '1':
                    self.DEBUGMODE = True
                    self.return_text.config(state='normal')
                    self.return_text.insert(END,'Debug-Mode On'+"\n")
                    self.return_text.config(state='disabled')
                    self.return_text.see("end")
 
                    controller.connection.write(CommandType.encode('utf-8'))
                    controller.connection.write(CommandPort.encode('utf-8'))
                else:
                    self.DEBUGMODE = False
                    self.type_entry.config(state='normal')

                    self.return_text.config(state='normal')
                    self.return_text.insert(END,'Debug-Mode Off'+"\n")
                    self.return_text.config(state='disabled')
                    self.return_text.see("end")

                    controller.connection.write(CommandType.encode('utf-8'))
                    controller.connection.write(CommandPort.encode('utf-8'))
					 
        controller.connection.write(CommandType.encode('utf-8'))
        controller.connection.write(CommandPort.encode('utf-8'))
        controller.connection.write(b"\n")
        self.printSerialReturn(controller)

    def printSerialReturn(self, controller):
        sleep(0.02)
        OutputText = self.CleanList(controller.connection.receive())

        if OutputText != '[]':
            self.return_text.config(state='normal')
            self.return_text.insert(END,OutputText+"\n")
            self.return_text.config(state='disabled')
            self.return_text.see("end")

    def CleanList(self,InputList):
        OutputString = "["
        for returnstring in range(0,len(InputList)):
            if (returnstring != (len(InputList) - 1)):
                OutputString += str(InputList[returnstring][:-1]) + ', '
            else:
                OutputString += str(InputList[returnstring][:-1])

        OutputString += "]"
        return OutputString

    def UptimeReturn(self, controller):
        if controller.connection.is_connected():
            controller.connection.write(b"U")
            controller.connection.write(b"\n")
            self.printSerialReturn(controller)
        else:
            txt = "No device has been connected"
            self.return_text.config(state='normal')
            self.return_text.insert(END,txt+"\n")
            self.return_text.config(state='disabled')
            self.return_text.see("end")

    def clear(self, controller):
        if controller.connection.is_connected():
            self.return_text.config(state='normal')
            self.return_text.delete(1.0,END)
            self.return_text.config(state='disabled')
            #self.type_entry.delete(0,'end')
            #self.port_entry.delete(0,'end')
            #self.type_entry.config(state='normal')
            #self.port_entry.config(state='normal')
            #self.request_button.config(state='normal')
        else:
            self.return_text.config(state='normal')
            self.return_text.delete(1.0,END)
            self.return_text.config(state='disabled')
            #self.type_entry.delete(0,'end')
            #self.port_entry.delete(0,'end')
            #self.type_entry.config(state='normal')
            #self.port_entry.config(state='normal')
            #self.request_button.config(state='normal')

            self.device_list = BeetleConnection.possible_connections()

            possible_values = [
                x.device for x in self.device_list if "Arduino" in str(x)
            ]
            self.device_picker["values"] = possible_values
            if len(possible_values) > 0:
                self.device_picker.current(0)
            self.event_disconnected(controller)
   
class DiagnosticFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
		
		#code for adding a submenu to swap frames
		#code for main connection frame)
		#create the menubar
        self.menubar = Menu(controller)
        controller.config(menu=self.menubar)	
	    #create the submenu
        self.subMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="Navigation",menu=self.subMenu)
        self.subMenu.add_command(label="Connection", command=lambda: controller.show_connection_frame())
        self.subMenu.add_command(label="Diagnostic")
        self.subMenu.add_command(label="Exit", command= self.winfo_toplevel().destroy)
		
        def about_project():
            tkinter.messagebox.showinfo('About Project', 'This application is a connection and diagnostics viewer and was made by Bradley Fourie for the EDesign344 course at Stellenboch University.')
	
        self.subMenu = Menu(self.menubar)
        self.menubar.add_cascade(label="Help",menu=self.subMenu)
        self.subMenu.add_command(label="About", command= about_project)
		
		#create the page title
        self.page_title_label = ttk.Label(self.winfo_toplevel(), text="System Diagnostics")
        self.page_title_label.grid(column=0, row=0, padx=230, pady=5,sticky="NSEW", columnspan=4)		
        self.page_title_label.config(font=("Calibri", 18))	
		
		#graph for the voltage transducer
        self.figure_voltage = Figure(figsize=(6, 2.3), dpi=80)
        voltage_graph = self.figure_voltage.add_subplot(1, 1, 1)
        voltage_graph.set_title('Voltage Transducer Measurement')
		
        voltage_graph.plot(0.5, 0.3, color="red", marker="o", linestyle="")

        x = [ 0.1, 0.2, 0.3 ]
        y = [ -0.1, -0.2, -0.3 ]
        voltage_graph.plot(x, y, color="blue", marker="x", linestyle="")
    
        self.voltage_canvas = FigureCanvasTkAgg(self.figure_voltage, controller)
        self.voltage_canvas.get_tk_widget().grid(column=0, row=1, padx=10, pady=0,sticky="WE", columnspan=4, rowspan=3)
		
		#graph for the current transducer
        self.figure_current = Figure(figsize=(6, 2.3), dpi=80)
        current_graph = self.figure_current.add_subplot(1, 1, 1)
        current_graph.set_title('Current Transducer Measurement')

        current_graph.plot(0.5, 0.3, color="red", marker="o", linestyle="")

        x = [ 0.1, 0.2, 0.3 ]
        y = [ -0.1, -0.2, -0.3 ]
        current_graph.plot(x, y, color="blue", marker="x", linestyle="")

        self.current_canvas = FigureCanvasTkAgg(self.figure_current, controller)
        self.current_canvas.get_tk_widget().grid(column=0, row=4, padx=10, pady=0,sticky="WE", columnspan=4, rowspan=3)

		#graph for the phase transducer
        self.figure_phase = Figure(figsize=(6, 2.3), dpi=80)
        phase_graph = self.figure_phase.add_subplot(1, 1, 1)
        phase_graph.set_title('Phase Transducer Measurement')

        phase_graph.plot(0.5, 0.3, color="red", marker="o", linestyle="")

        x = [ 0.1, 0.2, 0.3 ]
        y = [ -0.1, -0.2, -0.3 ]	
        phase_graph.plot(x, y, color="blue", marker="x", linestyle="")

        self.phase_canvas = FigureCanvasTkAgg(self.figure_phase, controller)
        self.phase_canvas.get_tk_widget().grid(column=0, row=7, padx=10, pady=0,sticky="WE", columnspan=4, rowspan=3)
		
		#create the statusbar
        self.statusbar = Label(self.winfo_toplevel(), text="Trip Status: Not Tripped", relief=SUNKEN)
        self.statusbar.grid(column=0, row=13, padx=5, pady=5, sticky="WES", columnspan=4)

        self.reset_button = ttk.Button(self.winfo_toplevel(), text="Reset Trip Switch")
        self.reset_button.grid(column=0, row=12, padx=5, pady=5, sticky="WES", columnspan=4)
	
class Main:
    def __init__(self):
        app = App()
        app.mainloop()

Main()
