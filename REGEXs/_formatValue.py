def formatValue(value):
    splitat = len(str(value))
    inteiro,decimal = str(value)[:splitat-2], str(value)[splitat-2:]
    formated = inteiro +'.'+decimal
    return float(formated)

if __name__ == "__main__":
    formatValue(16480)
