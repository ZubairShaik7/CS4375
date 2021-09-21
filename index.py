import math
import sys

class node:
    def __init__(self, zeros, ones, twos, total):
        self.zeros = zeros
        self.ones = ones
        self.twos = twos
        self.total = total
        self.left = None
        self.middle = None
        self.right = None
        self.attributes = list()
        self.ids = list()
        self.classification = None

def main():
    #args = sys.argv[1:]
    #if len(args) > 2 or len(args) < 2:
        #print("Invalid number of arguments specified")
        #return
    totalZeros = 0
    totalOnes = 0
    totalTwos = 0
    trainingData = open("train.dat", "r")
    getAttributes = 0
    numberOfAttributes = 0
    attributesRemaining = list()
    for line in trainingData:
        arr = line.split()
        if (arr[len(arr) - 1] == "0"):
            totalZeros+=1
        elif (arr[len(arr) - 1] == "1"):
            totalOnes += 1
        elif (arr[len(arr) - 1] == "2"):
            totalTwos+=1
        if (getAttributes == 0):
            numberOfAttributes = len(line.split()) - 1
            getAttributes+=1
        
    for i in range(0, numberOfAttributes):
        attributesRemaining.append(i)
    parentNode = node(totalZeros,totalOnes,totalTwos, totalZeros + totalOnes + totalTwos)
    learningAlgorithm(attributesRemaining=attributesRemaining, trainingData=trainingData, parentNode=parentNode)

def calculateEntropy(currentNode):
    zeros = currentNode.zeros
    ones = currentNode.ones
    twos = currentNode.twos
    total = zeros + ones + twos
    entropy = 0
    if (zeros != 0):
        entropy += (-zeros/total)*math.log((zeros/total),2)
    if (ones != 0):
        entropy += (-ones/total)*math.log((ones/total),2)
    if (twos != 0):
        entropy += (-twos/total)*math.log((twos/total),2)
    return entropy

def learningAlgorithm(attributesRemaining, trainingData, parentNode):
    recursiveLearningAlgorithm(currentNode=parentNode, attributesRemaining=attributesRemaining)
    treeOutput(currentNode=parentNode, index=-1, spaces=-1)


