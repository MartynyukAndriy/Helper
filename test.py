import datetime

date_now = datetime.datetime.now().year
print(type(date_now))

test_date = datetime.date(2024, 1, 10)

delta = datetime.datetime.now().date() - test_date

print(delta.days < 0)
