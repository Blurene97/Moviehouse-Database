from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import mysql.connector
import commands
import functions
import os
import time
import sys
import getpass
#connect to database
dbcon = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "moviehousedb",
    port = 3306,
    autocommit = True
    )
#database cursur
print(dbcon)
dbcur = dbcon.cursor()

#main gui
def startScreen():
    global gui
    global LoginButton
    global header
    gui = Tk()
    gui.title("Movie House Database")
    gui.iconbitmap('images\\icon.ico')
    gui.geometry("1280x720")
    bg1 = ImageTk.PhotoImage(Image.open('images\\bg1.png'))
    background = Label(gui, image = bg1)
    background.place(x = 0, y = 0)
    header = Label(text = "IDALSO Moviehouse", bg = "#41c9a9", width = 1280, height = 2, font = ("Ting Tong", 65))
    header.pack()
    LoginButton = Button(gui, text = "Login", bg = "white", width = 10, height = 1, font = ("AGFatumC", 15), command = LoginGUI)
    LoginButton.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    gui.mainloop()

def mainProgram(userInfo):
    print(userInfo)
    header.destroy()
    LoginButton.destroy()
    header2 = Label(text = "IDALSO Moviehouse", bg = "#41c9a9", width = 1280, height = 1, font = ("Ting Tong", 40))
    header2.pack()
    StaffID = Label(gui, text = ("UserID:", userInfo), bg = "#41c9a9", font = ("AGFatumC", 15))
    StaffID.place(x = 0, y = 0)
    TicketButton = Button(gui, text = "Generate Ticket", fg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = ticketManipulation)
    TicketButton.place(relx = 0.37, rely = 0.18)
    MoviesButton = Button(gui, text = "Movies Screening", fg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = moviesManipulation)
    MoviesButton.place(relx = 0.37, rely = 0.38)
    DBTableButton = Button(gui, text = "Database Tables", fg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = dbManipulation)
    DBTableButton.place(relx = 0.37, rely = 0.58)
    StaffButton = Button(gui, text = "Staff", fg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = staffManipulation)
    StaffButton.place(relx = 0.37, rely = 0.78)

#commands
'''ticket'''
def ticketManipulation():
    screen2 = Toplevel(gui)
    screen2.title("Ticket")
    screen2.geometry("320x400")
    screen2.iconbitmap('images\\icon.ico')
    LogsButton = Button(screen2, text = "Ticket Logs", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = displayTicketTable)
    LogsButton.place(relx = 0.075, rely = 0.08)
    AddButton = Button(screen2, text = "Add Ticket", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = insertTicketTable)
    AddButton.place(relx = 0.075, rely = 0.28)
    PullButton = Button(screen2, text = "Search Ticket", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = ticketPull)
    PullButton.place(relx = 0.075, rely = 0.48)
    DeleteButton = Button(screen2, text = "Delete Ticket", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = ticketDelete)
    DeleteButton.place(relx = 0.075, rely = 0.68)

def displayTicketTable():
    screen3 = Toplevel(gui)
    screen3.title("Ticket Table")
    screen3.geometry("810x900")
    screen3.iconbitmap('images\\icon.ico')
    #scrollbar
    screenFrame = Frame(screen3)
    screenFrame.pack(fill = BOTH, expand = 1)
    screenCanvas = Canvas(screenFrame)
    screenCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
    windowSlider = ttk.Scrollbar(screenFrame, orient = VERTICAL, command = screenCanvas.yview)
    windowSlider.pack(side = RIGHT, fill = Y)
    screenCanvas.configure(yscrollcommand = windowSlider.set)
    screenCanvas.bind('<Configure>', lambda e: screenCanvas.configure(scrollregion = screenCanvas.bbox("all")))
    screenFrame2 = Frame(screenCanvas)
    screenCanvas.create_window((0,0), window = screenFrame2, anchor = "nw")
    #tablehead
    TicketNo = Button(screenFrame2, text = "Ticket No", width = 15, fg = "white", bg = "#41c9a9")
    TicketNo.grid(row = 0, column = 0)
    Staff_ID = Button(screenFrame2, text = "Staff ID", width = 15, fg = "white", bg = "#41c9a9")
    Staff_ID.grid(row = 0, column = 1)
    CDName = Button(screenFrame2, text = "Movie Code", width = 15, fg = "white", bg = "#41c9a9")
    CDName.grid(row = 0, column = 2)
    CinemaNo = Button(screenFrame2, text = "Cinema No", width = 15, fg = "white", bg = "#41c9a9")
    CinemaNo.grid(row = 0, column = 3)
    SeatNo = Button(screenFrame2, text = "Seat No", width = 15, fg = "white", bg = "#41c9a9")
    SeatNo.grid(row = 0, column = 4)
    SchedNo = Button(screenFrame2, text = "Sched Code", width = 15, fg = "white", bg = "#41c9a9")
    SchedNo.grid(row = 0, column = 5)
    
    dbcur.execute(commands.displayTicket_Logs())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenFrame2, width = 15, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def insertTicketTable():
    global screenInsert
    screenInsert = Toplevel(gui)
    screenInsert.title("Add Ticket")
    screenInsert.geometry("300x200")
    screenInsert.iconbitmap('images\\icon.ico')
    
    global movieCode
    global cinemaNum
    global seatNum
    global screeningCode
    global movieCode_entry
    global cinemaNum_entry
    global seatNum_entry
    global screeningCode_entry

    movieCode = StringVar()
    cinemaNum = StringVar()
    seatNum = StringVar()
    screeningCode = StringVar()

    movieCode_entry = Entry(screenInsert, textvariable = movieCode)
    movieCode_entry.grid(row = 0, column = 1, padx = 20)
    movieCode_label = Label(screenInsert, text = "Movie Code")
    movieCode_label.grid(row = 0, column = 0)
    
    cinemaNum_entry = Entry(screenInsert, textvariable = cinemaNum)
    cinemaNum_entry.grid(row = 1, column = 1)
    cinemaNum_label = Label(screenInsert, text = "Cinema No.")
    cinemaNum_label.grid(row = 1, column = 0)
    
    seatNum_entry = Entry(screenInsert, textvariable =seatNum)
    seatNum_entry.grid(row = 2, column = 1)
    seatNum_label = Label(screenInsert, text = "Seat No.")
    seatNum_label.grid(row = 2, column = 0)
    
    screeningCode_entry = Entry(screenInsert, textvariable = screeningCode)
    screeningCode_entry.grid(row = 3, column = 1)
    screeningCode_label = Label(screenInsert, text = "Screening Code")
    screeningCode_label.grid(row = 3, column = 0)
    
    ticketSubmit = Button(screenInsert, text = "Submit", bg = "#41c9a9", command = insertTicketCMD)
    ticketSubmit.grid(row = 5, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)

