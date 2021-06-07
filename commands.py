import mysql.connector
import commands
import functions
import os
import time
import sys
dbcon = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "moviehousedb",
    port = 3306,
    autocommit = True
    )

dbcur = dbcon.cursor()
#insert queries
def insertTicket(valuesCMD):
    insertCMD = "INSERT INTO ticket(staff_ID, code_name, cinema_no, seat_no, sched_code) VALUES (%s, %s, %s, %s, %s)"
    dbcur.execute(insertCMD,valuesCMD)
    dbcon.commit()

def insertMovies(valuesCMD):
    insertCMD = "INSERT INTO movie(code_name, title, movie_description) VALUES ('%s', '%s','%s');"
    dbcur.execute(insertCMD,valuesCMD)
    dbcon.commit()

#display queries
def showTables():
    insertCMD = "SHOW TABLES;"
    return insertCMD

def displayCinema_Hall():
    insertCMD = "SELECT * FROM cinema_hall"
    return insertCMD

def displayMovies():
    insertCMD = "SELECT * FROM movie"
    return insertCMD

def displayScreening():
    insertCMD = "SELECT * FROM showtime"
    return insertCMD

def displayTicket_Logs():
    insertCMD = "SELECT * FROM ticket"
    return insertCMD

def displayHall_Screenings():
    insertCMD = "SELECT * FROM hall_screenings"
    return insertCMD

def displayStaff():
    insertCMD = "SELECT * FROM staff"
    return insertCMD

def displayScreeningSched():
    insertCMD = "SELECT b.show_start, b.show_end, a.time_slot, a.CinemaHall_no, a.movie_code, c.title FROM hall_screenings a JOIN showtime b ON a.time_slot = b.sched_code JOIN movie c ON a.movie_code = c.code_name ORDER BY b.show_start;"
    return insertCMD

def displayMoviesSched(valuesCMD):
    insertCMD = "SELECT a.movie_code, c.title, a.CinemaHall_no, b.show_start, b.show_end, a.time_slot FROM hall_screenings a JOIN showtime b ON a.time_slot = b.sched_code JOIN movie c ON a.movie_code = c.code_name WHERE a.movie_code = '%s' ORDER BY b.show_start"
    dbcur.execute(insertCMD % valuesCMD)
    TableLogs = dbcur.fetchall()
    return TableLogs

#delete queries
def deleteTicket(valuesCMD):
    insertCMD = "DELETE FROM ticket WHERE ticket_no = %s"
    dbcur.execute(insertCMD % valuesCMD)
    dbcon.commit()

#update queries
def updateStaffPassword(valuesCMD):
    insertCMD = "UPDATE staff SET staff_password = %s WHERE staff_ID = %s"
    dbcur.execute(insertCMD,valuesCMD)
    dbcon.commit()

def updateStaff_FName(valuesCMD):
    insertCMD = "UPDATE staff SET staff_fname = %s WHERE staff_ID = %s"
    dbcur.execute(insertCMD,valuesCMD)
    dbcon.commit()

def updateStaff_LName(valuesCMD):
    insertCMD = "UPDATE staff SET staff_lname = %s WHERE staff_ID = %s"
    dbcur.execute(insertCMD,valuesCMD)
    dbcon.commit()

def addStaff(valuesCMD):
    insertCMD = "INSERT INTO staff(Staff_fname, Staff_lname, staff_password) VALUES ( %s, %s, %s)"
    dbcur.execute(insertCMD,valuesCMD)
    dbcon.commit()

def delStaff(valuesCMD):
    insertCMD = "DELETE FROM staff WHERE staff_ID = %s"
    dbcur.execute(insertCMD % valuesCMD)
    dbcon.commit()

#others
def selectTicket(ticketPULL):
    insertCMD = "SELECT a.ticket_no, a.code_name AS 'movie_code', c.title, a.sched_code, b.show_start, b.show_end, a.seat_no FROM ticket a JOIN showtime b ON a.sched_code = b.sched_code AND a.cinema_no = b.hall_no JOIN movie c ON a.code_name = c.code_name WHERE ticket_no = %s"
    dbcur.execute(insertCMD % ticketPULL)
    TableLogs = dbcur.fetchall()
    return TableLogs

def checkStaff(userID):
    insertCMD = "SELECT COUNT(*) FROM staff WHERE staff_ID = %s;"
    dbcur.execute(insertCMD % userID)
    TableLogs = dbcur.fetchone()
    return TableLogs

def checkTicket(ticket_no):
    insertCMD = "SELECT COUNT(*) FROM ticket WHERE ticket_no = %s;"
    dbcur.execute(insertCMD % ticket_no)
    TableLogs = dbcur.fetchone()
    return TableLogs

def selectStaff(userID):
    insertCMD = "SELECT * FROM staff WHERE staff_ID = %s"
    dbcur.execute(insertCMD % userID)
    TableLogs = dbcur.fetchall()
    for i in TableLogs:
        userID = i[0]
        userPass = i[3]
        staffName = i[1]
    return userID, userPass, staffName