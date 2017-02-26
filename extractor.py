import sys
import re
import glob
import os

from trie import Trie

#Food afjectives file name
foodAdj_file = 'foodAdjectives.txt'
adverbs_file = 'adverbs.txt'

class Example:
    P_PREFIX = '<ptag>'
    P_SUFFIX = '</ptag>'
    N_PREFIX = '<ntag>'
    N_SUFFIX = '</ntag>'
    P_RE = '<ptag>[\s+\'a-zA-Z0-9_-]+</ptag>'
    N_RE = '<ntag>[\s+\'a-zA-Z0-9_-]+</ntag>'
    
    def __init__(self):
        self.words = []
        self.plabels = []
        self.nlabels = []
        self.tag_dict = {}

    def parseLine(self, line):
        line = line.strip()
        self.plabels = re.findall(Example.P_RE, line)
        if len(self.plabels) > 0:
            line = re.sub(Example.P_RE, ' $# ', line)
            for idx, plabel in enumerate(self.plabels):
                self.plabels[idx] = plabel.replace(Example.P_PREFIX, '').replace(Example.P_SUFFIX, '').strip()
        
        self.nlabels = re.findall(Example.N_RE, line)
        if len(self.nlabels) > 0:
            line = re.sub(Example.N_RE, ' $@ ', line)
            for idx, nlabel in enumerate(self.nlabels):
                self.nlabels[idx] = nlabel.replace(Example.N_PREFIX, '').replace(Example.N_SUFFIX, '').strip()
            
        tags = line.split(' ')

        # Remove empty strings
        if (self.containsTag()):
            self.words = filter(None, tags)
            #print 'plabels=', self.plabels
            #print 'nlabels=', self.nlabels
            plabel_ctr = 0
            nlabel_ctr = 0
            for i, w in enumerate(self.words):
                if w == '$#':
                    self.tag_dict[i] = self.plabels[plabel_ctr]
                    plabel_ctr+=1
                elif w == '$@':
                    self.tag_dict[i] = self.nlabels[nlabel_ctr]
                    nlabel_ctr+=1
            #print self.tag_dict


    def containsTag(self):
        if (len(self.plabels) > 0 or len(self.nlabels) > 0):
            return True
        return False

    def getTagName(self, index):
        #print self.tag_dict
        return self.tag_dict[index]

    def getOutputForIndex(self, index):
        if(self.words[index] == '$#'):
            return 1
        if(self.words[index] == '$@'):
            return 0
        return -1
    
    def getNextTag(self, index):
        if(index+1 >= len(self.words)):
           return -1
        for i in range(index+1, len(self.words)):
            #print "debug", i
            if self.words[i] == '$#':
                return i
            if self.words[i] == '$@':
                return i
            #i+=1
        return -1

    # Prefix is food adjective    
    def evaluateFeature1(self, index, trie):
        tagType = self.words[index]
        prevElements = self.words[index-1:index]
        #print prevElements
        if (len(prevElements) > 0):
            return trie.search(prevElements[0])

        return False

    # Food part of comma seperated values.    
    def evaluateFeature2(self, index):
        tagType = self.words[index]

        prevElements = self.words[index-2:index]
        
        if (len(prevElements) == 2):
            if prevElements[1] == ',' and (index-2) in self.tag_dict:
                #print "current_debug: ", prevElements
                return True

        nextElements = self.words[index+1:index+3]
        
        if (len(prevElements) == 2):
            if prevElements[0] == ',' and (index+2) in self.tag_dict:
                #print "current_debug: ", nextElements
                return True

        return False

    # Prefix is pronoun and suffix is "is/was/were"
    def evaluateFeature3(self, index):
        tagType = self.words[index]

        elements = self.words[index-1:index+2]
        
        if (len(elements) == 3):
            if ((elements[0].lower() == 'their') and (elements[2].lower() in ['is', 'was', 'were'])):
                return True

        return False

    # Prefix is chose,had,choose
    def evaluateFeature4(self, index):
        tagType = self.words[index]
        prevElements = self.words[index-1:index]
        #print prevElements
        if (len(prevElements) > 0):
            if(prevElements[0].lower() in ['chose', 'had', 'choose']):
                return True
        return False

    # Previous 2 words contain ordered.
    def evaluateFeature5(self, index):
        tagType = self.words[index]
        prevElements = self.words[index-2:index]
        #print prevElements
        if (len(prevElements) > 0):
            for each_elem in prevElements:
                if(each_elem.lower() == "ordered"):
                    #print each_elem + "=========================\n"
                    return True
                    
        return False

    # Suffix is 'with'    
    def evaluateFeature6(self, index):
        boolResult = False
        if((index + 1) in range(len(self.words))):
            if(self.words[index + 1].lower() == 'with'):
                boolResult = True
                #print str(self.words)
        return boolResult

    #Number of characters is greater than 2
    def evaluateFeature7(self, index):
        boolResult = False
        strVal = "DEFAULT"
        if index in self.tag_dict:
            strVal = self.tag_dict[index].lower()
        if (strVal.lower() == "sauce" or strVal.lower() == "sauces"):
            boolResult = True
            #print strVal + "=========================\n"
        return boolResult

    #Prefix is article
    def evaluateFeature8(self, index):
        boolResult = False 
        listArticles = ['a','an','the']
        strVal = ""
        if (index-1) in self.tag_dict:
            strVal = self.tag_dict[index-1].lower()
        else:
            if((index - 1) in range(len(self.words))):
                strVal = self.words[index - 1].lower()
        if(strVal) in listArticles:
            #print " VALUE FOUND IS :  " + strVal
            boolResult = True 
        return boolResult       


    #Prefix is 'with'
    def evaluateFeature9(self, index):
        boolResult = False
        if((index - 1) in range(len(self.words))):
            if(self.words[index - 1].lower() == 'with'):
                boolResult = True
                #print str(self.words)

        return boolResult

    # Is a food adjective slang
    def evaluateFeature10(self,index, trie):
        #print str(index) + " and dict " + str(self.tag_dict)
        if index in self.tag_dict:
            return trie.search(self.tag_dict[index].lower())
        else:
            return False


    #Is a pronoun
    def evaluateFeature11(self, index):
        boolResult = False 
        listArticles = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']
        strVal = ""
        if index in self.tag_dict:
            strVal = self.tag_dict[index].lower()
        if(strVal) in listArticles:
            #print " VALUE FOUND IS :  " + strVal
            boolResult = True 
        return boolResult

    #Prefix is is/was/were/in/to/I/for.
    def evaluateFeature13(self, index):
        boolResult = False 
        listArticles = ['is','was','were','in','to','i','for']
        strVal = ""
        if (index-1) in self.tag_dict:
            strVal = self.tag_dict[index-1].lower()
        else:
            if((index - 1) in range(len(self.words))):
                strVal = self.words[index - 1].lower()
        if(strVal) in listArticles:
            #print " PREFIX FOUND IS :  " + strVal
            boolResult = True 
        return boolResult

    #Prefix is adverb
    def evaluateFeature15(self, index, trie):
        boolResult = False 
        #listArticles = ['so', 'very', 'really', 'super', 'painfully', 'only', 'utterly']
        strVal = "DEFAULT"
        if (index-1) in self.tag_dict:
            strVal = self.tag_dict[index-1].lower()
        else:
            if((index - 1) in range(len(self.words))):
                strVal = self.words[index - 1].lower()
        boolResult = trie.search(strVal)
        '''if boolResult:
            print strVal + "=======================\n"'''
        return boolResult

    # Suffix is such that its a name of a place
    def evaluateFeature12(self, index):
        tagValue = self.tag_dict[index]
        for suffix in ['king', 'hut', 'house', 'quiznos', 'place', 'houses']:
            if (str.endswith(tagValue.lower(), suffix)):
                return True

        return False

    # Is last word of the sentence.
    def evaluateFeature14(self, index):
        tagValue = self.tag_dict[index]
        values = self.words[index+1:index+2]

        if len(values) > 0:
            for suffix in ['.', '!', ')']:
                if (str.endswith(values[0], suffix)):
                    return True
        return False

    # Suffix is '-'    
    def evaluateFeature16(self, index):
        boolResult = False
        if((index + 1) in range(len(self.words))):
            if(self.words[index + 1].lower() == '-'):
                boolResult = True
                #print str(self.words) + "=========================\n"
        return boolResult


