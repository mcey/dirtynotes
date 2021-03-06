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
			displayFindDictionaryNameScreen()
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
		displayFindDictionaryNameScreen()
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


def displayFindDictionaryNameScreen():
	dictionaryName = findDictionaryName()
	if dictionaryName == -1:
		getPressedKey();
		return
	else:
		displayDictionaryScreen(dictionaryName)
		


def displayDictionaryScreen(dictionaryName):
	os.system('clear')
	dictionaryMenu = "(N)ew Note\n(E)dit Note\n(C)hange Note Name\n(D)elete Note\n(M)ain Menu\n"
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
	elif command == "C":
		showChangeNoteNamePrompt(dictionaryName)
	elif command == 'D':
		key = str(raw_input("Enter note name: "))
		del dictionary[key]
		saveDictionaries()
		displayDictionaryScreen(dictionaryName)
	elif command == 'M':
		return



def findDictionaryName(nameInput = None):
	if(nameInput == None):
		nameInput = str(raw_input("Enter dictionary name: "))
	for key in dictionaries.keys():
		if nameInput.upper() == key.upper():
			return key
	print("No such dictionary exists")
	return -1


def createNewDictionary():
	nameInput = str(raw_input("Enter dictionary name: "))
	dictionaryName = findDictionaryName(nameInput)
	if dictionaryName == -1:
		dictionaries[nameInput] = {}
		saveDictionaries()
		displayDictionaryScreen(nameInput)
	else:
		print("Dictionary {0} exists. Opening it now...".format(dictionaryName))
		getPressedKey()
		displayDictionaryScreen(dictionaryName)


def showDeleteDictionaryScreen():
	dictionaryName = findDictionaryName()
	if dictionaryName != -1:
		del dictionaries[dictionaryName]
	getPressedKey()

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


def showChangeNoteNamePrompt(dictionaryName):
	oldName = str(raw_input("Enter the old note name: "))
	newName = str(raw_input("Enter new note name: "))
	dictionaries[dictionaryName][newName] = dictionaries[dictionaryName].pop(oldName)
	displayDictionaryScreen(dictionaryName)


dictionaries = loadDictionaries()
displayMainMenu()