#Account class containing account info
class Account(object):
    def __init__(self, login, password, balance=0):
        self.checkString(login)
        self.login = login
        self.checkPassword(password)
        self.password = password
        self.balance = float(balance)

    #Method to check if username is valid
    def checkString(self, text):
        if len(text) <= 0:
            raise Exception()
        letters='qwertyuiopasdfghjklzxcvbnm_'
        num = '0123456789'
        for letter in text:
            if letter not in letters and letter not in num:
                raise Exception()
        
    def checkPassword(self,text):
        if len(text) <= 0:
            raise Exception
    #Overriding compare to check if username is already taken
    def __eq__(self, other):
        if self.login == other.login:
            return True
        else:
            return False

    
    def addBalance(self, ammount):
        #Checking if ammount doesn't have decimal places past 2 or is lower or equal to 0
        if ammount <= 0 or ((ammount*1000)%10) != 0:
            raise Exception()
        else:
            self.balance += ammount
    
    
    def withdraw(self,ammount):
        #Bank account can't have negative balance
        if self.balance- ammount < 0:
            raise Exception()
        else:
            self.balance -= ammount

    def getBalance(self):
        return self.balance
    
    def __str__(self) -> str:
        return self.login + ' ' + self.password + ' ' +str(self.balance)
    
class Bank(object):
    # Bank contains list of accounts
    def __init__(self,accounts=[]):
        self.accounts = accounts

    def addAccount(self,account):
        self.accounts.append(account)

    def transferMoney(self,account1,account2,ammount):
        self.accounts[account1].withdraw(ammount)
        self.accounts[account2].addBalance(ammount)

    def returnIndexOfUsername(self,username):
        i = 0
        for account in self.accounts:
            if account.login == username:
                return i
            i+= 1
        return -1

    #Loading bank from file
    def loadAccounts(self, fileName):
        f = open(f'banks/{fileName}','r')
        lines = f.readlines()

        for line in lines:
            info = line.split(' ')
            if len(info) < 2 or len(info) > 3:
                raise Exception()
            if info[-1][-1] == '\n':
                info[-1] = info[-1][:-1]
            try:
                new = Account(info[0],info[1],float(info[2]))
            except:
                new = Account(info[0],info[1])
            
            flag = True
            for account in self.accounts:
                if account == new:
                    flag = False
                    break
            if flag: 
                self.accounts.append(new)

    #Exporting bank to file
    def exportAccounts(self,fileName):
        f = open(f'banks/{fileName}','w')
        for item in self.accounts:
            if item == self.accounts[-1]:
                mystr = item.login + ' ' + item.password + ' ' + str(item.balance)
            else:
                mystr = item.login + ' ' + item.password + ' ' + str(item.balance) + '\n'
            f.write(mystr)

bank = Bank()

