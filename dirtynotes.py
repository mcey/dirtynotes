import os, termios, fcntl, sys
SOURCE_FILE = 'dictionaries.txt'

def displayMainMenu():
	exitState = 0;
	#dictionaries = loadDictionaries()
	menu = "(L)ist All Dictionaries\n(N)ew Dictionary\n(F)ind Dictionary\n(D)elete Dictionary\n(E)xit\n"
	while(not exitState):
		os.system('clear')
		print(menu)
		command = getPressedKey().upper()
		if command =='L':
			ListAllDictionaries()
		elif command == 'E':
			exitState = 1
			saveDictionaries()
		elif command == 'N':
			createNewDictionary()
		elif command == 'F':
			displayFindDictionaryScreen()
		elif command == 'D':
			showDeleteDictionaryScreen()


def ListAllDictionaries():
	menu = ("(O)pen Dictionary\n(D)elete Dictionary\n(M)ain Menu\n")
	os.system('clear')
	print(menu)
	for key in dictionaries.keys():
		print(key)
	command = getPressedKey().upper()

	if command == 'O':
		displayFindDictionaryScreen()
	elif command == 'D':
		showDeleteDictionaryScreen()
		ListAllDictionaries()



def getPressedKey():
	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	try:
	    while 1:
	        try:
	            c = sys.stdin.read(1)
	            return c
	        except IOError: pass
	finally:
	    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


def displayFindDictionaryScreen():
	dictionaryName = str(raw_input("Enter dictionary name: "))
	dictionary = findDictionary(dictionaryName)
	if dictionary == -1:
		print("{} not found".format(dictionaryName))
		getPressedKey();
		return
	else:
		displayDictionaryScreen(dictionaryName)
		


def displayDictionaryScreen(dictionaryName):
	os.system('clear')
	dictionaryMenu = "(N)ew Note\n(E)dit Note\n(D)elete Note\n(M)ain Menu\n"
	dictionary = dictionaries[dictionaryName]
	print(dictionaryMenu);
	printDictionary(dictionaryName)
	command = getPressedKey().upper()

	if command == 'N':
		key = str(raw_input("Enter note name: "))
		content = str(raw_input("Enter note content: "))
		dictionary[key] = content
		saveDictionaries()
		displayDictionaryScreen(dictionaryName)
	elif command == 'E':
		key = str(raw_input("Enter note name: "))
		print(dictionary[key])
		content = content = str(raw_input("Enter new note content: "))
		dictionary[key] = content
		saveDictionaries()
		print(dictionary[key])
		displayDictionaryScreen(dictionaryName)
	elif command == 'D':
		key = str(raw_input("Enter note name: "))
		del dictionary[key]
		saveDictionaries()
		displayDictionaryScreen(dictionaryName)
	elif command == 'M':
		return



def findDictionary(dictionaryName):
	if dictionaryName not in dictionaries.keys():
		return -1
	else:
		return dictionaries[dictionaryName]



def createNewDictionary():
	dictionaryName = str(raw_input("Enter dictionary name: "))
	if findDictionary(dictionaryName) == -1:
		dictionaries[dictionaryName] = {}
		saveDictionaries()
		displayDictionaryScreen(dictionaryName)
	else:
		print("Dictionary {0} exists. Opening it now...".format(dictionaryName))
		getPressedKey()
		displayDictionaryScreen(dictionaryName)


def showDeleteDictionaryScreen():
	dictionaryName = str(raw_input("Enter dictionary name: "))
	del dictionaries[dictionaryName]

def saveDictionaries():
	file = open(SOURCE_FILE, 'w')
	for dictionaryName in dictionaries.keys():
		file.write("{}\n".format(dictionaryName))
		dictionary = dictionaries[dictionaryName]
		for key in dictionary.keys():
			file.write("{}:{}\n".format(key, dictionary[key]))
	file.close()


def loadDictionaries():
	dictionaries = {}
	with open(SOURCE_FILE) as file:
		for line in file:
			line = line.translate(None, '\n')
			if ':' not in line:
				dictionaries[line] = {}
				dictionaryName = line
			else:
				fields = line.split(":")
				dictionaries[dictionaryName][fields[0]] = fields[1]
	return dictionaries

def printDictionary(dictionaryName):
	print("Dictionary: {}".format(dictionaryName))
	for key in dictionaries[dictionaryName].keys():
		print("{}: {}".format(key, dictionaries[dictionaryName][key]))


dictionaries = loadDictionaries()
displayMainMenu()