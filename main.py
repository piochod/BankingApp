'''
    Bank App by Piotr Chodkowski SGGW
    Main functionalities:
        -Adding accounts to a bank
        -Logging into accounts
        -Depositing, withdrawing money from account
        -Transfering money between accounts
        -Exporting bank into a file
        -Loading bank from a file
    Loading/Exporting to files rules:
        -every account consist of username(required), password(required) and balance(optional)
        -every account is written in one line every atribute seperated by space
        -accounts can't have the same usernames
'''


import customtkinter
from CTkMessagebox import CTkMessagebox
from classes import *

#Making a window
root = customtkinter.CTk()
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=60,fill='both',expand=True, anchor = 'center')

#Page to choose logging in or creating an account
def choicePage(bank,frame):
    makeStandardWindow()

    #Making sure window is cleared
    for widget in frame.winfo_children():
        widget.destroy()
    
    label = customtkinter.CTkLabel(master = frame, text = 'Welcome to Bank XYZ', font = ('Arial',24))
    label.pack(padx= 12,pady = 12)

    button1 = customtkinter.CTkButton(master = frame, text='Login', command= lambda: loginPage(bank,frame), anchor = 'CENTER')
    button1.pack(padx=12,pady=12)
    
    button2 = customtkinter.CTkButton(master = frame, text='Register', command= lambda: registerPage(bank,frame), anchor = 'CENTER')
    button2.pack(padx=12,pady=12)

    button3 = customtkinter.CTkButton(master = frame, text='Load from file', command= lambda: loadBank(bank,frame), anchor = 'CENTER')
    button3.pack(padx=12,pady=12)
    
    button4 = customtkinter.CTkButton(master = frame, text='Export to file', command= lambda: exportBank(bank,frame), anchor = 'CENTER')
    button4.pack(padx=12,pady=12)      
    
    root.mainloop()

#Loading from file
def loadBank(bank, frame):
    for widget in frame.winfo_children():
        widget.destroy()
    label = customtkinter.CTkLabel(master = frame, text = 'Load from file', font = ('Arial',24))
    label.pack(padx= 12,pady = 12)

    entry = customtkinter.CTkEntry(master=frame,placeholder_text="File Name")
    entry.pack(pady=12,padx=10)

    button1 = customtkinter.CTkButton(master = frame, text='Load', command= lambda: loadBankAction(bank,frame,entry), anchor = 'CENTER')
    button1.pack(padx=12,pady=12)

    button2=customtkinter.CTkButton(master=frame,text='Back',command=lambda: choicePage(bank,frame))
    button2.pack(pady=12,padx=10)

def loadBankAction(bank,frame,entry):
    try:
        bank = Bank()
        bank.loadAccounts(entry.get())
        CTkMessagebox(icon='check',message='Succesfully loaded from file!',option_1='OK')
        choicePage(bank,frame)
    except:
        CTkMessagebox(title='Error',message=f"Error reading from a file", icon='cancel')
        entry.delete(0,customtkinter.END)


def exportBank(bank,frame):
    for widget in frame.winfo_children():
        widget.destroy()
    label = customtkinter.CTkLabel(master = frame, text = 'Export to file', font = ('Arial',24))
    label.pack(padx= 12,pady = 12)

    entry = customtkinter.CTkEntry(master=frame,placeholder_text="File Name")
    entry.pack(pady=12,padx=10)

    button1 = customtkinter.CTkButton(master = frame, text='Export', command= lambda: exportBankAction(bank,frame,entry), anchor = 'CENTER')
    button1.pack(padx=12,pady=12)

    button2=customtkinter.CTkButton(master=frame,text='Back',command=lambda: choicePage(bank,frame))
    button2.pack(pady=12,padx=10)

def exportBankAction(bank,frame,entry):
    try:
        bank.exportAccounts(entry.get())
        CTkMessagebox(icon='check',message='Succesfully exported to file!',option_1='OK')
        choicePage(bank,frame)
    except:
        CTkMessagebox(title='Error',message=f"Something went wrong", icon='cancel')
        entry.delete(0,customtkinter.END)

