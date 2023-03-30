
def cleanLine(inputStr):
    #print(inputStr)
    if "#" in inputStr:
        if inputStr.strip().index("#") > 0 :
            cleanedStr=inputStr.strip()[:inputStr.index("#")].strip()
            if cleanedStr=="" or cleanedStr==None :
                return None
            return cleanedStr
        else:
            return None
    else:
        if inputStr.strip()=="":
            return None
        return inputStr.strip()