def insertTicketCMD():
    values = []
    values.append(userID.get())
    values.append(movieCode.get())
    values.append(cinemaNum.get())
    values.append(seatNum.get())
    values.append(screeningCode.get())
    print(values)

    try:
        commands.insertTicket(values)
        insertFeedback = Label(screenInsert, text = "Insert successful", fg = "#41c9a9", font = ("AGFatumC", 15))
        insertFeedback.grid(row = 6, column = 0, columnspan = 2)
        print("//---___*Rapper*Ha*Sooyoung*___---//")
    except mysql.connector.errors.IntegrityError:
        insertFeedback = Label(screenInsert, text = "Incorrect Values", fg = "#c40000", font = ("AGFatumC", 15))
        insertFeedback.grid(row = 6, column = 0, columnspan = 2)
        print("//---___*Rapper*Ha*Sooyoung*___---//")

    movieCode_entry.delete(0, END)
    cinemaNum_entry.delete(0, END)
    seatNum_entry.delete(0, END)
    screeningCode_entry.delete(0, END)

def ticketPull():
    screenPull = Toplevel(gui)
    screenPull.title("Ticket Logs")
    screenPull.geometry("500x300")
    screenPull.iconbitmap('images\\icon.ico')
    global screenPullFrame

    screenFrame = Frame(screenPull)
    screenFrame.pack(fill = BOTH, expand = 1)
    screenCanvas = Canvas(screenFrame)
    screenCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
    windowSlider = ttk.Scrollbar(screenFrame, orient = VERTICAL, command = screenCanvas.yview)
    windowSlider.pack(side = RIGHT, fill = Y)
    screenCanvas.configure(yscrollcommand = windowSlider.set)
    screenCanvas.bind('<Configure>', lambda e: screenCanvas.configure(scrollregion = screenCanvas.bbox("all")))
    screenPullFrame = Frame(screenCanvas)
    screenCanvas.create_window((0,0), window = screenPullFrame, anchor = "nw")
    
    global ticketNum
    global ticketNum_entry
    ticketNum = StringVar()
    
    ticketNum_entry = Entry(screenPullFrame, textvariable = ticketNum)
    ticketNum_label = Label(screenPullFrame, text = "Insert ticket number", font = ("AGFatumC", 15))
    ticketNum_label.pack()
    ticketNum_entry.pack()
    submitPull = Button(screenPullFrame, text = "Submit", bg = "#41c9a9", command = pullTicketCMD)
    submitPull.pack()
    print("Ticket Pull")

def pullTicketCMD():
    screen = screenPullFrame
    try:
        ticketNum_value = ticketNum.get()
        val = int(ticketNum_value)
        checkReturn = commands.checkTicket(ticketNum_value)
        if int(checkReturn[0]) == 1:
            TableLogs = commands.selectTicket(int(ticketNum_value))
            for i in TableLogs:
                Label(screen, text = "_______________________________________________________________________", height = 1).pack()
                TN_label = Label(screen, text = ("Ticket No: ", i[0]), bg = "#41c9a9", font = ("AGFatumC", 15))
                MC_label = Label(screen, text = ("Movie Code: ", i[1]), bg = "#41c9a9", font = ("AGFatumC", 15))
                MT_label = Label(screen, text = ("Movie Title: ", i[2]), bg = "#41c9a9", font = ("AGFatumC", 15))
                SC_label = Label(screen, text = ("Screening Code: ", i[3]), bg = "#41c9a9", font = ("AGFatumC", 15))
                ST_label = Label(screen, text = ("Start: ", i[4]), bg = "#41c9a9", font = ("AGFatumC", 15))
                ED_label = Label(screen, text = ("End: ", i[5]), bg = "#41c9a9", font = ("AGFatumC", 15))
                SN_label = Label(screen, text = ("Seat No: ", i[6]), bg = "#41c9a9", font = ("AGFatumC", 15))
                TN_label.pack()
                MC_label.pack()
                MT_label.pack()
                SC_label.pack()
                ST_label.pack()
                ED_label.pack()
                SN_label.pack()
                ticketNum_entry.delete(0, END)
        else:
            Label(screen, text = "_______________________________________________________________________", height = 1).pack()
            insertFeedback = Label(screen, text = "Ticket number does not exist.", fg = "#c40000", font = ("AGFatumC", 15))
            insertFeedback.pack()
            ticketNum_entry.delete(0, END)
            print("//---___*Rapper*Ha*Sooyoung*___---//")
    except ValueError:
        Label(screen, text = "_______________________________________________________________________", height = 1).pack()
        insertFeedback = Label(screen, text = "Invalid ticket number.", fg = "#c40000", font = ("AGFatumC", 15))
        insertFeedback.pack()
        ticketNum_entry.delete(0, END)
        print("//---___*Rapper*Ha*Sooyoung*___---//")

