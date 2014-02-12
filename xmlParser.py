import xml.etree.ElementTree as ET

def parseXml(filename):
    filetext = open(filename).read()
    root = ET.fromstring("<BIBLE>" + filetext + "</BIBLE>")

    sentenceList = []

    for doc in root:
        for text in doc:
            words = text.text.split()
            #print words
            wordList = []
            for word in words:
                wordList.append(word)
                if "." in word:
                    sentenceList.append(wordList)
                    wordList = []
    return sentenceList

print parseXml("kjbible.train")
