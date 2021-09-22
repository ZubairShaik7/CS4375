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
    
trainClasses = list()
trainIdList =  list()
testClasses = list()
tempList = list()
idsList = list()

def main():
    args = sys.argv[1:]
    if len(args) > 2 or len(args) < 2:
        print("Invalid number of arguments specified")
        return
    fileName = "train.dat"
    totalZeros = 0
    totalOnes = 0
    totalTwos = 0
    trainingData = open(fileName, "r")
    fileName = args[0]
    testFileName = args[1]
    getAttributes = 0
    numberOfAttributes = 0
    attributesRemaining = list()
    attributes = list()
    for line in trainingData:
        arr = line.split()
        if (arr[0] != "0" and arr[0] != "1" and arr[0] != "2"):
            for word in arr:
                attributes.append(word)
        if (arr[len(arr) - 1] == "0"):
            totalZeros+=1
        elif (arr[len(arr) - 1] == "1"):
            totalOnes += 1
        elif (arr[len(arr) - 1] == "2"):
            totalTwos+=1
        if (getAttributes == 0):
            numberOfAttributes = len(line.split()) - 1
            getAttributes+=1
        temp = list()
        for num in arr:
            temp.append(num)
        trainClasses.append(temp.copy())
    
    mostFrequent = max([totalZeros, totalOnes, totalTwos])
    frequent = ""
    if (mostFrequent == totalZeros):
        frequent = 0
    elif (mostFrequent == totalOnes):
        frequent = 1
    else:
        frequent = 2
    for i in range(0, numberOfAttributes):
        attributesRemaining.append(i)
    parentNode = node(totalZeros,totalOnes,totalTwos, totalZeros + totalOnes + totalTwos)
    learningAlgorithm(attributesRemaining=attributesRemaining, fileName=fileName, parentNode=parentNode, frequent=frequent, attributes=attributes)
    res1 = calculateAccuracy(fileName=fileName)
    res2 = calculateAccuracy(fileName=testFileName)
    print("Accuracy on training set (",res1[1]," instances): ", round(res1[0] / res1[1] * 100,1),"%")
    print("Accuracy on test set (",res2[1]," instances): ", round(res2[0] / res2[1] * 100,1),"%")


def calculateAccuracy(fileName):
    testData = open(fileName,"r")
    correct = 0
    amt = 0
    for line in testData:
        arr = line.split()
        for j in range(len(tempList)):
            instance = tempList[j]
            ids = idsList[j]
            foundInstance = False
            for i in range(len(instance) -1):
                temp1 = arr[instance[i]]
                temp2 = str(ids[i])
                t = len(instance) - 2
                if (temp1 != temp2):
                    break
                if (i == t and temp1 == temp2):
                    foundInstance = True
                    break
            if (foundInstance):
                classNum = arr[len(arr) -1]
                testClass = str(instance[len(instance)-1])
                if (testClass == classNum):
                    correct += 1
                amt += 1
                

    result = (correct / amt) * 100
    return [correct, amt]
    round(result, 1)
    



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

def learningAlgorithm(attributesRemaining,fileName, parentNode, frequent, attributes):
    recursiveLearningAlgorithm(currentNode=parentNode, attributesRemaining=attributesRemaining, frequent=frequent, fileName=fileName)
    treeOutput(currentNode=parentNode, index=-1, spaces=-1, attributes=attributes)


def recursiveLearningAlgorithm(currentNode, attributesRemaining, frequent, fileName):
        entropyOfNode = calculateEntropy(currentNode=currentNode)
        if (entropyOfNode == 0 or len(attributesRemaining) == 0 or currentNode.total == 0):
            if (currentNode.zeros >= currentNode.ones and currentNode.zeros > currentNode.twos):
                currentNode.classification = 0
            elif (currentNode.ones > currentNode.zeros and currentNode.ones >= currentNode.twos):
                currentNode.classifcation = 1
            elif (currentNode.twos > currentNode.ones and currentNode.twos > currentNode.zeros):
                currentNode.classification = 2
            else:
                currentNode.classification = frequent
            return
        maxLeftNode = node(0,0,0,0)
        maxMiddleNode = node(0,0,0,0)
        maxRightNode = node(0,0,0,0)
        index = 0
        maxGain = -1000000 
        for count in attributesRemaining:
            trainingData = open(fileName, "r")
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
        recursiveLearningAlgorithm(currentNode=currentNode.left, attributesRemaining=attributesRemaining.copy(), frequent=frequent, fileName=fileName)
        recursiveLearningAlgorithm(currentNode=currentNode.middle, attributesRemaining=attributesRemaining.copy(), frequent=frequent, fileName=fileName)
        recursiveLearningAlgorithm(currentNode=currentNode.right, attributesRemaining=attributesRemaining.copy(), frequent=frequent, fileName=fileName)

def treeOutput(currentNode, index, spaces, attributes):
    if (currentNode == None or len(currentNode.attributes) <= index):
        return
    for i in range(spaces):
        print("| ", end="")

    if (attributes[currentNode.attributes[index]] in attributes):
        num = currentNode.attributes[index]
        if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
            print(attributes[num], "=", currentNode.ids[index], ": ", end="")
        else :
            print(attributes[num], "=", currentNode.ids[index], ":")
    if (currentNode.left == None and currentNode.middle == None and currentNode.right == None):
        if (currentNode.classification == None):
            currentNode.classification = 1
        temp = currentNode.attributes.copy()
        temp2 = currentNode.ids.copy()
        idsList.append(temp2)
        temp.append(currentNode.classification)
        tempList.append(temp)
        print(currentNode.classification)

    

    treeOutput(currentNode=currentNode.left, index=index+1, spaces=spaces+1, attributes=attributes)
    treeOutput(currentNode=currentNode.middle, index=index+1, spaces=spaces+1, attributes=attributes)
    treeOutput(currentNode=currentNode.right, index=index+1, spaces=spaces+1, attributes=attributes)

main()