def ticketDelete():
    global screenDelete
    screenDelete = Toplevel(gui)
    screenDelete.title("Delete Ticket")
    screenDelete.geometry("550x200")
    screenDelete.iconbitmap('images\\icon.ico')
    
    global ticketNumDEL
    global ticketNumDEL_entry
    ticketNumDEL = StringVar()
    
    ticketNumDEL_entry = Entry(screenDelete, textvariable = ticketNumDEL)
    ticketNumDEL_label = Label(screenDelete, text = "Insert ticket number of the ticket to be DELETED", font = ("AGFatumC", 15))
    ticketNumDEL_label.pack()
    ticketNumDEL_entry.pack()
    submitDEL = Button(screenDelete, text = "Submit", bg = "#41c9a9", command = deleteTicketCMD)
    submitDEL.pack()
    
def deleteTicketCMD():
    try:
        ticketNumDEL_value = ticketNumDEL.get()
        val = int(ticketNumDEL_value)
        checkReturn = commands.checkTicket(ticketNumDEL_value)
        if int(checkReturn[0]) == 1:
            commands.deleteTicket(ticketNumDEL_value)
            insertFeedback = Label(screenDelete, text = "Ticket log successfully deleted.", fg = "#41c9a9", font = ("AGFatumC", 15))
            insertFeedback.pack()
            print("//---___*Rapper*Ha*Sooyoung*___---//")
        else:
            commands.deleteTicket(ticketNumDEL_value)
            insertFeedback = Label(screenDelete, text = "Ticket number does not exist.", fg = "#c40000", font = ("AGFatumC", 15))
            insertFeedback.pack()
            print("//---___*Rapper*Ha*Sooyoung*___---//")      
    except ValueError:
        commands.deleteTicket(ticketNumDEL_value)
        insertFeedback = Label(screenDelete, text = "Invalid ticket number.", fg = "#c40000", font = ("AGFatumC", 15))
        insertFeedback.pack()
        print("//---___*Rapper*Ha*Sooyoung*___---//")      

'''movies'''
def moviesManipulation():
    screen4 = Toplevel(gui)
    screen4.title("Movies")
    screen4.geometry("320x400")
    screen4.iconbitmap('images\\icon.ico')
    LogsButton = Button(screen4, text = "Movies", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = displayMoviesTable)
    LogsButton.place(relx = 0.075, rely = 0.18)
    MHallsButton = Button(screen4, text = "Screening Schedule(by time)", bg = "#41c9a9", width = 24, height = 3, font = ("AGFatumC", 13), command = displaySSTime)
    MHallsButton.place(relx = 0.075, rely = 0.38)
    SPMButton = Button(screen4, text = "Screening Schedule(by movie)", bg = "#41c9a9", width = 24, height = 3, font = ("AGFatumC", 13), command = displaySSMovie)
    SPMButton.place(relx = 0.075, rely = 0.61)

