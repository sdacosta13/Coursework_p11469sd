
def getLine():
    #simple function to get user input
    sentence = input("Enter sentence to spellcheck: ")
    sentence = sentence.split(" ")
    return sentence


def readFromFile():
    #gets words from EnglishWords.txt and splits them into a list
    with open("EnglishWords.txt") as myFile:
        words = myFile.read().split("\n")
    return words


def spellcheck():
    #get required data
    words = readFromFile()
    sentence = getLine()
    #check sentence against the list of valid words
    for userWord in sentence:
        inDict = False
        for word in words:
            if word == userWord:
                inDict = True
        if inDict:
            print(userWord," spelt correctly")
        else:
            print(userWord," not found in dictionary")

spellcheck()
