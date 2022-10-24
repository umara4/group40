import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3

#two variables that are subject to change based on the pacemaker.
#warning is a boolean to show that there is another pacemaker nearby
warning = True
#connection is a boolean to show that the connection with the pacemaker
connection = True

#stores the login creditals
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
            "CREATE TABLE IF NOT EXISTS AAIparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, AtrialAmplitude text, AtrialWidth text, AtrialSensitivity text, ARP text, PVARP text, Hysteresis text, RateSmoothing text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()

    def Insert(self, userID, LRL, URL,Atrial_Amplitude, Atrial_Pulse_Width, Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing):
        self.Cursor.execute("INSERT INTO AAIparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width,Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing))
        self.connection.commit()

    def Display(self):
        self.Cursor.execute("SELECT * FROM AAIparameter_table")
        records = self.Cursor.fetchall()
        return records

    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM AAIparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults

    def Update(self, LRL, URL,Atrial_Amplitude, Atrial_Pulse_Width, Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing, userID):
        self.Cursor.execute(
            "UPDATE AAIparameter_table SET LRL = ?, URL = ?, AtrialAmplitude = ?, AtrialWidth = ?, AtrialSensitivity = ?, ARP = ?, PVARP = ?, Hysteresis = ?, RateSmoothing = ? WHERE userID = ?",
            (LRL, URL, Atrial_Amplitude,Atrial_Pulse_Width,Atrial_Sensitivity, ARP, PVARP, Hysteresis, Rate_Smoothing, userID))
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
            "CREATE TABLE IF NOT EXISTS VVIparameter_table (UserID PRIMARYKEY text unique, LRL text, URL text, VentricularAmplitude text, VentricularWidth text, VentricularSensitivity text, VRP text, Hysteresis text, RateSmoothing text)")

    def __del__(self):
        self.Cursor.close()
        self.connection.close()

    def Insert(self, userID, LRL, URL,Ventricular_Amplitude, Ventricular_Pulse_Width, Ventricular_Sensitivity, VRP, Hysteresis, Rate_Smoothing):
        self.Cursor.execute("INSERT INTO VVIparameter_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (userID, LRL, URL, Ventricular_Amplitude,Ventricular_Pulse_Width,Ventricular_Sensitivity, VRP, Hysteresis, Rate_Smoothing))
        self.connection.commit()

    def Display(self):
        self.Cursor.execute("SELECT * FROM VVIparameter_table")
        records = self.Cursor.fetchall()
        return records

    def Search(self, userID):
        self.Cursor.execute("SELECT * FROM VVIparameter_table WHERE UserID = ?", (userID,))
        searchResults = self.Cursor.fetchall()
        return searchResults

    def Update(self, LRL, URL,Ventricular_Amplitude, Ventricular_Pulse_Width, Ventricular_Sensitivity, VRP, Hysteresis, Rate_Smoothing, userID):
        self.Cursor.execute(
            "UPDATE VVIparameter_table SET LRL = ?, URL = ?, AtrialAmplitude = ?, AtrialWidth = ?, AtrialSensitivity = ?, ARP = ?, PVARP = ?, Hysteresis = ?, RateSmoothing = ? WHERE userID = ?",
            (LRL, URL, Ventricular_Amplitude,Ventricular_Pulse_Width,Ventricular_Sensitivity, VRP, Hysteresis, Rate_Smoothing, userID))
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
                                        "ARP", "PVARP","Hysteresis", "RateSmoothing")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("AtrialAmplitude", text="AtrialAmplitude")
        self.databaseView.heading("AtrialWidth", text="AtrialWidth")
        self.databaseView.heading("AtrialSensitivity", text="AtrialSensitivity")
        self.databaseView.heading("ARP", text="ARP")
        self.databaseView.heading("PVARP", text="PVARP")
        self.databaseView.heading("Hysteresis", text="Hysteresis")
        self.databaseView.heading("RateSmoothing", text="RateSmoothing")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("AtrialAmplitude", width=100)
        self.databaseView.column("AtrialWidth", width=100)
        self.databaseView.column("AtrialSensitivity", width=100)
        self.databaseView.column("ARP", width=100)
        self.databaseView.column("PVARP", width=100)
        self.databaseView.column("Hysteresis", width=100)
        self.databaseView.column("RateSmoothing", width=100)

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
                                        "VentricularSensitivity", "VRP", "Hysteresis", "RateSmoothing")

        # Treeview column headings
        self.databaseView.heading("UserID", text="UserID")
        self.databaseView.heading("LRL", text="LRL")
        self.databaseView.heading("URL", text="URL")
        self.databaseView.heading("VentricularAmplitude", text="VentricularAmplitude")
        self.databaseView.heading("VentricularWidth", text="VentricularWidth")
        self.databaseView.heading("VentricularSensitivity", text="VentricularSensitivity")
        self.databaseView.heading("VRP", text="VRP")
        self.databaseView.heading("Hysteresis", text="Hysteresis")
        self.databaseView.heading("RateSmoothing", text="RateSmoothing")

        self.databaseView.column("UserID", width=100)
        self.databaseView.column("LRL", width=100)
        self.databaseView.column("URL", width=100)
        self.databaseView.column("VentricularAmplitude", width=100)
        self.databaseView.column("VentricularWidth", width=100)
        self.databaseView.column("VentricularSensitivity", width=100)
        self.databaseView.column("VRP", width=100)
        self.databaseView.column("Hysteresis", width=100)
        self.databaseView.column("RateSmoothing", width=100)

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
        tkinter.Button(self.loginwindow, width=10, fg=cha_color, bg=bg_color, font=("times new roman", 10, "bold"),
                       text="Submit", command=self.Submit).grid(pady=15, padx=5, column=1,row=14)
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
        tkinter.Button(self.window, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Sign Out",
                       font=("times new roman", 15, "bold"), command=self.Signout).grid(pady=15, column=1, row=6)
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

    def Signout(self):
        self.window.destroy()
        self.homepage = HomePage()
    #directs to the mode window
    def Mode(self):
        self.modewindow = ModeWindow(self.UserID)

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
                self.parameterWindow = ParametersWindow(self.UserID)
            except AttributeError:
                tkinter.messagebox.showerror("Invalid Mode", "Select your mode first!")


