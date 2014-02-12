import xml.etree.ElementTree as ET

def parseXml(file):
    tree = ET.parse(file)
    root = tree.getroot()

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
