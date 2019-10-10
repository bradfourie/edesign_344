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
	
    def __init__(self, *args, **kwargs):    
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.grid(row=0, column = 0, sticky='nsew')
		
        self.container_global = container
        	
        self.geometry("655x660")
        self.resizable(False, False)
		
        #for F in (StartFrame, ConnectionFrame, DiagnosticFrame):
        #    frame = F(container, self)
        #    self.frames[F] = frame
        #    frame.grid(row=0, column = 0, sticky='nsew')
        container.frame1= ConnectionFrame(container, self)
        container.frame1.grid(row=1, column = 0, sticky='nsew')	
		
        #container.frame1.page_title_label.grid_forget()	
        #container.frame1.page_title_label.grid_forget()
		
        self.connectframe = container.frame1
		
        #container.frame2= DiagnosticFrame(container, self)
        #container.frame2.grid(row=2, column = 0, sticky='nsew')	
        #container.frame2.grid_forget()

        #self.show_frame(DiagnosticFrame)	
        #self.show_connection_frame()		
		
    def show_connection_frame(self):
        if self.diagnosticframe != -1:
            self.diagnosticframe.page_title_label.grid_forget()
            self.diagnosticframe.menubar.grid_forget()		
        
        self.config(menu=self.connectframe.menubar)
        self.connectframe.statusbar.grid(column=0, row=7, padx=5, pady=5, sticky="WE", columnspan=4)
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
		
        self.connectframe.tkraise()		
		
    #    print(cont)
		
        #frame = self.frames[cont]	)	

   # def create_start_frame(self, container):
    #    self.frame1 = StartFrame(container, self)	
     #   self.frame1.grid(row=0, column = 0, sticky='nsew')	

    def show_diagnostic_frame(self):
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
		
        if self.diagnosticframe == -1:
            self.diagnosticframe= DiagnosticFrame(self.container_global, self)
            self.diagnosticframe.grid(row=2, column = 0, sticky='nsew')		
            self.diagnosticframe.tkraise()
        else:
            self.config(menu=self.diagnosticframe.menubar)
            self.diagnosticframe.page_title_label.grid(column=0, row=0, padx=100, pady=5,sticky="NSEW", columnspan=4)
            self.diagnosticframe.tkraise()		
    #    print(cont)
		
        #frame = self.frames[cont]	
		
			