def registerPage(bank,frame):
    for widget in frame.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(master = frame, text = 'Sign Up for Bank XYZ', font = ('Arial',24))
    label.pack(padx= 12,pady = 12)

    entry1 = customtkinter.CTkEntry(master=frame,placeholder_text="Username")
    entry1.pack(pady=12,padx=10)

    entry2 = customtkinter.CTkEntry(master=frame,placeholder_text="Password",show='*')
    entry2.pack(pady=12,padx=10)

    entry3 = customtkinter.CTkEntry(master=frame,placeholder_text="Repeat Password",show='*')
    entry3.pack(pady=12,padx=10)

    button1 = customtkinter.CTkButton(master = frame, text='Register', command= lambda: checkEntry(entry1,entry2,entry3,bank,frame), anchor = 'CENTER')
    button1.pack(padx=12,pady=12)

    button2=customtkinter.CTkButton(master=frame,text='Back',command=lambda: choicePage(bank,frame))
    button2.pack(pady=12,padx=10)

    root.mainloop() 

#Checking if register credentials are valid
def checkEntry(entry1,entry2,entry3,bank,frame):
    #Checking if password box is empty
    if len(entry2.get()) == 0:
        CTkMessagebox(title='Error',message=f"Password cannot be empty", icon='cancel')
        entry1.delete(0,customtkinter.END)
        entry2.delete(0,customtkinter.END)
        entry3.delete(0,customtkinter.END)
    
    #Checking if passwords match
    elif entry2.get() != entry3.get():
        CTkMessagebox(title='Error',message=f"Passwords don't match", icon='cancel')
        entry1.delete(0,customtkinter.END)
        entry2.delete(0,customtkinter.END)
        entry3.delete(0,customtkinter.END)
    
    else:
        try:
            #Checking if username isn't already taken
            new = Account(entry1.get(),entry2.get())

            flag = True
            for account in bank.accounts:
                if new == account:
                    CTkMessagebox(title='Error',message=f"Username already taken!", icon='cancel')
                    flag = False
                    entry1.delete(0,customtkinter.END)
                    entry2.delete(0,customtkinter.END)
                    entry3.delete(0,customtkinter.END)
                    break

            if flag:
                bank.addAccount(new)
                CTkMessagebox(icon='check',message='Account added succesfully! You can login now',option_1='OK')
                loginPage(bank,frame)
        #Throwing an error messagebox if username isn't valid
        except:
            CTkMessagebox(title='Error',message=f"Username must contain at least 1 character and can only consist of letters, numbers and underscore", icon='cancel')
            entry1.delete(0,customtkinter.END)
            entry2.delete(0,customtkinter.END)
            entry3.delete(0,customtkinter.END)

#Creating a window
def makeStandardWindow():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    root.title('Bank App')
    root.geometry('600x360')

#Checking if credentials match any account in a Bank
def login(entry1,entry2,bank,frame):
    count = 0
    for account in bank.accounts:
        if entry1.get() == account.login and entry2.get() == account.password:
            logged(bank,frame,bank.accounts.index(account))
            count +=1
            break
    
    if count == 0:
        CTkMessagebox(title='Error',message='No account matches these credentials', icon='cancel')
        entry1.delete(0,customtkinter.END)
        entry2.delete(0,customtkinter.END)

#Adding balance to an account
def deposit(bank,frame,index):
    for widget in frame.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(master=frame,text=f'Deposit to: {bank.accounts[index].login}',font=('Arial',24))
    label.pack(pady = 12, padx = 10)

    entry1 = customtkinter.CTkEntry(master=frame,placeholder_text="Ammount")
    entry1.pack(pady=12,padx=10)

    button1=customtkinter.CTkButton(master=frame,text='Deposit',command=lambda: depositAction(bank,frame,index,entry1.get(),entry1))
    button1.pack(pady=12,padx=10)

    button2=customtkinter.CTkButton(master=frame,text='Back',command=lambda: logged(bank,frame,index))
    button2.pack(pady=12,padx=10)

    root.update()
    root.mainloop()

#Trying to update balance after depositing, checking if entry is valid
def depositAction(bank,frame,index,amm,entry):
    try:
        bank.accounts[index].addBalance(float(amm))
        CTkMessagebox(icon='check',message='Balance updated succesfully',option_1='OK')
        logged(bank,frame,index)
    except:
        CTkMessagebox(title='Error',message='Wrong ammount', icon='cancel')
        entry.delete(0,customtkinter.END)

#Similar to depositing
def withdraw(bank,frame,index):
    for widget in frame.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(master=frame,text=f'Withdraw from: {bank.accounts[index].login}',font=('Arial',24))
    label.pack(pady = 12, padx = 10)

    entry1 = customtkinter.CTkEntry(master=frame,placeholder_text="Ammount")
    entry1.pack(pady=12,padx=10)

    button1=customtkinter.CTkButton(master=frame,text='Withdraw',command=lambda: withdrawAction(bank,frame,index,entry1.get(),entry1))
    button1.pack(pady=12,padx=10)

    button2=customtkinter.CTkButton(master=frame,text='Back',command=lambda: logged(bank,frame,index))
    button2.pack(pady=12,padx=10)

    root.update()
    root.mainloop()