def displayMoviesTable():
    screenMTable = Toplevel(gui)
    screenMTable.title("Movies Table")
    screenMTable.geometry("1690x150")
    screenMTable.iconbitmap('images\\icon.ico')
    #tablehead
    codeName = Button(screenMTable, text = "Movie Code", width = 69, fg = "white", bg = "#41c9a9")
    codeName.grid(row = 0, column = 0)
    movieTitle = Button(screenMTable, text = "Title", width = 69, fg = "white", bg = "#41c9a9")
    movieTitle.grid(row = 0, column = 1)
    movieDesc = Button(screenMTable, text = "Movie Description", width = 69, fg = "white", bg = "#41c9a9")
    movieDesc.grid(row = 0, column = 2)
    
    dbcur.execute(commands.displayMovies())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenMTable, width = 69, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def displaySSTime():
    screenMTime = Toplevel(gui)
    screenMTime.title("Screening Schedule(Time)")
    screenMTime.geometry("1500x300")
    screenMTime.iconbitmap('images\\icon.ico')
    #tablehead
    showStart = Button(screenMTime, text = "Start", width = 30, fg = "white", bg = "#41c9a9")
    showStart.grid(row = 0, column = 0)
    showEnd = Button(screenMTime, text = "End", width = 30, fg = "white", bg = "#41c9a9")
    showEnd.grid(row = 0, column = 1)
    timeCode = Button(screenMTime, text = "Time Code", width = 30, fg = "white", bg = "#41c9a9")
    timeCode.grid(row = 0, column = 2)
    cinemaHall = Button(screenMTime, text = "Cinema Hall", width = 30, fg = "white", bg = "#41c9a9")
    cinemaHall.grid(row = 0, column = 3)
    mCode = Button(screenMTime, text = "Movie Code", width = 30, fg = "white", bg = "#41c9a9")
    mCode.grid(row = 0, column = 4)
    mTitle = Button(screenMTime, text = "Title", width = 30, fg = "white", bg = "#41c9a9")
    mTitle.grid(row = 0, column = 5)

    dbcur.execute(commands.displayScreeningSched())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenMTime, width = 30, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def displaySSMovie():
    global screenMMovie
    screenMMovie = Toplevel(gui)
    screenMMovie.title("Screening Schedule(Movie)")
    screenMMovie.geometry("1500x300")
    screenMMovie.iconbitmap('images\\icon.ico')
    
    menuButton = Menubutton(screenMMovie, text = "Click here to pick a Movie", bg = "#41c9a9")
    menuButton.menu = Menu(menuButton)
    menuButton["menu"] = menuButton.menu 
    menuButton.menu.add_command(label = "New AVENGERS", command = SSMovieCMD1)
    menuButton.menu.add_command(label = "Final Fantasy 7: Loveless Chronos", command = SSMovieCMD2)
    menuButton.menu.add_command(label = "LOONA Midnight Festival", command = SSMovieCMD3)
    menuButton.menu.add_command(label = "STAR WARS: Rise of a New Code", command = SSMovieCMD4)
    menuButton.grid(row = 0, column = 0, columnspan = 2)

def SSMovieCMD1():
    mCode = Button(screenMMovie, text = "Movie Code", width = 30, fg = "white", bg = "#41c9a9")
    mCode.grid(row = 2, column = 0)
    mTitle = Button(screenMMovie, text = "Movie Title", width = 30, fg = "white", bg = "#41c9a9")
    mTitle.grid(row = 2, column = 1)
    cinemaHall = Button(screenMMovie, text = "Cinema Hall", width = 30, fg = "white", bg = "#41c9a9")
    cinemaHall.grid(row = 2, column = 2)
    SStart = Button(screenMMovie, text = "Start", width = 30, fg = "white", bg = "#41c9a9")
    SStart.grid(row = 2, column = 3)
    SEnd = Button(screenMMovie, text = "End", width = 30, fg = "white", bg = "#41c9a9")
    SEnd.grid(row = 2, column = 4)
    TCode = Button(screenMMovie, text = "Time Code", width = 30, fg = "white", bg = "#41c9a9")
    TCode.grid(row = 2, column = 5)
    
    TableLogs = commands.displayMoviesSched("AVR-NW")
    i = 3 
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenMMovie, width = 30, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def SSMovieCMD2():
    mCode = Button(screenMMovie, text = "Movie Code", width = 30, fg = "white", bg = "#41c9a9")
    mCode.grid(row = 2, column = 0)
    mTitle = Button(screenMMovie, text = "Movie Title", width = 30, fg = "white", bg = "#41c9a9")
    mTitle.grid(row = 2, column = 1)
    cinemaHall = Button(screenMMovie, text = "Cinema Hall", width = 30, fg = "white", bg = "#41c9a9")
    cinemaHall.grid(row = 2, column = 2)
    SStart = Button(screenMMovie, text = "Start", width = 30, fg = "white", bg = "#41c9a9")
    SStart.grid(row = 2, column = 3)
    SEnd = Button(screenMMovie, text = "End", width = 30, fg = "white", bg = "#41c9a9")
    SEnd.grid(row = 2, column = 4)
    TCode = Button(screenMMovie, text = "Time Code", width = 30, fg = "white", bg = "#41c9a9")
    TCode.grid(row = 2, column = 5)
    
    TableLogs = commands.displayMoviesSched("FF7-LC")
    i = 3 
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenMMovie, width = 30, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def SSMovieCMD3():
    mCode = Button(screenMMovie, text = "Movie Code", width = 30, fg = "white", bg = "#41c9a9")
    mCode.grid(row = 2, column = 0)
    mTitle = Button(screenMMovie, text = "Movie Title", width = 30, fg = "white", bg = "#41c9a9")
    mTitle.grid(row = 2, column = 1)
    cinemaHall = Button(screenMMovie, text = "Cinema Hall", width = 30, fg = "white", bg = "#41c9a9")
    cinemaHall.grid(row = 2, column = 2)
    SStart = Button(screenMMovie, text = "Start", width = 30, fg = "white", bg = "#41c9a9")
    SStart.grid(row = 2, column = 3)
    SEnd = Button(screenMMovie, text = "End", width = 30, fg = "white", bg = "#41c9a9")
    SEnd.grid(row = 2, column = 4)
    TCode = Button(screenMMovie, text = "Time Code", width = 30, fg = "white", bg = "#41c9a9")
    TCode.grid(row = 2, column = 5)
    
    TableLogs = commands.displayMoviesSched("LNA-MF")
    i = 3 
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenMMovie, width = 30, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def SSMovieCMD4():
    mCode = Button(screenMMovie, text = "Movie Code", width = 30, fg = "white", bg = "#41c9a9")
    mCode.grid(row = 2, column = 0)
    mTitle = Button(screenMMovie, text = "Movie Title", width = 30, fg = "white", bg = "#41c9a9")
    mTitle.grid(row = 2, column = 1)
    cinemaHall = Button(screenMMovie, text = "Cinema Hall", width = 30, fg = "white", bg = "#41c9a9")
    cinemaHall.grid(row = 2, column = 2)
    SStart = Button(screenMMovie, text = "Start", width = 30, fg = "white", bg = "#41c9a9")
    SStart.grid(row = 2, column = 3)
    SEnd = Button(screenMMovie, text = "End", width = 30, fg = "white", bg = "#41c9a9")
    SEnd.grid(row = 2, column = 4)
    TCode = Button(screenMMovie, text = "Time Code", width = 30, fg = "white", bg = "#41c9a9")
    TCode.grid(row = 2, column = 5)
    
    TableLogs = commands.displayMoviesSched("STW-EX")
    i = 3
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenMMovie, width = 30, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

