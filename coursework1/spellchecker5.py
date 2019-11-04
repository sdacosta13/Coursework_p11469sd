from string import ascii_letters
from datetime import datetime
from difflib import SequenceMatcher
ascii_letters += " "

def getLine():
    #simple user input
    sentence = input("Enter sentence to spellcheck: ").lower()
    for i in sentence:
        if i not in ascii_letters:
            sentence = sentence.replace(i,"")
    sentence = sentence.split(" ")
    return sentence
def validate(sentence):
    #remove instances of ""
    for i in sentence:
        if i not in ascii_letters:
            sentence = sentence.replace(i,"")
    return sentence

def readFromFile():
    #get english words data
    with open("EnglishWords.txt") as myFile:
        words = myFile.read().split("\n")
    return words

def addWord(word):
    #add word to dictionary
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
    #old function for single line checking
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

def determine(correct,false,ignored,marked,added,wordsCopy,userWord):
    #declare menu
    x = """
    ┌─────────────────────────────────────────────────┐
    │    W O R D   N O T   F O U N D                  │
    │                                                 │
    │      """+ userWord+ " "*(43-len(userWord))+"""│
    │                                                 │
    │      1. Ignore the word.                        │
    │      2. Mark the word as incorrect.             │
    │      3. Add word to dictionary.                 │
    │                                                 │
    ├─────────────────────────────────────────────────┘
    └───────────── Enter choice: """
    #mark words
    userInp = input(x)
    if userInp == "1":
        ignored += 1
        for n,i in enumerate(wordsCopy):
            if i == userWord:
                wordsCopy[n] = "!"+wordsCopy[n]+"!"
    elif userInp == "3":
        added += 1
        addWord(userWord)
        for n,i in enumerate(wordsCopy):
            if i == userWord:
                wordsCopy[n] = "*"+wordsCopy[n]+"*"
    else:
        false += 1
        marked += 1
        for n,i in enumerate(wordsCopy):
            if i == userWord:
                wordsCopy[n] = "?"+wordsCopy[n]+"?"
    return correct,false,ignored,marked,added,wordsCopy,userWord

def checkFile():
    #declare menu
    x = """
    ┌─────────────────────────────────────────────────┐
    │    L O A D   F I L E                            │
    │                                                 │
    │      Enter the file name                        │
    │      the press [enter]                          │
    │                                                 │
    │      0. Quit                                    │
    ├─────────────────────────────────────────────────┘
    └───────────── Filename: """
    #get filename, open retrieve data and format
    try:
        filename = input(x)
        starttime = datetime.now()
        with open(filename) as myFile:
            words = myFile.read()
            words = validate(words)
            words = words.lower()
    except FileNotFoundError:
        print("File not found")
        quit()
    #format data
    words = words.split(" ")
    words = rmAll(words, "")
    wordsCopy = words
    sentence = words
    words = readFromFile()
    #initialise vars
    length = len(sentence)
    correct = 0
    false = 0
    ignored = 0
    marked = 0
    added = 0
    mostValidScore = 0
    #check input against english words
    for userWord in sentence:
        inDict = False
        for word in words:
            if word == userWord:
                inDict = True
        if inDict:
            #print(userWord," spelt correctly")
            correct += 1
        else:
            mostValid = "No words Found"
            #search english words for the most likely substitute word
            for legal in words:
                if SequenceMatcher(None,legal, userWord).ratio()>mostValidScore:
                    mostValid = legal
                    mostValidScore = SequenceMatcher(None,legal, userWord).ratio()
            #define menu

            if mostValid != "No words Found":
                x = """
    ┌─────────────────────────────────────────────────┐
    │    W O R D   N O T   F O U N D                  │
    │                                                 │
    │      """+ userWord+ " "*(43-len(userWord))+"""│
    │      did you mean                               │
    │                                                 │
    │      """+ mostValid+ " "*(43-len(mostValid))+"""│
    ├─────────────────────────────────────────────────┘
    └───────────── Enter [y] or [n]: """
                #get response , defualt to no
                userInp = input(x)
                if userInp.lower() == "y":
                    for n,i in enumerate(wordsCopy):
                        if i == userWord:
                            wordsCopy[n] = mostValid
                else:
                    correct,false,ignored,marked,added,wordsCopy,userWord = determine(correct,false,ignored,marked,added,wordsCopy,userWord)
            else:
                correct,false,ignored,marked,added,wordsCopy,userWord = determine(correct,false,ignored,marked,added,wordsCopy,userWord)

    #write stats and data
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
##    print("\nNumber of words: ",str(length))
##    print("Number of correctly spelt words: ",str(correct))
##    print("Number of incorrectly spelt words: ",str(false))
##    print("Number ignored: ",str(ignored))
##    print("Number added to dictionary: ",str(added))
##    print("Number marked: ",str(marked))
##    print("\nTime elapsed "+str((elapsed.seconds*1000000)+elapsed.microseconds)+" microseconds\n")




def main():
    #main menu
    x = """
    ┌─────────────────────────────────────────────────┐
    │    S P E L L   C H E C K E R                    │
    │                                                 │
    │      1. Check a file                            │
    │      2. Check a sentence                        │
    │                                                 │
    │      0. Quit                                    │
    ├─────────────────────────────────────────────────┘
    └───────────────────────────────── Enter choice: """
    while True:
        choice = input(x)
        if choice.lower() == "2":
            sentence = getLine()
            spellcheck(sentence)
        elif choice.lower() == "1":
            checkFile()
        else:
            break



main()
