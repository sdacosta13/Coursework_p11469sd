from string import ascii_letters
from datetime import datetime

ascii_letters += " "

def getLine():
    #gets the user input and removes non alphabetical characters
    sentence = input("Enter sentence to spellcheck: ").lower()
    for i in sentence:
        if i not in ascii_letters:
            sentence = sentence.replace(i,"")
    #splits sentence
    sentence = sentence.split(" ")
    return sentence

def validate(sentence):
    #remove instances of ""
    for i in sentence:
        if i not in ascii_letters:
            sentence = sentence.replace(i,"")
    return sentence

def readFromFile():
    #load english words
    with open("EnglishWords.txt") as myFile:
        words = myFile.read().split("\n")
    return words

def rmAll(list1,t):
    #useful function for removing all instances of t from list1
    list2 = []
    for i in list1:
        if i != t:
            list2.append(i)
    return list2

def spellcheck(sentence):
    #get required data and set variables
    words = readFromFile()
    #set vars
    length = len(sentence)
    correct = 0
    false = 0
    #check words agains english words
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
    #print stats
    print()
    print("Number of words: ",str(length))
    print("Number of correctly spelt words: ",str(correct))
    print("Number of incorrectly spelt words: ",str(false))

def checkFile():
    #load sentences from the file
    try:
        filename = input("Enter the name of the file to spellcheck: ")
        starttime = datetime.now()
        with open(filename) as myFile:
            words = myFile.read()
            words = validate(words)
            words = words.lower()
    except FileNotFoundError:
        print("File not found")
    #format list
    words = words.split(" ")
    words = rmAll(words, "")
    #set vars
    wordsCopy = words
    sentence = words
    words = readFromFile()

    length = len(sentence)
    correct = 0
    false = 0
    incorrectWords = []
    #check data against english words
    for userWord in sentence:
        inDict = False
        for word in words:
            if word == userWord:
                inDict = True
        if inDict:
            #print(userWord," spelt correctly")
            correct += 1
        else:
            #print(userWord," not found in dictionary")
            false += 1
            #incorrectWords.append(userWord)
            for n,i in enumerate(wordsCopy):
                if i == userWord:
                    wordsCopy[n] = "?"+wordsCopy[n]+"?"
    #make new file
    output = " "
    output = output.join(wordsCopy)
    filename = filename[:-4]+"_spellchecked.txt"
    curDate = datetime.now()
    curDate = curDate.strftime("%d/%m/%Y %H:%M:%S")
    with open(filename,"w") as myFile:
        myFile.write(curDate)
        myFile.write("\nNumber of words: {}".format(str(length)))
        myFile.write("\nNumber of correctly spelt words: {}".format(str(correct)))
        myFile.write("\nNumber of incorrectly spelt words: {}\n".format(str(false)))
        myFile.write(output)
    #workout time
    endtime = datetime.now()
    elapsed = endtime-starttime
    print("\nNumber of words: ",str(length))
    print("Number of correctly spelt words: ",str(correct))
    print("Number of incorrectly spelt words: ",str(false))
    print("\nTime elapsed "+str((elapsed.seconds*1000000)+elapsed.microseconds)+" microseconds\n")




def main():
    #basic menu
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
