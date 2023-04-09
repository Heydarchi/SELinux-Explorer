
def clean_line(input_str):
    # print(input_str)
    if "#" in input_str:
        if input_str.strip().index("#") > 0:
            cleaned_str = input_str.strip()[:input_str.index("#")].strip()
            if cleaned_str == "" or cleaned_str is None:
                return None
            return cleaned_str
        else:
            return None
    else:
        if input_str.strip() == "":
            return None
        return input_str.strip()
