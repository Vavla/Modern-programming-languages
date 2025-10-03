import csv
import random
from concurrent.futures import ProcessPoolExecutor as Pool
import pandas as pd
import numpy as np

FILENAME1 = "file1.csv"
FILENAME2 = "file2.csv"
FILENAME3 = "file3.csv"
FILENAME4 = "file4.csv"
FILENAME5 = "file5.csv"
filenames = [FILENAME1,FILENAME2,FILENAME3,FILENAME4,FILENAME5]
categories = "ABCD"

for fname in filenames:
    with open(fname, "w", newline="") as file:
        writer = csv.writer(file)
        for i in range(0,20):
            stroka = [random.choice(categories),round(random.random()*100,2)]
            writer.writerow(stroka)


def median_list(array1):
    array1 = sorted(array1)
    if((len(array1) % 2) != 0):
         return array1[len(array1)//2]
    else:
        return (array1[len(array1)//2 - 1] + array1[len(array1)//2])/2


def processing_file(fname):
    array_letter_a = []
    array_letter_b = []
    array_letter_c = []
    array_letter_d = []
    result = 0
    with open(fname, mode='r') as file:
        print(f"This file: {fname}")
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] == 'A':
                array_letter_a.append(float(row[1]))
            elif row[0] == 'B':
                array_letter_b.append(float(row[1]))
            elif row[0] == 'C':
                array_letter_c.append(float(row[1]))
            elif row[0] == 'D':
                array_letter_d.append(float(row[1]))
    with open(f'{fname[0:5]}_out.txt', 'w') as m_file:
        if(len(array_letter_a) != 0):
            m_file.write('A: '+ str(median_list(array_letter_a))+'\n')
        if(len(array_letter_b) != 0):
            m_file.write('B: '+ str(median_list(array_letter_b))+'\n')
            print(fname,'B: '+ median_list(array_letter_b))
        if(len(array_letter_c) != 0):
            m_file.write('C: ' + str(median_list(array_letter_c))+'\n')
            print(fname,'C: '+ str(median_list(array_letter_c)))
        if(len(array_letter_d) != 0):
            m_file.write('D: ' + str(median_list(array_letter_d))+'\n')
            print(fname,'D: '+ str(median_list(array_letter_d)))
    

if __name__ == "__main__":
    with Pool(5) as executor:
    # Запуск задачи параллельно
        executor.map(processing_file, filenames)
    # Ожидание результата и получение его
    