'''database tables'''
def dbManipulation():
    screen5 = Toplevel(gui)
    screen5.title("Database")
    screen5.geometry("250x320")
    screen5.iconbitmap('images\\icon.ico')
    TicketButton = Button(screen5, text = "Ticket", bg = "#41c9a9", width = 18, height = 1, font = ("AGFatumC", 15), command = dbTicket)
    TicketButton.place(relx = 0.02, rely = 0.05)
    CinemaButton = Button(screen5, text = "Cinema", bg = "#41c9a9", width = 18, height = 1, font = ("AGFatumC", 15), command = dbCinema)
    CinemaButton.place(relx = 0.02, rely = 0.20)
    MovieButton = Button(screen5, text = "Movies", bg = "#41c9a9", width = 18, height = 1, font = ("AGFatumC", 15), command = dbMovie)
    MovieButton.place(relx = 0.02, rely = 0.35)
    ShowsButton = Button(screen5, text = "Showing times", bg = "#41c9a9", width = 18, height = 1, font = ("AGFatumC", 15), command = dbShows)
    ShowsButton.place(relx = 0.02, rely = 0.50)
    ScreeningsButton = Button(screen5, text = "Sceenings", bg = "#41c9a9", width = 18, height = 1, font = ("AGFatumC", 15), command = dbScreening)
    ScreeningsButton.place(relx = 0.02, rely = 0.65)

def dbTicket():
    screen3 = Toplevel(gui)
    screen3.title("Ticket Table")
    screen3.geometry("810x900")
    screen3.iconbitmap('images\\icon.ico')
    #scrollbar
    screenFrame = Frame(screen3)
    screenFrame.pack(fill = BOTH, expand = 1)
    screenCanvas = Canvas(screenFrame)
    screenCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
    windowSlider = ttk.Scrollbar(screenFrame, orient = VERTICAL, command = screenCanvas.yview)
    windowSlider.pack(side = RIGHT, fill = Y)
    screenCanvas.configure(yscrollcommand = windowSlider.set)
    screenCanvas.bind('<Configure>', lambda e: screenCanvas.configure(scrollregion = screenCanvas.bbox("all")))
    screenFrame2 = Frame(screenCanvas)
    screenCanvas.create_window((0,0), window = screenFrame2, anchor = "nw")
    #tablehead
    TicketNo = Button(screenFrame2, text = "Ticket No", width = 15, fg = "white", bg = "#41c9a9")
    TicketNo.grid(row = 0, column = 0)
    Staff_ID = Button(screenFrame2, text = "Staff ID", width = 15, fg = "white", bg = "#41c9a9")
    Staff_ID.grid(row = 0, column = 1)
    CDName = Button(screenFrame2, text = "Movie Code", width = 15, fg = "white", bg = "#41c9a9")
    CDName.grid(row = 0, column = 2)
    CinemaNo = Button(screenFrame2, text = "Cinema No", width = 15, fg = "white", bg = "#41c9a9")
    CinemaNo.grid(row = 0, column = 3)
    SeatNo = Button(screenFrame2, text = "Seat No", width = 15, fg = "white", bg = "#41c9a9")
    SeatNo.grid(row = 0, column = 4)
    SchedNo = Button(screenFrame2, text = "Sched Code", width = 15, fg = "white", bg = "#41c9a9")
    SchedNo.grid(row = 0, column = 5)
    
    dbcur.execute(commands.displayTicket_Logs())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenFrame2, width = 15, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def dbCinema():
    screenCinema = Toplevel(gui)
    screenCinema.title("Cinama halls Table")
    screenCinema.geometry("270x110")
    screenCinema.iconbitmap('images\\icon.ico')
    #tablehead
    CinemaNo = Button(screenCinema, text = "Cinema No", width = 15, fg = "white", bg = "#41c9a9")
    CinemaNo.grid(row = 0, column = 0)
    MaxCapacity = Button(screenCinema, text = "Max Capacity", width = 15, fg = "white", bg = "#41c9a9")
    MaxCapacity.grid(row = 0, column = 1)
    dbcur.execute(commands.displayCinema_Hall())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenCinema, width = 15, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def dbMovie():
    screenMTable = Toplevel(gui)
    screenMTable.title("Movies Table")
    screenMTable.geometry("1690x150")
    screenMTable.iconbitmap('images\\icon.ico')
    #tablehead
    codeName = Button(screenMTable, text = "Ticket No", width = 69, fg = "white", bg = "#41c9a9")
    codeName.grid(row = 0, column = 0)
    movieTitle = Button(screenMTable, text = "Staff ID", width = 69, fg = "white", bg = "#41c9a9")
    movieTitle.grid(row = 0, column = 1)
    movieDesc = Button(screenMTable, text = "Movie Code", width = 69, fg = "white", bg = "#41c9a9")
    movieDesc.grid(row = 0, column = 2)
    
    dbcur.execute(commands.displayMovies())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenMTable, width = 69, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

