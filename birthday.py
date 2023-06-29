birthday = input("생일을 6자리 수로 입력하세요: ")
if len(birthday) != 6:
    print("입력하신 생일이 올바르지 않습니다")
else:
    year = int(birthday[:2])
    month = int(birthday[2:4])
    day = int(birthday[4:])
    if year > 21:
        year += 1900
    else:
        year += 2000
    if month < 1 or month > 12 or day < 1 or day > 31 or (month == 2 and day > 29):
        print("입력하신 생일이 올바르지 않습니다")
    else:
        print(f"입력하신 생일은 {year}년 {month}월 {day}일입니다")
