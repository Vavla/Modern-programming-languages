import csv
import random
from concurrent.futures import ProcessPoolExecutor as Pool
import pandas as pd

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

