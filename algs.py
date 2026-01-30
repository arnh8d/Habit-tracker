import datetime
TODAY = datetime.date.today()
print(TODAY)
marks = [datetime.datetime.strptime('2026-01-29', "%Y-%m-%d"),
         datetime.datetime.strptime('2026-01-28', "%Y-%m-%d"),
         datetime.datetime.strptime('2026-01-27', "%Y-%m-%d")]
print(marks)
if not marks:
    print(1000)
elif len(marks) == 1:
    print(1111)
else:
    max_streak = 1
    current_streak = 1

    # Сортируем даты по убыванию (от новых к старым)
    marks.sort(reverse=True)

    for i in range(1, len(marks)):
        prev_date = marks[i - 1].date()  # Преобразуем в date
        curr_date = marks[i].date()      # Преобразуем в date

        delta = (prev_date - curr_date).days  # Получаем разницу в днях (число)

        if delta == 1:  # Теперь сравниваем числа
            current_streak += 1
        else:
            current_streak = 1  # Обрываем стрик, если разница > 1 дня

        max_streak = max(max_streak, current_streak)

    print(max_streak)