class FeatureSet:
    def __init__(self):
        self.values = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0,0]

    def __str__(self):
        return ' '.join(str(x) for x in self.values)
    
    def setFeatureValue(self, featureNum, value):
        if((featureNum-1) >= len(self.values)):
            return -1
        self.values[featureNum-1] = value

    def getFeaturesCount(self):
        return len(self.values)

class DataSet:
    def __init__(self, name):
        self.exList = []
        self.featuresList = []
        self.outputList = []
        self.adjTrie = Trie()
        self.advTrie = Trie()
        #self.labelList = []
        with open(foodAdj_file) as f:
            for line in f:
                if len(line) > 2:
                    #print "l" + line
                    self.adjTrie.insert(line.rstrip().lower())

        with open(adverbs_file) as f:
            for line in f:
                if len(line) > 2:
                    #print "l" + line
                    self.advTrie.insert(line.rstrip().lower())
        #print self.advTrie.get_all()

    def insertExample(self, example, idx, fileName):
        fs = FeatureSet()
        value = example.evaluateFeature1(idx, self.adjTrie)
        if value:
            fs.setFeatureValue(1,1)

        value = example.evaluateFeature2(idx)
        if value:
            fs.setFeatureValue(2,1)

        value = example.evaluateFeature3(idx)
        if value:
            fs.setFeatureValue(3,1)

        value = example.evaluateFeature4(idx)
        if value:
            fs.setFeatureValue(4,1)

        value = example.evaluateFeature5(idx)
        if value:
            fs.setFeatureValue(5,1)

        value = example.evaluateFeature10(idx,self.adjTrie)
        if value:
            fs.setFeatureValue(10,1)

        value = example.evaluateFeature6(idx)
        if value:
            fs.setFeatureValue(6,1)

        value = example.evaluateFeature7(idx)
        if value:
            fs.setFeatureValue(7,1)

        value = example.evaluateFeature8(idx)
        if value:
            fs.setFeatureValue(8,1)

        value = example.evaluateFeature9(idx)
        if value:
            fs.setFeatureValue(9,1)

        value = example.evaluateFeature11(idx)
        if value:
            fs.setFeatureValue(11,1)

        value = example.evaluateFeature13(idx)
        if value:
            fs.setFeatureValue(13,1)

        value = example.evaluateFeature15(idx,self.advTrie)
        if value:
            fs.setFeatureValue(15,1)
        '''value = example.evaluateFeature10(idx)
        if value:
            fs.setFeatureValue(10,1)'''

        value = example.evaluateFeature12(idx)
        if value:
            fs.setFeatureValue(12,1)
            
        value = example.evaluateFeature14(idx)
        if value:
            fs.setFeatureValue(14,1)

        value = example.evaluateFeature16(idx)
        if value:
            fs.setFeatureValue(16,1)

        print fs, example.getOutputForIndex(idx), example.getTagName(idx), os.path.basename(fileName)

        self.exList.append(example)
        self.featuresList.append(fs)
        self.outputList.append(example.getOutputForIndex(idx))
        #self.labelList.append(example.getTagName())

