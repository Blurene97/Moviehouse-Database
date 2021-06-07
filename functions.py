import commands
import functions
import os
import time
import tkinter
import sys
def start_up(dbcursur):
    dbcur = dbcursur
    print("Movie House Database")
    print("[1] Generate a Ticket")
    print("[2] View screening movies")
    print("[3] Log-In different user")
    print("[4] Display database tables")
    print("[5] More")
    start_choice = input()
    os.system('cls')
    if start_choice == '1':
        ticketManipulation(dbcur)
    elif start_choice == '2':
        dbcur.execute(commands.displayScreeningSched())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            start_up(dbcur)
        else:
            os.system('cls')
            start_up(dbcur)
    elif start_choice == '3':
        print('display **prices table**')
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            start_up(dbcur)
        else:
            os.system('cls')
            start_up(dbcur)
    elif start_choice == '4':
        dbcur.execute(commands.showTables())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            start_up(dbcur)
        else:
            os.system('cls')
            start_up(dbcur)
    elif start_choice == '5':
        dbcur.execute(display_table(dbcur))
    else:
        print('Invalid input!')
        time.sleep(2)
        os.system('cls')
        start_up(dbcur)
        
def display_table(dbcursur):
    dbcur = dbcursur
    print("Select Table to display")
    print("[1] Cinema Halls")
    print("[2] Movies Showing")
    print("[3] Screening times")
    print("[4] Ticket Logs")
    print("[5] Cinema Screening Schedule")
    print("[6] Staff")
    print("[7] Back to previous page")
    choiceTable = input("Which Table: ")
    if choiceTable == '1':
        dbcur.execute(commands.displayCinema_Hall())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            display_table(dbcur)
        else:
            os.system('cls')
            display_table(dbcur)
    elif choiceTable == '2':
        dbcur.execute(commands.displayMovies())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            display_table(dbcur)
        else:
            os.system('cls')
            display_table(dbcur)
    elif choiceTable == '3':
        dbcur.execute(commands.displayScreening())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            display_table(dbcur)
        else:
            os.system('cls')
            display_table(dbcur)
    elif choiceTable == '4':
        dbcur.execute(commands.displayTicket_Logs())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            display_table(dbcur)
        else:
            os.system('cls')
            display_table(dbcur)
    elif choiceTable == '5':
        dbcur.execute(commands.displayHall_Screenings())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            display_table(dbcur)
        else:
            os.system('cls')
            display_table(dbcur)
    elif choiceTable == '6':
        dbcur.execute(commands.displayStaff())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(2)
        exit = input("Press any key to go back.")
        if exit == 'e' or 'E':
            os.system('cls')
            display_table(dbcur)
        else:
            os.system('cls')
            display_table(dbcur)
    elif choiceTable == '7':
        os.system('cls')
        start_up(dbcur)
    else:
        os.system('cls')
        print("Invalid Input!")
        time.sleep(2)
        display_table(dbcur)

def ticketManipulation(dbcur):
    print("[1] Existing ticket")
    print("[2] Add ticket")
    ticketCMD = input()
    if ticketCMD == '1':
        dbcur.execute(commands.displayTicket_Logs())
        TableLogs = dbcur.fetchall()
        for i in TableLogs:
            print(i)
        time.sleep(1)
        ticketPULL = int(input("Ticket Number: "))
        commands.selectTicket(ticketPULL)
        exitCMD = input("Press 'B' to go back...")
        if exitCMD == 'b' and 'B':
            ticketManipulation(dbcur)
        else:
            os.system('cls')
            print("Invalid input.")
            time.sleep(1)
            print("Going back...")
            time.sleep(1)
            start_up(dbcur)
            os.system('cls')
    elif ticketCMD == '2':
        values = []
        values.append(input(print("Staff ID: ")))
        values.append(input(print("Movie Code: ")))
        values.append(input(print("Cinema No.: ")))
        values.append(input(print("Seat No.: ")))
        values.append(input(print("Screening Code: ")))
        commands.insertTicket(values)
        print("Input Successful.")
        time.sleep
        exitCMD = input("Press 'B' to go back...")
        os.system('cls')
        if exitCMD == 'b' and 'B':
            os.system('cls')
            ticketManipulation(dbcur)
        else:
            os.system('cls')
            print("Invalid input.")
            time.sleep(2)
            print("Going back...")
            time.sleep(2)
            start_up(dbcur)
            os.system('cls')
    elif ticketCMD == 'b' and 'B':
        os.system('cls')
        start_up(dbcur)
    else:
        print("Invalid input.")
        os.system('cls')
        ticketManipulation(dbcur)