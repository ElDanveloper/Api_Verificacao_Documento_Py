def numberWithoutMask(number):
    valorTotal = number
    valorTotalNum=""
    for num in valorTotal:
        if num.isdigit():
            valorTotalNum += num
    return valorTotalNum