from string import ascii_letters
from datetime import datetime
#get string of valid characters
ascii_letters += " "

def getLine():
    #get user sentence to check
    sentence = input("Enter sentence to spellcheck: ").lower()
    for i in sentence:
        if i not in ascii_letters:
            sentence = sentence.replace(i,"")
    sentence = sentence.split(" ")
    return sentence
def validate(sentence):
    #remove non alpha
    for i in sentence:
        if i not in ascii_letters:
            sentence = sentence.replace(i,"")
    return sentence

def readFromFile():
    #get data from englishwords
    with open("EnglishWords.txt") as myFile:
        words = myFile.read().split("\n")
    return words

def addWord(word):
    #add new word to dictionary
    with open("EnglishWords.txt","a") as myFile:
        myFile.write("\n{}".format(word))


def rmAll(list1,t):
    #useful function for removing all instances of t from list1
    list2 = []
    for i in list1:
        if i != t:
            list2.append(i)
    return list2

def spellcheck(sentence):
    #no changes from previous file
    words = readFromFile()

    length = len(sentence)
    correct = 0
    false = 0

    for userWord in sentence:
        inDict = False
        for word in words:
            if word == userWord:
                inDict = True
        if inDict:
            print(userWord," spelt correctly")
            correct += 1
        else:
            print(userWord," not found in dictionary")
            false += 1
    print()
    print("Number of words: ",str(length))
    print("Number of correctly spelt words: ",str(correct))
    print("Number of incorrectly spelt words: ",str(false))

def checkFile():
    #get filename from user and retrieve data
    try:
        filename = input("Enter the name of the file to spellcheck: ")
        starttime = datetime.now()
        with open(filename) as myFile:
            words = myFile.read()
            words = validate(words)
            words = words.lower()
    except FileNotFoundError:
        print("File not found")
    #format data
    words = words.split(" ")
    words = rmAll(words, "")
    wordsCopy = words
    sentence = words
    words = readFromFile()
    #set vars
    length = len(sentence)
    correct = 0
    false = 0
    ignored = 0
    marked = 0
    added = 0
    #check data against englishwords
    for userWord in sentence:
        inDict = False
        for word in words:
            if word == userWord:
                inDict = True
        if inDict:
            #print(userWord," spelt correctly")
            correct += 1
        else:
            print(userWord," not found in dictionary")
	    #menu for correcting a word
            #incorrectWords.append(userWord)
            print("""
            1. Ignore the word.
            2. Mark the words as incorrect.
            3. Add word to dictionary.
            """)
            userInp = input("Enter choice:")
            if userInp == "1":
                false += 1
                ignored += 1
                for n,i in enumerate(wordsCopy):
                    if i == userWord:
                        #append and prepend a !
                        wordsCopy[n] = "!"+wordsCopy[n]+"!"
            elif userInp == "3":
                added += 1
                false += 1
                addWord(userWord)
                for n,i in enumerate(wordsCopy):
                    if i == userWord:
                        #append and prepend a *
                        wordsCopy[n] = "*"+wordsCopy[n]+"*"
            else:
                marked += 1
                false += 1
                for n,i in enumerate(wordsCopy):
                    if i == userWord:
                        #append and prepend a ?
                        wordsCopy[n] = "?"+wordsCopy[n]+"?"
    #write statistics, date to file
    output = " "
    output = output.join(wordsCopy)
    filename = filename[:-4]+"_spellchecked.txt"
    curDate = datetime.now()
    curDate = curDate.strftime("%d/%m/%Y %H:%M:%S")
    with open(filename,"w") as myFile:
        myFile.write(curDate)
        myFile.write("\nNumber of words: {}".format(length))
        myFile.write("\nNumber of correctly spelt words: {}".format(correct))
        myFile.write("\nNumber of incorrectly spelt words: {}".format(false))
        myFile.write("\nNumber ignored: {}".format(ignored))
        myFile.write("\nNumber added to dictionary: {}".format(added))
        myFile.write("\nNumber markered: {}\n\n".format(marked))

        myFile.write(output)
    endtime = datetime.now()
    elapsed = endtime-starttime
    #print statistics
    print("\nNumber of words: ",str(length))
    print("Number of correctly spelt words: ",str(correct))
    print("Number of incorrectly spelt words: ",str(false))
    print("Number ignored: ",str(ignored))
    print("Number added to dictionary: ",str(added))
    print("Number marked: ",str(marked))
    print("\nTime elapsed "+str((elapsed.seconds*1000000)+elapsed.microseconds)+" microseconds\n")




def main():
    #main menu
    x = """S P E L L C H E C K E R
 1. Check a file
 2. Check a sentence
 0. Quit
    """
    while True:
        choice = input(x)
        print("Enter a choice: ",end="")

        if choice.lower() == "2":
            sentence = getLine()
            spellcheck(sentence)
        elif choice.lower() == "1":
            checkFile()
        else:
            break



main()