class ConnectionFrame(Frame):
    def __create_connection(self):
        self.connection = BeetleConnection()

        def connection_callback(state):
            if state == ConnectionStatus.DISCONNECTED:
                self.event_disconnected()
            elif state == ConnectionStatus.CONNECTED:
                self.event_connected()
            elif state == ConnectionStatus.FAILED_TO_CONNECT:
                self.event_failed_to_connect()
            elif state == ConnectionStatus.DISCONNECTED_TIMEOUT:
                self.event_disconnected_timeout()
            elif state == ConnectionStatus.DISCONNECTED_ERROR:
                self.event_disconnected_error()
            else:
                raise Exception("Unhandled connection callback")

        self.connection.register_status_callback(connection_callback)

    def __set_connected_button(self):
        def connect_button_callback():
            self.connection.disconnect()

        self.connection.write(b"U")
        self.connection.write(b"\n")

        self.connect_button["command"] = connect_button_callback
        self.connect_button["text"] = "Disconnect"
        self.device_picker["state"] = "disabled"

    def __set_disconnected_button(self):
        def connect_button_callback():
            device = self.device_picker.get()
            self.connection.connect(device)

        self.connect_button["command"] = connect_button_callback
        self.connect_button["text"] = "Connect"

        self.device_picker["state"] = "normal"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
		
        self.__create_connection()
		
		#Code for setting the app name and icon
        controller.title("Smart Power Meter")
        controller.call('wm', 'iconphoto', self.winfo_toplevel()._w, tk.PhotoImage(file='baseline_power_black_24dp.png'))
		#
		
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
        self.statusbar.grid(column=0, row=7, padx=5, pady=5, sticky="WE", columnspan=4)
		
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
        self.request_button = ttk.Button(self.winfo_toplevel(),command = self.SendRequest, text="Send Request")
        self.request_button.grid(column=0, row=4,padx=5, pady=5, sticky="WE", columnspan=4)
		#row 5
		#see below 
		
		#row6
        self.clear_button = ttk.Button(self.winfo_toplevel(), text="Clear")
        self.clear_button.grid(column=0, row=6,padx=5, pady=5, sticky="WE", columnspan=2)		
		
        self.Uptime_button = ttk.Button(self.winfo_toplevel(), command = self.UptimeReturn, text="Uptime")
        self.Uptime_button.grid(column=2, row=6, padx=5, pady=5, sticky="WE", columnspan=2)
		
        self.return_text = Text(self.winfo_toplevel())
        self.return_text.config(state='disabled')
        self.return_text.grid(column=0, row=5, padx=5, pady=5, sticky="WE", columnspan=4)
        self.return_text.see("end")
        self.clear()

        self.DEBUGMODE = False
        self.after(2000, self.refresh_debug)#self.printSerialReturn())

        def clear_button_callback():
            self.clear()

        self.clear_button["command"] = clear_button_callback
		

    def refresh_debug(self):

        if self.DEBUGMODE == True and self.connection.is_connected():
            self.printSerialReturn()
        self.after(2000, self.refresh_debug)#self.printSerialReturn())

    def event_connected(self):
        self.statusbar["text"] = "Connection Status: Connected"

        self.__set_connected_button()

    def event_disconnected(self):
        self.statusbar["text"] = "Connection Status: Disconnected"

        self.__set_disconnected_button()

    def event_disconnected_timeout(self):
        self.statusbar["text"] = "Connection Status: Disconnected (Timeout)"

        self.__set_disconnected_button()

    def event_disconnected_error(self):
        self.statusbar["text"] = "Connection Status: Disconnected (Error)"

        self.__set_disconnected_button()

    def event_failed_to_connect(self):
        self.statusbar["text"] = "Connection Status: Disconnected (Failed to connect)"

        self.__set_disconnected_button()

    def SendRequest(self):
        CommandType = self.type_entry.get()  #String is saved in Command
        CommandPort = self.port_entry.get()

        if not self.connection.is_connected():
            self.connection_status_label["text"] = "Cannot write when not connected"
            return

        # Entry validation:
        if CommandType not in ['0','1','2','X','x']:
            txt = "Please enter valid type (0,1,2,X)"
            self.connection_status_label["text"] = txt
            return

        else:
            self.connection_status_label["text"] = ''

        if CommandType == '1':
            if CommandPort not in ['0','1','2']:
                txt = "Please enter valid analogue port number (0,1,2)"
                self.connection_status_label["text"] = txt
                return

        elif CommandType == '2':
            if CommandPort not in ['0','1','2']:
                txt = "Please enter valid digital port number (0,1,2)"
                self.connection_status_label["text"] = txt
                return


        elif CommandType in ['x','X']:
            if CommandPort not in ['0','1']:
                txt = "Please enter 0 (debug off) or 1 (debug on) in port field"
                self.connection_status_label["text"] = txt
                return
            else:
                if CommandPort == '1':
                    self.DEBUGMODE = True
                    self.return_text.config(state='normal')
                    self.return_text.insert(END,"\n"+'Debug-Mode On')
                    self.return_text.config(state='disabled')
                    self.return_text.see("end")

                    self.connection.write(CommandType.encode('utf-8'))
                    self.connection.write(CommandPort.encode('utf-8'))
                else:
                    self.DEBUGMODE = False
                    self.type_entry.config(state='normal')

                    self.return_text.config(state='normal')
                    self.return_text.insert(END,"\n"+'Debug-Mode Off')
                    self.return_text.config(state='disabled')
                    self.return_text.see("end")

                    self.connection.write(CommandType.encode('utf-8'))
                    self.connection.write(CommandPort.encode('utf-8'))
        else:
            self.connection_status_label["text"] = ''

        self.connection.write(CommandType.encode('utf-8'))
        self.connection.write(CommandPort.encode('utf-8'))
        self.connection.write(b"\n")
        self.printSerialReturn()

    def printSerialReturn(self):
        sleep(0.02)
        OutputText = self.CleanList(self.connection.receive())

        if OutputText != '[]':
            self.return_text.config(state='normal')
            self.return_text.insert(END,"\n"+OutputText)
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

    def UptimeReturn(self):
        if self.connection.is_connected():
            self.connection.write(b"U")
            self.connection.write(b"\n")
            self.printSerialReturn()

    def clear(self):

        if self.connection.is_connected():

            self.return_text.config(state='normal')
            self.return_text.delete(1.0,END)
            self.return_text.config(state='disabled')
            self.type_entry.delete(0,'end')
            self.port_entry.delete(0,'end')
            self.type_entry.config(state='normal')
            self.port_entry.config(state='normal')
            self.request_button.config(state='normal')
        else:
            self.return_text.config(state='normal')
            self.return_text.delete(1.0,END)
            self.return_text.config(state='disabled')
            self.type_entry.delete(0,'end')
            self.port_entry.delete(0,'end')
            self.type_entry.config(state='normal')
            self.port_entry.config(state='normal')
            self.request_button.config(state='normal')

            self.device_list = BeetleConnection.possible_connections()

            possible_values = [
                x.device for x in self.device_list if "Arduino" in str(x)
            ]
            self.device_picker["values"] = possible_values
            if len(possible_values) > 0:
                self.device_picker.current(0)
            self.event_disconnected()
   
class DiagnosticFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

		#Code for setting the app name and icon
        controller.title("Smart Power Meter")
        controller.call('wm', 'iconphoto', self.winfo_toplevel()._w, tk.PhotoImage(file='baseline_power_black_24dp.png'))
		#
		
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
        self.page_title_label.grid(column=0, row=0, padx=100, pady=5,sticky="NSEW", columnspan=4)		
        self.page_title_label.config(font=("Calibri", 18))	


	
class Main:
    def __init__(self):
        #self.window = Tk()
        #self.connection_frame = ConnectionFrame(self)
        #self.connection_frame.grid(row=0, sticky="NWE", columnspan=4)

        #self.window.resizable(False, False)
        #self.window.mainloop()
		
        #self.window = Tk()
        #self.window.geometry("800x800")
		
        app = App()
        app.mainloop()

Main()
