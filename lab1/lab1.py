import csv
import random

FILENAME1 = "file1.csv"


categories = "ABCD"

 
with open(FILENAME1, "w", newline="") as file:
    writer = csv.writer(file)
    for i in range(0,20):
        stroka = [random.choice(categories),round(random.random()*100,2)]
        writer.writerow(stroka)
with open(FILENAME2, "w", newline="") as file:
    writer = csv.writer(file)
    for i in range(0,20):
        stroka = [random.choice(categories),round(random.random()*100,2)]
        writer.writerow(stroka)
with open(FILENAME3, "w", newline="") as file:
    writer = csv.writer(file)
    for i in range(0,20):
        stroka = [random.choice(categories),round(random.random()*100,2)]
        writer.writerow(stroka)
with open(FILENAME4, "w", newline="") as file:
    writer = csv.writer(file)
    for i in range(0,20):
        stroka = [random.choice(categories),round(random.random()*100,2)]
        writer.writerow(stroka)
with open(FILENAME5, "w", newline="") as file:
    writer = csv.writer(file)
    for i in range(0,20):
        stroka = [random.choice(categories),round(random.random()*100,2)]
        writer.writerow(stroka)  


#считали данные, сразу записыаем в нужную строку матрицы, в зависимости от номера буквы. Далее по каждой строке поиск медианы, вывод с буквой. потом будет общая матрица со всеми данными 
def medianList(array1):
    array1 = sorted(array1)
    if((len(array1) % 2) != 0):
         return array1[len(array1)/2]
    else:
        return (array1[len(array1)//2 + 1] + array1[len(array1)//2])/2

#print(medianList())