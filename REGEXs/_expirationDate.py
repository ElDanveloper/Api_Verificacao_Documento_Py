from datetime import date, timedelta
d1 = date(1997, 10, 7)
def expirationDate(days_number):
    td = timedelta(days = days_number)
    return d1 + td

if __name__ == "__main__":
    exp_date = expirationDate(8675)
    print(exp_date)
    

