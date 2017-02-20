import sys
import re
import glob

class Example:
    P_PREFIX = '<ptag>'
    P_SUFFIX = '</ptag>'
    N_PREFIX = '<ntag>'
    N_SUFFIX = '</ntag>'
    P_RE = '<ptag>[a-zA-Z0-9_-]+</ptag>'
    N_RE = '<ntag>[a-zA-Z0-9_-]+</ntag>'
    
    def __init__(self):
        self.words = []
        self.plabels = []
        self.tag_dict = {}
        self.nlabels = []

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
            print 'plabels=', self.plabels
            print 'nlabels=', self.nlabels
            plabel_ctr = 0
            nlabel_ctr = 0
            for i, w in enumerate(self.words):
                if w == '$#':
                    self.tag_dict[i] = self.plabels[plabel_ctr]
                    plabel_ctr+=1
                elif w == '$@':
                    self.tag_dict[i] = self.nlabels[nlabel_ctr]
                    nlabel_ctr+=1
            print self.tag_dict

    def containsTag(self):
        if (len(self.plabels) > 0 or len(self.nlabels) > 0):
            return True
        return False

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

    def evaluateFeature5(self, index):
        tagType = self.words[index]
        prevElements = self.words[index-2:index]
        #print prevElements
        if (len(prevElements) > 0):
            if('ordered' in prevElements):
                return True
        return False

    def evaluateFeature1(self, index):
        return False


class FeatureSet:
    def __init__(self):
        self.values = [0,0,0, 0,0,0, 0,0,0, 0]

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
    
    def insertExample(self, example, idx):
        fs = FeatureSet()
        value = example.evaluateFeature5(idx)
        
        if value:
            fs.setFeatureValue(5,1)
        print fs
        self.exList.append(example)
        self.featuresList.append(fs)
        self.outputList.append(example.getOutputForIndex(idx))

class FileReader:
    def __init__(self):
        self.exampleList = []
        self.dataSet = DataSet('train')

    def readExamples(self, directoryName):
        files = glob.glob(directoryName+'/*')
        filecount = 1
        for file in files:
            print file
            filefd = open(file, 'r')
            for r in filefd:
                r = r.strip()
                if(len(r) > 0):
                    e = Example()
                    e.parseLine(r)
                    if(e.containsTag()):
                        self.exampleList.append(e)
            filefd.close()
            
    def generateDataSet(self):
        for i, ex in enumerate(self.exampleList):
            index = -2
            while(index != -1):
                index = ex.getNextTag(index)
                self.dataSet.insertExample(ex, index)
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
