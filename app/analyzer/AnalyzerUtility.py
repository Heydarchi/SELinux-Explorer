
def clean_line(inputStr):
    # print(inputStr)
    if "#" in inputStr:
        if inputStr.strip().index("#") > 0:
            cleaned_str = inputStr.strip()[:inputStr.index("#")].strip()
            if cleaned_str == "" or cleaned_str is None:
                return None
            return cleaned_str
        else:
            return None
    else:
        if inputStr.strip() == "":
            return None
        return inputStr.strip()