#opens and intializes the parameters window
class ParametersWindow:
    def __init__(self, userID):
        self.UserID = userID
        self.login = LoginDatabase()
        self.result = self.login.ReturnMode(self.UserID)
        self.currentmode = self.result[0][4]
        self.parameterwindow = tkinter.Tk()
        self.parameterwindow.wm_title("Current Parameters")
        self.AAI = AAIParameterDatabase()
        self.VVI = VVIParameterDatabase()
        self.AOO = AOOParameterDatabase()
        self.VOO = VOOParameterDatabase()
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"

        #restricts the input allowed in parameters page
        self.LRLtype = list(range(50,91))
        self.URLtype = list(range(50,176,5))
        self.PulseAmplitudetype = ["Off", "1.25V", "2.5V", "3.75V", "5.0V"]
        self.PulseWidthtype = [0.05]
        self.Sensitivitytype = [0.25, 0.5, 0.75]
        self.RPtype = list(range(150,501,10))
        self.PVARPtype = list(range(150,501,10))
        self.Hysteresistype = ["Off", "Same as LRL"]
        self.RateSmoothingtype = ["Off", "3%", "6%", "9%", "12%", "15%", "18%", "21%", "25%"]

        #operational buttons
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="LRL: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=1)
        tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                      text="URL: ",
                      font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=2)
        tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Edit",
                       font=("times new roman", 15, "bold"), command=self.Edit).grid(pady=15, column=1, row=10)
        tkinter.Button(self.parameterwindow, width=20, relief=tkinter.GROOVE, fg=cha_color, bg=bg_color, text="Save",
                       font=("times new roman", 15, "bold"), command=self.Save).grid(pady=15, column=2, row=10)
        #the parameters shown when mode is AAI
        if self.currentmode == "AAI":
            #create the last hand side of the page consisting of labels displaying the name of the parameters
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Sensitivity: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=5)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="ARP: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=6)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="PVARP: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=7)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Hysteresis: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=8)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Rate Smoothing: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=9)

            #creates the right hand side of the page consisting of comboboxes
            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype, width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')
            self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                       state='disabled')
            self.ARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')
            self.PVARPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PVARPtype, width=20, state='disabled')
            self.HysteresisBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Hysteresistype,
                                                      width=20, state='disabled')
            self.RateSmoothingBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RateSmoothingtype, width=20,
                                                         state='disabled')
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
                self.HysteresisBox.set(self.searchresult[0][8])
                self.RateSmoothingBox.set(self.searchresult[0][9])
            else:
                self.AAIdefaultSetting()
            #location of the comboboxes
            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)
            self.SensitivityBox.grid(pady=5, column=3, row=5)
            self.ARPBox.grid(pady=5, column=3, row=6)
            self.PVARPBox.grid(pady=5, column=3, row=7)
            self.HysteresisBox.grid(pady=5, column=3, row=8)
            self.RateSmoothingBox.grid(pady=5, column=3, row=9)

        elif self.currentmode == "VVI":
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Sensitivity: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=5)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="VRP: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=6)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Hysteresis: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=7)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Rate Smoothing: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=8)

            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype,width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')
            self.SensitivityBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Sensitivitytype, width=20,
                                                       state='disabled')
            self.VRPBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RPtype, width=20, state='disabled')
            self.HysteresisBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.Hysteresistype, width=20,
                                                      state='disabled')
            self.RateSmoothingBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.RateSmoothingtype, width=20,
                                                         state='disabled')
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
                self.HysteresisBox.set(self.searchresult[0][7])
                self.RateSmoothingBox.set(self.searchresult[0][8])
            else:
                self.VVIdefaultSetting()

            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)
            self.SensitivityBox.grid(pady=5, column=3, row=5)
            self.VRPBox.grid(pady=5, column=3, row=6)
            self.HysteresisBox.grid(pady=5, column=3, row=7)
            self.RateSmoothingBox.grid(pady=5, column=3, row=8)

        elif self.currentmode == "AOO":
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Atrial Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)
            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype,width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')
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

            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)

        elif self.currentmode == "VOO":
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Amplitude: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=3)
            tkinter.Label(self.parameterwindow, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color,
                          text="Ventricular Pulse Width: ",
                          font=("times new roman", 10, "bold"), width=50).grid(pady=20, column=1, row=4)

            self.LRLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.LRLtype, width=20, state='disabled')
            self.URLBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.URLtype, width=20, state='disabled')
            self.PulseAmplitudeBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseAmplitudetype,width=20,
                                                          state='disabled')
            self.PulseWidthBox = tkinter.ttk.Combobox(self.parameterwindow, values=self.PulseWidthtype, width=20,
                                                      state='disabled')
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

            self.LRLBox.grid(pady=5, column=3, row=1)
            self.URLBox.grid(pady=5, column=3, row=2)
            self.PulseAmplitudeBox.grid(pady=5, column=3, row=3)
            self.PulseWidthBox.grid(pady=5, column=3, row=4)
    #save the currently entered parameter and disable the comboboxes from editing again until clicking edit again
    def Save(self):
        self.AAIdatabase = AAIParameterDatabase()
        self.VVIdatabase = VVIParameterDatabase()
        self.AOOdatabase = AOOParameterDatabase()
        self.VOOdatabase = VOOParameterDatabase()
        self.LRLBox.config(state='disabled')
        self.URLBox.config(state='disabled')
        self.PulseAmplitudeBox.config(state='disabled')
        self.PulseWidthBox.config(state='disabled')
        if self.currentmode == "AAI":
            self.ARPBox.config(state='disabled')
            self.PVARPBox.config(state='disabled')
            self.SensitivityBox.config(state='disabled')
            self.HysteresisBox.config(state='disabled')
            self.RateSmoothingBox.config(state='disabled')
            #try to insert the parameters, if failed because of previously saved parameters, update them
            try:
                self.AAIdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.ARPBox.get(),self.PVARPBox.get(),
                                        self.SensitivityBox.get(),self.HysteresisBox.get(),self.RateSmoothingBox.get())
            except sqlite3.IntegrityError:
                self.AAIdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.ARPBox.get(),self.PVARPBox.get(),
                                        self.SensitivityBox.get(),self.HysteresisBox.get(),self.RateSmoothingBox.get(),
                                        self.UserID)
        elif self.currentmode == "VVI":
            self.VRPBox.config(state='disabled')
            self.SensitivityBox.config(state='disabled')
            self.HysteresisBox.config(state='disabled')
            self.RateSmoothingBox.config(state='disabled')
            try:
                self.VVIdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.VRPBox.get(),
                                        self.SensitivityBox.get(),self.HysteresisBox.get(),self.RateSmoothingBox.get())
            except sqlite3.IntegrityError:
                self.VVIdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.VRPBox.get(),
                                        self.SensitivityBox.get(),self.HysteresisBox.get(),self.RateSmoothingBox.get(),
                                        self.UserID)
        elif self.currentmode == "AOO":
            try:
                self.AOOdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get())
            except sqlite3.IntegrityError:
                self.AOOdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.UserID)
        elif self.currentmode == "VOO":
            try:
                self.VOOdatabase.Insert(self.UserID, self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get())
            except sqlite3.IntegrityError:
                self.VOOdatabase.Update(self.LRLBox.get(), self.URLBox.get(), self.PulseAmplitudeBox.get(),
                                        self.PulseWidthBox.get(),self.UserID)
        tkinter.messagebox.showinfo("Saved", "Saved")
    #make the comboxes editable again
    def Edit(self):
        self.LRLBox.config(state='readonly')
        self.URLBox.config(state='readonly')
        self.PulseAmplitudeBox.config(state='readonly')
        self.PulseWidthBox.config(state='readonly')
        if self.currentmode == "AAI":
            self.SensitivityBox.config(state='readonly')
            self.ARPBox.config(state='readonly')
            self.PVARPBox.config(state='readonly')
            self.HysteresisBox.config(state='readonly')
            self.RateSmoothingBox.config(state='readonly')
        elif self.currentmode == "VVI":
            self.SensitivityBox.config(state='readonly')
            self.VRPBox.config(state='readonly')
            self.HysteresisBox.config(state='readonly')
            self.RateSmoothingBox.config(state='readonly')
        tkinter.messagebox.showinfo("Edit Mode on", "Edit Mode on")
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
    #default setting if no previous saved paramters
    def AAIdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(90)
        self.PulseAmplitudeBox.set("Off")
        self.PulseWidthBox.set(0.05)
        self.SensitivityBox.set(0.25)
        self.ARPBox.set(200)
        self.PVARPBox.set(200)
        self.HysteresisBox.set("Same as LRL")
        self.RateSmoothingBox.set("Off")

    def VVIdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(90)
        self.PulseAmplitudeBox.set("Off")
        self.PulseWidthBox.set(0.05)
        self.SensitivityBox.set(0.25)
        self.VRPBox.set(200)
        self.HysteresisBox.set("Same as LRL")
        self.RateSmoothingBox.set("Off")

    def AOOVOOdefaultSetting(self):
        self.LRLBox.set(60)
        self.URLBox.set(90)
        self.PulseAmplitudeBox.set("Off")
        self.PulseWidthBox.set(0.05)