def dbShows():
    screenShows = Toplevel(gui)
    screenShows.title("Showtime Table")
    screenShows.geometry("525x320")
    screenShows.iconbitmap('images\\icon.ico')
    #tablehead
    HallNo = Button(screenShows, text = "Hall No", width = 15, fg = "white", bg = "#41c9a9")
    HallNo.grid(row = 0, column = 0)
    SchedCode = Button(screenShows, text = "Sched Code", width = 15, fg = "white", bg = "#41c9a9")
    SchedCode.grid(row = 0, column = 1)
    ShowStart = Button(screenShows, text = "Show Start", width = 15, fg = "white", bg = "#41c9a9")
    ShowStart.grid(row = 0, column = 2)
    ShowEnd = Button(screenShows, text = "Show End", width = 15, fg = "white", bg = "#41c9a9")
    ShowEnd.grid(row = 0, column = 3)
    dbcur.execute(commands.displayScreening())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenShows, width = 15, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1
    print("//---___*Rapper*Ha*Sooyoung*___---//")
    
def dbScreening():
    screenScreening = Toplevel(gui)
    screenScreening.title("Screening Schedule Table")
    screenScreening.geometry("400x310")
    screenScreening.iconbitmap('images\\icon.ico')
    #tablehead
    CinemaNo = Button(screenScreening, text = "Cinema No", width = 15, fg = "white", bg = "#41c9a9")
    CinemaNo.grid(row = 0, column = 0)
    MovieCode = Button(screenScreening, text = "Movie Code", width = 15, fg = "white", bg = "#41c9a9")
    MovieCode.grid(row = 0, column = 1)
    TimeCode = Button(screenScreening, text = "Time Slot", width = 15, fg = "white", bg = "#41c9a9")
    TimeCode.grid(row = 0, column = 2)

    dbcur.execute(commands.displayHall_Screenings())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenScreening, width = 15, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1
    print("//---___*Rapper*Ha*Sooyoung*___---//")

def dbStaff():
    screenStaff = Toplevel(gui)
    screenStaff.title("Staff Table")
    screenStaff.geometry("525x130")
    screenStaff.iconbitmap('images\\icon.ico')
    #tablehead
    StffID = Button(screenStaff, text = "Staff ID", width = 15, fg = "white", bg = "#41c9a9")
    StffID.grid(row = 0, column = 0)
    FName = Button(screenStaff, text = "First Name", width = 15, fg = "white", bg = "#41c9a9")
    FName.grid(row = 0, column = 1)
    LName = Button(screenStaff, text = "Last Name", width = 15, fg = "white", bg = "#41c9a9")
    LName.grid(row = 0, column = 2)
    StffPass = Button(screenStaff, text = "Password", width = 15, fg = "white", bg = "#41c9a9")
    StffPass.grid(row = 0, column = 3)
    dbcur.execute(commands.displayStaff())
    i = 1 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(screenStaff, width = 15, fg = "black")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1
    print("//---___*Rapper*Ha*Sooyoung*___---//")

'''staff'''
def staffManipulation():
    print(userID.get())
    if userID.get() == '501101':
        screen6 = Toplevel(gui)
        screen6.title("Staff")
        screen6.geometry("320x400")
        screen6.iconbitmap('images\\icon.ico')
        changePass = Button(screen6, text = "Change Password", bg = "#41c9a9", width = 20, height = 1, font = ("AGFatumC", 15), command = staffChangePass)
        changePass.place(relx = 0.075, rely = 0.05)
        AddStaff = Button(screen6, text = "Add Staff", bg = "#41c9a9", width = 20, height = 1, font = ("AGFatumC", 15), command = staffInsert)
        AddStaff.place(relx = 0.075, rely = 0.20)
        updateName = Button(screen6, text = "Update Name", bg = "#41c9a9", width = 20, height = 1, font = ("AGFatumC", 15), command = staffUpdate)
        updateName.place(relx = 0.075, rely = 0.35)
        StaffButton = Button(screen6, text = "Staff Table", bg = "#41c9a9", width = 20, height = 1, font = ("AGFatumC", 15), command = dbStaff)
        StaffButton.place(relx = 0.075, rely = 0.50)
        LogOut = Button(screen6, text = "Log Out", bg = "#41c9a9", width = 20, height = 1, font = ("AGFatumC", 15), command = LogoutCMD)
        LogOut.place(relx = 0.075, rely = 0.65)
    elif userID.get() != '501101':
        screen6 = Toplevel(gui)
        screen6.title("Ticket")
        screen6.geometry("320x400")
        screen6.iconbitmap('images\\icon.ico')
        changePass = Button(screen6, text = "Change Password", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = staffChangePass)
        changePass.place(relx = 0.075, rely = 0.08)
        updateName = Button(screen6, text = "Update Name", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = staffUpdate)
        updateName.place(relx = 0.075, rely = 0.28)
        LogOut = Button(screen6, text = "Log Out", bg = "#41c9a9", width = 20, height = 2, font = ("AGFatumC", 15), command = LogoutCMD)
        LogOut.place(relx = 0.075, rely = 0.48)
    else:
        insertFeedback = Label(screenDelete, text = "Unexpected error.", fg = "#c40000", font = ("AGFatumC", 15))
        insertFeedback.pack()
        print("//---___*Rapper*Ha*Sooyoung*___---//") 