def recursiveLearningAlgorithm(currentNode, attributesRemaining):
        entropyOfNode = calculateEntropy(currentNode=currentNode)
        if (entropyOfNode == 0 or len(attributesRemaining) == 0 or currentNode.total == 0):
            if (currentNode.zeros >= currentNode.ones and currentNode.zeros > currentNode.twos):
                currentNode.classification = 0
            elif (currentNode.ones > currentNode.zeros and currentNode.ones >= currentNode.twos):
                currentNode.classifcation = 1
            else:
                currentNode.classification = 2
            return
        maxLeftNode = node(0,0,0,0)
        maxMiddleNode = node(0,0,0,0)
        maxRightNode = node(0,0,0,0)
        index = 0
        maxGain = -1000000 
        for count in attributesRemaining:
            trainingData = open("train.dat", "r")
            leftNode = node(0,0,0,0)
            middleNode = node(0,0,0,0)
            rightNode = node(0,0,0,0)
            for line in trainingData:
                arr = line.split()
                current = arr[count]
                classNum = arr[len(arr) - 1]
                isTrue = True
                for i in range(len(currentNode.attributes)):
                    temp2 = arr[currentNode.attributes[i]]
                    num = currentNode.ids[i]
                    if (temp2 != num):
                        isTrue = False
                        break
                if (isTrue):
                    if (current == "0"):
                        if (classNum == "0"):
                            leftNode.zeros+=1
                        elif (classNum == "1"):
                            leftNode.ones+=1
                        elif (classNum == "2"):
                            leftNode.twos+=1
                    elif (current == "1"):
                        if (classNum == "0"):
                            middleNode.zeros+=1
                        elif (classNum == "1"):
                            middleNode.ones+=1
                        elif (classNum == "2"):
                            middleNode.twos+=1
                    elif (current == "2"):
                        if (classNum == "0"):
                            rightNode.zeros+=1
                        elif (classNum == "1"):
                            rightNode.ones+=1
                        elif (classNum == "2"):
                            rightNode.twos+=1

            leftNode.total = leftNode.zeros + leftNode.ones + leftNode.twos
            rightNode.total = rightNode.zeros + rightNode.ones + rightNode.twos
            middleNode.total = middleNode.zeros + middleNode.ones + middleNode.twos
            #leftNode.ids.append("0")
            #middleNode.ids.append("1")
            #rightNode.ids.append("2")
            entropyOfLeft = calculateEntropy(leftNode) * (leftNode.total / currentNode.total)
            entropyOfMiddle = calculateEntropy(middleNode) * (middleNode.total / currentNode.total) 
            entropyOfRight = calculateEntropy(rightNode) * (rightNode.total / currentNode.total) 
            infoGain = entropyOfNode - (entropyOfLeft + entropyOfMiddle + entropyOfRight)
            if (infoGain > maxGain):
                maxGain = infoGain
                maxLeftNode = leftNode
                maxMiddleNode = middleNode
                maxRightNode = rightNode
                index = count
        attributesRemaining.remove(index)
        tempList = attributesRemaining.copy()
        currentNode.attributes.append(index)
        maxLeftNode.attributes.extend(currentNode.attributes)
        currentNode.ids.append("0")
        maxLeftNode.ids.extend(currentNode.ids)
        currentNode.ids.pop()
        currentNode.ids.append("1")
        maxMiddleNode.ids.extend(currentNode.ids)
        currentNode.ids.pop()
        currentNode.ids.append("2")
        maxRightNode.ids.extend(currentNode.ids)
        maxMiddleNode.attributes.extend(currentNode.attributes)
        maxRightNode.attributes.extend(currentNode.attributes)
        currentNode.left = maxLeftNode
        currentNode.right = maxRightNode
        currentNode.middle = maxMiddleNode
        print("going to left")
        recursiveLearningAlgorithm(currentNode=currentNode.left, attributesRemaining=attributesRemaining.copy())
        print("going to middle")
        recursiveLearningAlgorithm(currentNode=currentNode.middle, attributesRemaining=attributesRemaining.copy())
        print("going to right")
        recursiveLearningAlgorithm(currentNode=currentNode.right, attributesRemaining=attributesRemaining.copy())

def treeOutput(currentNode, index, spaces):
    if (currentNode == None or len(currentNode.attributes) <= index):
        return
    for i in range(spaces):
        print("| ", end="")

    if (currentNode.attributes[index] == 0):
        if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
            print("wesley", "=", currentNode.ids[index], ": ", end="")
        else :
            print("wesley", "=", currentNode.ids[index], ":")
    if (currentNode.attributes[index] == 1):
        if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
            print("romulan", "=", currentNode.ids[index], ": ", end="")
        else :
            print("romulan", "=", currentNode.ids[index], ":")
    if (currentNode.attributes[index] == 2):
        if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
            print("poetry", "=", currentNode.ids[index], ": ", end="")
        else :
            print("poetry", "=", currentNode.ids[index], ":")
    if (currentNode.attributes[index] == 3):
        if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
            print("honor", "=", currentNode.ids[index], ": ", end="")
        else :
            print("honor", "=", currentNode.ids[index], ":")
    if (currentNode.attributes[index] == 4):
        if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
            print("tea", "=", currentNode.ids[index], ": ", end="")
        else :
            print("tea", "=", currentNode.ids[index], ":")
    if (currentNode.attributes[index] == 5):
        if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
            print("barclay", "=", currentNode.ids[index], ": ", end="")
        else :
            print("barclay", "=", currentNode.ids[index], ":")
    
    if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
        print(currentNode.classification)

    

    treeOutput(currentNode=currentNode.left, index=index+1, spaces=spaces+1)
    treeOutput(currentNode=currentNode.middle, index=index+1, spaces=spaces+1)
    treeOutput(currentNode=currentNode.right, index=index+1, spaces=spaces+1)


main()