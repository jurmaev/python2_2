import pdf
import table

work_method = input('Введите вид формирования данных: ')
if work_method.lower() == 'вакансии':
    table.get_table()
elif work_method.lower() == 'статистика':
    pdf.get_pdf()
else:
    print('Неверный метод формирования данных!')