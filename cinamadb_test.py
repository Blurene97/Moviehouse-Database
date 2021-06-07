from tkinter import *
import mysql.connector
import commands
#connect to db
dbcon = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "moviehousedb",
    port = 3306
)
if type(1) == type(8):
    print("ok goods")
else:
    print("flop")
def selectStaff(userID):
    insertCMD = "SELECT * FROM staff WHERE staff_ID = %s"
    dbcur.execute(insertCMD % userID)
    TableLogs = dbcur.fetchall()
    for i in TableLogs:
        userID = i[0]
        userPass = i[3]
        staffName = i[1]
    return userID, userPass, staffName
#Displaying Table in Tkinter
    dbcur.execute(commands.displayScreeningSched())
    i = 0 
    TableLogs = dbcur.fetchall()
    for a in TableLogs:
        for j in range(len(a)):
            e = Entry(mainscreen, width = 15, fg = "#41c9a9")
            e.grid(row = i, column = j)
            e.insert(END, a[j]) 
        i = i + 1

#scroll bar
#mainframe
gui = Tk()
screenFrame = Frame(gui)
screenFrame.pack(fill = BOTH, expand = 1)
#canvas
screenCanvas = Canvas(screenFrame)
screenCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
gui.mainloop()
#scrollbar
windowSlider = ttk.Scrollbar(screenFrame, orient = VERTICAL, command = screenCanvas.yview)
windowSlider.pack(side = RIGHT, fill = Y)
#configure canvas
screenCanvas.configure(yscrollcommand = windowSlider.set)
screenCanvas.bind('<Configure>', lambda e: screenCanvas.configure(scrollregion = screenCanvas.bbox("all")))
#second frame
screenFrame2 = Frame(screenCanvas)
#window
screenCanvas.create_window((0,0), window = screenFrame2, anchor = "nw")



print(dbcon)
dbcur = dbcon.cursor()
userID = input()
TableContent = tuple(selectStaff(userID))
print(TableContent[0], " ", TableContent[1]," ", TableContent[2])
#close db
dbcon.close