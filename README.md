# python2_2

### Тесты с помощью docstring:
![Screenshot_20221130_042853](https://user-images.githubusercontent.com/51710201/204785008-02b672a3-7e9b-4170-abc5-39c299e875b3.png)
![Screenshot_20221130_042908](https://user-images.githubusercontent.com/51710201/204785015-ea99fe04-1da3-4350-b278-94fc58274c16.png)
![Screenshot_20221130_042922](https://user-images.githubusercontent.com/51710201/204785028-b51bc20a-823b-4a3e-97d4-6e6eec209064.png)
![Screenshot_20221130_043026](https://user-images.githubusercontent.com/51710201/204785040-131a8c1f-8baa-48c4-bfaa-f0ca92c36b0c.png)
![Screenshot_20221130_043039](https://user-images.githubusercontent.com/51710201/204785048-4fa2fd70-8c44-4541-bafc-c4711f5c3bf7.png)

### Тесты с помощью unittest:
![Screenshot_20221130_043214](https://user-images.githubusercontent.com/51710201/204785462-f2653ce6-56a7-4c46-8e89-352f4661ff83.png)
![Screenshot_20221130_043239](https://user-images.githubusercontent.com/51710201/204785470-34b85425-1d3d-489b-b791-aaa8478b6764.png)
![Screenshot_20221130_043251](https://user-images.githubusercontent.com/51710201/204785481-91cedb1e-bd56-4a81-9ead-8dfa2caedc24.png)


### Задание 2.3.3

Используем профилизатор на скрипте table.py, сортируя по общему времени выполнения функций:
![Screenshot_20221202_013118](https://user-images.githubusercontent.com/51710201/205325739-8709b4a1-fbc5-47a1-b4b9-3e5d4c783991.png)
![Screenshot_20221202_013130](https://user-images.githubusercontent.com/51710201/205325759-c1abaa13-ef4b-4248-8e65-b8b653b829ec.png)


Выделим преобразование даты в отдельную функцию и замерим время выполнения:
![Screenshot_20221202_075644](https://user-images.githubusercontent.com/51710201/205325814-f2c9a887-3dc5-4dd3-9857-0b41c34d449d.png)
![Screenshot_20221202_075851](https://user-images.githubusercontent.com/51710201/205325836-f407418a-e6ac-4b57-9484-ab41212f01a6.png)


Напишем еще 2 способа реализации этой функции и также замерим время выполнения:
- 1  
![Screenshot_20221202_080315](https://user-images.githubusercontent.com/51710201/205325878-2fc70ff5-f492-4d66-b3b0-b8e8d27ecaa6.png)
![Screenshot_20221202_080857](https://user-images.githubusercontent.com/51710201/205325885-52d63632-b652-4a15-b8e9-a7bc6c5407ca.png)

- 2   
![Screenshot_20221202_081446](https://user-images.githubusercontent.com/51710201/205325927-9dc49efe-a247-494a-80b7-09acc7ea94aa.png)
![Screenshot_20221202_081455](https://user-images.githubusercontent.com/51710201/205325951-3054d307-9678-4855-9ad6-790b185dba9d.png)

Можно сделать вывод, что последний способ является самым эффективным, его и оставим в коде

### Задание 3.2.1

Разделенные файлы csv:
![Screenshot_20221214_095334](https://user-images.githubusercontent.com/51710201/207509041-9f0d51a7-d588-4226-b884-3a30fdb61039.png)
![Screenshot_20221214_095351](https://user-images.githubusercontent.com/51710201/207509045-9f18aefd-2f09-4792-8ee3-689f5342962c.png)

Примеры:
[year_2007.csv](https://github.com/jurmaev/python2_2/files/10224387/year_2007.csv)
[year_2014.csv](https://github.com/jurmaev/python2_2/files/10224390/year_2014.csv)


### Задание 3.2.2

Результаты работы скрипта без многопроцессорной обработки:  
![Screenshot_20221207_044249](https://user-images.githubusercontent.com/51710201/206217220-a2a36138-f189-4185-be5f-220ce85b9d84.png)

Результаты работы скрипта с многопроцессорной обработкой:
![Screenshot_20221207_081222](https://user-images.githubusercontent.com/51710201/206217252-b25f8f70-588d-4c0d-a011-42e9645cc82c.png)


### Задание 3.2.3

Результаты работы скрипта используя concurrent futures: 
![Screenshot_20221207_102216](https://user-images.githubusercontent.com/51710201/206247933-fbf3ca93-bc35-4e39-a930-efc5d569df31.png)

Можем сделать вывод, что при использовании multiprocessing скрипт работает быстрее


### Задание 3.3.1

Частотность различных валют:  
![Screenshot_20221218_085421](https://user-images.githubusercontent.com/51710201/208307708-f57ec61a-2067-480a-bd87-68d841616ddf.png)

Итоговый dataframe:  
![Screenshot_20221218_105547](https://user-images.githubusercontent.com/51710201/208312111-d418d8a3-a14c-4e0d-81d4-baef0726de93.png)

Разделенные csv файлы:  
![Screenshot_20221218_085818](https://user-images.githubusercontent.com/51710201/208307715-aba1f1bd-3830-4e60-a23b-82ead97ae6a9.png)