#Similar to depositing
def withdrawAction(bank,frame,index,amm,entry):
    try:
        bank.accounts[index].withdraw(float(amm))
        CTkMessagebox(icon='check',message='Balance updated succesfully',option_1='OK')
        logged(bank,frame,index)
    except:
        CTkMessagebox(title='Error',message='Wrong ammount', icon='cancel')
        entry.delete(0,customtkinter.END)

#Transfering from accounts
def transfer(bank,frame,index):
    for widget in frame.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(master=frame,text=f'Transfering from: {bank.accounts[index].login}',font=('Arial',24))
    label.pack(pady = 12, padx = 10)
    
    entry1 = customtkinter.CTkEntry(master=frame,placeholder_text="Username of reciever")
    entry1.pack(pady=12,padx=10)

    entry2 = customtkinter.CTkEntry(master=frame,placeholder_text="Ammount")
    entry2.pack(pady=12,padx=10)

    button1=customtkinter.CTkButton(master=frame,text='Transfer',command=lambda: transferAction(bank,frame,index,entry1,entry2))
    button1.pack(pady=12,padx=10)

    button2=customtkinter.CTkButton(master=frame,text='Back',command=lambda: logged(bank,frame,index))
    button2.pack(pady=12,padx=10)

    root.update()
    root.mainloop()

def transferAction(bank,frame,index,entry1,entry2):
    #Checking if username exists
    index2 = bank.returnIndexOfUsername(entry1.get())
    if index2 == -1:
        CTkMessagebox(title='Error',message='Wrong username of reciever', icon='cancel')
        return
    if index2 == index:
        CTkMessagebox(title='Error',message="Can't transfer to yourself", icon='cancel')
        return
    try:
        bank.transferMoney(index, index2,float(entry2.get()))
        CTkMessagebox(icon='check',message='Transfer succesful',option_1='OK')
        logged(bank,frame,index)
    except:
        CTkMessagebox(title='Error',message='Wrong ammount', icon='cancel')
        entry1.delete(0,customtkinter.END)
        entry2.delete(0,customtkinter.END)


#Main page after logging in
def logged(bank,frame,index):
    for widget in frame.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(master=frame,text=f'Welcome {bank.accounts[index].login}!',font=('Arial',24))
    label.pack(pady = 12, padx = 10)

    label = customtkinter.CTkLabel(master=frame,text=f'Balance: {bank.accounts[index].getBalance()}',font=('Arial',20))
    label.pack(pady = 12, padx = 10)

    button1=customtkinter.CTkButton(master=frame,text='Deposit', command=lambda: deposit(bank,frame,index))
    button1.pack(pady=12,padx=10)

    button2=customtkinter.CTkButton(master=frame,text='Withdraw', command=lambda: withdraw(bank,frame,index))
    button2.pack(pady=12,padx=10)

    button3=customtkinter.CTkButton(master=frame,text='Transfer',command = lambda: transfer(bank, frame,index))
    button3.pack(pady=12,padx=10)

    button4=customtkinter.CTkButton(master=frame,text='Logout', command=lambda: choicePage(bank,frame))
    button4.pack(pady=12,padx=10)

    root.update()
    root.mainloop()


def loginPage(bank,frame):
    for widget in frame.winfo_children():
        widget.destroy()

    label = customtkinter.CTkLabel(master=frame,text='Login to Bank XYZ',font=('Arial',24))
    label.pack(pady = 12, padx = 10)

    entry1 = customtkinter.CTkEntry(master=frame,placeholder_text="Username")
    entry1.pack(pady=12,padx=10)

    entry2 = customtkinter.CTkEntry(master=frame,placeholder_text="Password",show='*')
    entry2.pack(pady=12,padx=10)

    button=customtkinter.CTkButton(master=frame,text='Login',command=lambda: login(entry1,entry2,bank,frame))
    button.pack(pady=12,padx=10)

    button4=customtkinter.CTkButton(master=frame,text='Back', command=lambda: choicePage(bank,frame))
    button4.pack(pady=12,padx=10)

    root.update()
    root.mainloop()


a,b,c = Account('a','b',123),Account('c','d'),Account('e','f',11231323)
bank = Bank([a,b,c])
choicePage(bank,frame)