#opens and initializes the mode window
class ModeWindow:
    def __init__(self, userID):
        self.UserID = userID
        self.login = LoginDatabase()
        self.result = self.login.ReturnMode(self.UserID)
        #the current mode
        self.cmode = self.result[0][4]
        self.window = tkinter.Tk()
        self.window.wm_title("Pacemaker Modes")
        bg_color = "blue"
        fg_color = "white"
        cha_color = "black"
        #the buttons on the page for the modes
        tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text="Current Mode: ",
                      font=("times new roman", 20, "bold"), width=30).grid(pady=20, column=1, row=1)
        self.label1 = tkinter.Label(self.window, relief=tkinter.GROOVE, fg=fg_color, bg=bg_color, text=self.cmode,
                      font=("times new roman", 20, "bold"), width=30)
        self.label1.grid(pady=20, column=2, row=1)
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
    #when mode is AOO
    def AOO(self):
        #updates the database for the new value of mode
        self.cmode = "AOO"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="disabled")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
    #when mode is VOO
    def VOO(self):
        # updates the database for the new value of mode
        self.cmode = "VOO"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="disabled")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="active")
    #when mode is AAI
    def AAI(self):
        # updates the database for the new value of mode
        self.cmode = "AAI"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="disabled")
        self.VVIbutton.config(state="active")
    #when mdoe is VVI
    def VVI(self):
        # updates the database for the new value of mode
        self.cmode = "VVI"
        self.login.setMode("UPDATE Login_table SET mode = ? WHERE UserID = ?", (self.cmode, self.UserID))
        self.label1.config(text=self.cmode)
        self.AOObutton.config(state="active")
        self.VOObutton.config(state="active")
        self.AAIbutton.config(state="active")
        self.VVIbutton.config(state="disabled")

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
