
def cleanLine(inputStr):
    print(inputStr)
    if "#" in inputStr:
        if inputStr.strip().index("#") > 0 :
            return inputStr.strip()[:inputStr.index("#")]
        else:
            return None
    else:
        return inputStr.strip()
