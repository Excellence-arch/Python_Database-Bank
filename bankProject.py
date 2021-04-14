import mysql.connector
import time
import sys
import random
class ATM:
	def __init__(self):
		self.connection()
		self.option()

	def connection(self):
		self.mycon = mysql.connector.connect(host='localhost', passwd='', user='root', database='bank')
		self.mycursor = self.mycon.cursor()
		# self.mycursor.execute('ALTER TABLE Customers ADD UNIQUE(Account_Number)')
		# self.mycursor.execute('CREATE TABLE Customers (Account_Number VARCHAR(20), First_Name VARCHAR(20), Last_Name VARCHAR(20), Sex VARCHAR(7), Phone_Number VARCHAR(12), Address VARCHAR(30), Account_Pin INT(4), Amount INT(20))') 

	def option(self):
		print('''Welcome to my bank
				1. Register
				2. Transaction
				3. Quit''')
		self.user = input('Enter your choice > ')
		if self.user == '1':
			self.Register()
		elif self.user == '2':
			self.login()
		elif self.user == '3':
			self.quit()
		else:
			print('Invalid Option')
			self.option()


	def Register(self):
		detail = ['fName', 'lName', 'sex', 'phone', 'adres', 'pin']
		req = ['First Name', 'Last Name', 'Sex', 'Phone', 'Address', 'Account Pin']
		for i in range(len(req)):
			detail[i] = input('Eneter your ' + req[i] + ">>> ")
		accNo = '101' + str(random.randint(0, 9000000))
		amount = 0
		myQuery = 'INSERT INTO Customers(Account_Number, First_Name, Last_Name, Sex, Phone_Number, Address, Account_Pin, Amount) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
		myVal = (accNo, detail[0], detail[1], detail[2], detail[3], detail[4], detail[5], amount)
		self.mycursor.execute(myQuery, myVal)
		self.mycon.commit()
		print(self.mycursor.rowcount, """registration is successful.\nYour account number is""" + accNo)
		self.option()

	def login(self):
		self.transact = ['1. withdraw', '2. Deposit', '3. Transfer', '4. Check Balance', '5. Cancel']
		self.accNo = input('Enter your account number >>>')
		self.pin = input('Enter your account pin >>>')
		query = 'SELECT * FROM Customers WHERE Account_Number = %s and Account_Pin = %s'
		val = (self.accNo, self.pin)
		self.mycursor.execute(query, val)
		self.record = self.mycursor.fetchall()
		if self.record:
			print('Welcome Dear ' + self.record[0][2] + ' ' + self.record[0][1])
			time.sleep(2)
			self.transaction()
		else:
			print('Dear Customer, You have no account with us')


	def transaction(self):
		for i in self.transact:
			print(i)
		self.userInput = input('Enter your choice >>>> ')
		if self.userInput == '1':
			self.withdraw()
		elif self.userInput == '2':
			self.deposit()
		elif self.userInput == '3':
			self.transfer()
		elif self.userInput == '4':
			self.checkBalance()
		elif self.userInput == '5':
			self.option()
		else:
			print('Invalid Option')
			self.transaction()


	def withdraw(self):
		self.yourAmount = {'1' : 1000, '2' : 2000, '3' : 5000, '4' :10000, '5' : 20000}
		for key, val in self.yourAmount.items():
			print(key, val)
		choice = input('Enter your choice >>>')
		if self.record[0][7] < self.yourAmount[choice]:
			print('Insufficient fund')
		else:
			newBal = self.record[0][7] - self.yourAmount[choice]
			query = 'UPDATE Customers SET Amount = %s WHERE Account_Number = %s'
			my_val = (newBal, self.record[0][0])
			self.mycursor.execute(query, my_val)
			self.mycon.commit()
			print('Please take out your cash of {}'.format(self.yourAmount[choice]))
			time.sleep(2)
			self.transaction()

	def deposit(self):
		yourAmount = {'1' : 1000, '2' : 2000, '3' : 5000, '4' :10000, '5' : 20000}
		for key, val in yourAmount.items():
			print(key, val)
		choice = input('Enter your choice >>>>')
		newBal = self.record[0][7] + yourAmount[choice]
		query = 'UPDATE Customers SET Amount = %s WHERE Account_Number = %s'
		my_val = (newBal, self.record[0][0])
		self.mycursor.execute(query, my_val)
		self.mycon.commit()
		print('Your new account balance is {}'.format(newBal))
		time.sleep(2)
		self.transaction()

	def transfer(self):
			tAmount = int(input('How much do you want to transfer >>>'))
			tAccount = int(input("Enter beneficiary's account number >>>>"))
			if self.record[0][7] > tAmount:
				newQuery = 'SELECT * FROM Customers WHERE Account_Number = %s'
				newVal = (tAccount,)
				rg = (newQuery, newVal)
				self.mycursor.execute(newQuery, newVal)
				self.newRecord = self.mycursor.fetchall()
				if self.newRecord:
					userBal = self.record[0][7] - tAmount
					benBal = self.newRecord[0][7] + tAmount
					query1 = 'UPDATE Customers SET Amount = %s WHERE Account_Number = %s'
					val1 = (userBal, self.record[0][0])
					query2 = 'UPDATE Customers SET Amount = %s WHERE Account_Number = %s'
					val2 = (benBal, self.newRecord[0][0])
					self.mycursor.execute(query1, val1)
					self.mycursor.execute(query2, val2)
					self.mycon.commit()
					time.sleep(2)
					print('You have successfully sent {} to {} {}'.format(tAmount, self.newRecord[0][1], self.newRecord[0][2]))
					time.sleep(2)
					self.transaction()
				else:
					print('Wrong Account number')


	def checkBalance(self):
		print('Your account balance is {}'.format(self.record[0][7]))
		time.sleep(2)
		self.transaction()


	def quit(self):
		sys.exit()

myAtm = ATM()