class FileReader:
    def __init__(self):
        self.exampleList = []
        self.dataSet = DataSet('train')
        self.fileNames = []

    def readExamples(self, directoryName):
        files = glob.glob(directoryName+'/*')
        filecount = 1
        for file in files:
            #print file
            filefd = open(file, 'r')
            for r in filefd:
                r = r.strip()
                if(len(r) > 0):
                    e = Example()
                    e.parseLine(r)
                    if(e.containsTag()):
                        self.exampleList.append(e)
                        self.fileNames.append(filefd.name)
            filefd.close()
            
    def generateDataSet(self):
        # print "current_debug", len(self.exampleList)
        for i, ex in enumerate(self.exampleList):
            index = -2
            while(index != -1):
                index = ex.getNextTag(index)
                if (index == -1): 
                    break
                self.dataSet.insertExample(ex, index, self.fileNames[i])
            #print i

if __name__ == '__main__':
    if (len(sys.argv) < 1):
        print 'Usage: python extractor.py <directory>'
        sys.exit(1)
    
    directoryName = sys.argv[1]
    fr = FileReader()
    fr.readExamples(directoryName)
    fr.generateDataSet()

'''
class TokenList:
    def __init__(self):
        self.exampleList = []
        
    def addNewExample(self, line):
        e = Example()
        e.parseLine(line)
        self.exampleList.append(e)

    
    def containsTag(self):
        returnFlag = False

        for word in self.tokenLists:
            word = word.strip()
            print word
            if str.startswith(word, Token.P_PREFIX) and str.endswith(word, Token.P_SUFFIX):
                #remove tags and record this index
                returnFlag = True
            elif str.startswith(word, Token.N_PREFIX) and str.endswith(word, Token.N_SUFFIX):
                #remove tags and record this index
                returnFlag = True
    
        if (
        return returnFlag
'''