def staffChangePass():
    global screenStaffPass
    global CurrentPass
    global NewPass
    global CurrentPass_entry
    global NewPass_entry

    screenStaffPass = Toplevel(gui)
    screenStaffPass.title("Change User Password")
    screenStaffPass.geometry("350x200")
    screenStaffPass.iconbitmap('images\\icon.ico')
    
    CurrentPass = StringVar()
    NewPass = StringVar()

    CurrentPass_entry = Entry(screenStaffPass, textvariable = CurrentPass, show = bullet)
    CurrentPass_entry.grid(row = 0, column = 1, padx = 20)
    CurrentPass_label = Label(screenStaffPass, text = "Current Password")
    CurrentPass_label.grid(row = 0, column = 0)

    NewPass_entry = Entry(screenStaffPass, textvariable = NewPass, show = bullet)
    NewPass_entry.grid(row = 1, column = 1)
    NewPass_label = Label(screenStaffPass, text = "New Password")
    NewPass_label.grid(row = 1, column = 0)

    passSubmit = Button(screenStaffPass, text = "Submit", bg = "#41c9a9", command = staffChangePassCMD)
    passSubmit.grid(row = 2, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)

def staffChangePassCMD():
    userInfo = userID.get()
    passInfo = CurrentPass.get()
    NPassInfo = NewPass.get()
    values = []
    values.append(str(NPassInfo))
    values.append(int(userInfo))
    print(values)
    staffInfo = tuple(commands.selectStaff(userInfo))
    if str(staffInfo[1]) == str(passInfo):
        print(userInfo," ",passInfo," ",NPassInfo)
        commands.updateStaffPassword(values)
        insertFeedback = Label(screenStaffPass, text = "Password successfully changed.", fg = "#41c9a9", font = ("AGFatumC", 15))
        insertFeedback.grid(row = 3, column = 0, columnspan = 2)
        print("//---___*Rapper*Ha*Sooyoung*___---//")
    else:
        insertFeedback = Label(screenStaffPass, text = "Current password incorrect.", fg = "#c40000", font = ("AGFatumC", 15))
        insertFeedback.grid(row = 3, column = 0, columnspan = 2)
        print("//---___*Rapper*Ha*Sooyoung*___---//")
    
    CurrentPass_entry.delete(0, END)
    NewPass_entry.delete(0, END)

def staffInsert():
    global screenSInsert
    screenSInsert = Toplevel(gui)
    screenSInsert.title("Add Staff")
    screenSInsert.geometry("300x200")
    screenSInsert.iconbitmap('images\\icon.ico')
    
    global SFName
    global SLName
    global SFName_entry
    global SLName_entry

    SFName = StringVar()
    SLName = StringVar()
    SPass = StringVar()

    SFName_entry = Entry(screenSInsert, textvariable = SFName)
    SFName_entry.grid(row = 0, column = 1, padx = 20)
    SFName_label = Label(screenSInsert, text = "First Name")
    SFName_label.grid(row = 0, column = 0)
    
    SLName_entry = Entry(screenSInsert, textvariable = SLName)
    SLName_entry.grid(row = 1, column = 1)
    SLName_label = Label(screenSInsert, text = "Last Name")
    SLName_label.grid(row = 1, column = 0)
    
    ticketSubmit = Button(screenSInsert, text = "Submit", bg = "#41c9a9", command = staffInsertCMD)
    ticketSubmit.grid(row = 2, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)

def staffInsertCMD():
    values = []
    values.append(SFName.get())
    values.append(SLName.get())
    values.append("")
    print(values)
    try:
        commands.addStaff(values)
        insertFeedback = Label(screenSInsert, text = "Staff successfully added.", fg = "#41c9a9", font = ("AGFatumC", 15))
        insertFeedback.grid(row = 3, column = 0, columnspan = 2)
        print("//---___*Rapper*Ha*Sooyoung*___---//")
    except mysql.connector.errors.IntegrityError:
        insertFeedback = Label(screenSInsert, text = "Unexpected error.", fg = "#c40000", font = ("AGFatumC", 15))
        insertFeedback.grid(row = 3, column = 0, columnspan = 2)
        print("//---___*Rapper*Ha*Sooyoung*___---//")

    SFName_entry.delete(0, END)
    SLName_entry.delete(0, END)

