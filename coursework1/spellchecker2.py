from string import ascii_letters
#get ascii_letters contains the alphabet
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


def readFromFile():
    #load english words
    with open("EnglishWords.txt") as myFile:
        words = myFile.read().split("\n")
    return words


def spellcheck():
    #get required data and set variables
    words = readFromFile()
    sentence = getLine()
    length = len(sentence)
    correct = 0
    false = 0
    #spellcheck
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

def main():
    #menu
    spellcheck()
    while True:
        choice = input("Press q [enter] to quit or any other key [enter] to go again:")
        if choice.lower() == "q":
            break
        else:
            spellcheck()




main()