def staffUpdate():
    global screenSUpdate
    screenSUpdate = Toplevel(gui)
    screenSUpdate.title("Update Name")
    screenSUpdate.geometry("300x200")
    screenSUpdate.iconbitmap('images\\icon.ico')
    
    global USFName
    global USLName
    global USPass
    global USFName_entry
    global USLName_entry
    global USPass_entry

    USFName = StringVar()
    USLName = StringVar()
    USPass = StringVar()

    USFName_entry = Entry(screenSUpdate, textvariable = USFName)
    USFName_entry.grid(row = 0, column = 1, padx = 20)
    USFName_label = Label(screenSUpdate, text = "First Name")
    USFName_label.grid(row = 0, column = 0)
    
    USLName_entry = Entry(screenSUpdate, textvariable = USLName)
    USLName_entry.grid(row = 1, column = 1)
    USLName_label = Label(screenSUpdate, text = "Last Name")
    USLName_label.grid(row = 1, column = 0)

    USPass_entry = Entry(screenSUpdate, textvariable = USPass)
    USPass_entry.grid(row = 2, column = 1)
    USPass_label = Label(screenSUpdate, text = "Password")
    USPass_label.grid(row = 2, column = 0)
    
    updateSubmit = Button(screenSUpdate, text = "Submit", bg = "#41c9a9", command = staffUpdateCMD)
    updateSubmit.grid(row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)

def staffUpdateCMD():
    values1 = []
    values2 = []

    values1.append(str(USFName.get()))
    values1.append(int(userID.get()))
    values2.append(str(USLName.get()))
    values2.append(int(userID.get()))

    print(values1," ",values2)
    staffInfo = tuple(commands.selectStaff(int(userID.get())))
    if str(staffInfo[1]) == str(USPass.get()):
        try:
            commands.updateStaff_FName(values1)
            commands.updateStaff_LName(values2)
            insertFeedback = Label(screenSUpdate, text = "Name successfully updated.", fg = "#41c9a9", font = ("AGFatumC", 15))
            insertFeedback.grid(row = 4, column = 0, columnspan = 2)
            print("//---___*Rapper*Ha*Sooyoung*___---//")
        except mysql.connector.errors.IntegrityError:
            insertFeedback = Label(screenSUpdate, text = "Unexpected error.", fg = "#c40000", font = ("AGFatumC", 15))
            insertFeedback.grid(row = 4, column = 0, columnspan = 2)
            print("//---___*Rapper*Ha*Sooyoung*___---//")
    else:
        insertFeedback = Label(screenSUpdate, text = "Password incorrect.", fg = "#c40000", font = ("AGFatumC", 15))
        insertFeedback.grid(row = 4, column = 0, columnspan = 2)
        print("//---___*Rapper*Ha*Sooyoung*___---//")
    
    USFName_entry.delete(0, END)
    USLName_entry.delete(0, END)
    USPass_entry.delete(0, END)

#login
def Login():
    userInfo = userID.get()
    passInfo = password.get()

    try:
        val = int(userInfo)
        checkLog = commands.checkStaff(userInfo)
        print(userInfo," ",passInfo," ",type(checkLog[0]))
        if int(checkLog[0]) == 1:
            staffInfo = tuple(commands.selectStaff(userInfo))
            if str(staffInfo[1]) == str(passInfo):
                print("Insert main program screen")
                screen1.destroy()
                mainProgram(userInfo)
            else:
                print("Incorrect password")
                screen2 = Toplevel(gui)
                screen2.title("Log In")
                screen2.geometry("300x150")
                screen2.iconbitmap('images\\icon.ico')
                Label(screen2, text = "", height = 3).pack()
                Label(screen2, text = "Incorrect password.", fg = "#c40000", font = ("AGFatumC", 15)).pack()
        else:
            print("User does not exist")
            screen2 = Toplevel(gui)
            screen2.title("Log In")
            screen2.geometry("300x150")
            screen2.iconbitmap('images\\icon.ico')
            Label(screen2, text = "", height = 3).pack()
            Label(screen2, text = "User does not exist.", fg = "#c40000", font = ("AGFatumC", 15)).pack()
    except ValueError:
        print("Invalid Staff ID")
        screen2 = Toplevel(gui)
        screen2.title("Log In")
        screen2.geometry("300x150")
        screen2.iconbitmap('images\\icon.ico')
        Label(screen2, text = "", height = 3).pack()
        Label(screen2, text = "Invalid Staff ID", fg = "#c40000", font = ("AGFatumC", 15)).pack()

    userEntry.delete(0, END)
    passEntry.delete(0, END)

def LoginGUI():
    global screen1
    screen1 = Toplevel(gui)
    screen1.title("Log In")
    screen1.geometry("300x300")
    screen1.iconbitmap('images\\icon.ico')
    
    global userID
    global password
    global userEntry
    global passEntry
    global bullet 

    userID = StringVar()
    password = StringVar()

    Label(screen1, text = "",height = 2).pack()
    Label(screen1, text = "Staff ID", bg = "#41c9a9", width = 250, height = 2, font = ("AGFatumC", 15)).pack()
    userEntry = Entry(screen1, textvariable = userID)
    userEntry.pack()
    Label(screen1, text = "Password", bg = "#41c9a9", width = 250, height = 2, font = ("AGFatumC", 15)).pack()
    bullet = "\u2022"
    passEntry = Entry(screen1, textvariable = password, show = bullet)
    passEntry.pack()
    Label(screen1, text = "",height = 2).pack()
    Button(screen1, text = "Login", bg = "#41c9a9", height = 1, width = 25, command = Login).pack()
    Label(screen1, text = "",height = 2).pack()

def LogoutCMD():
    gui.destroy()
    startScreen()

#main
startScreen()