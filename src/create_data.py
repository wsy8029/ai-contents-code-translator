import csv
import random
import itertools

output_complex = []
output_and = []
output_basic = []
input = []
input_and_or = []
input_box = []
output_box = []
sentence = []

with open('train data/output_basic.csv', newline='') as f:
    reader = csv.reader(f)
    for line in reader:
        sentence.append(line[0])

with open('train data/input.csv', newline='') as f:
    reader = csv.reader(f)
    for line in reader:
        input.append(line[0])

with open('train data/input_and.csv', newline='') as f:
    reader = csv.reader(f)
    for line in reader:
        input_and_or.append(line[0])

with open('train data/input_or.csv', newline='') as f:
    reader = csv.reader(f)
    for line in reader:
        input_and_or.append(line[0])

with open('train data/output_complex.csv', newline='') as f:
    reader = csv.reader(f)
    for line in reader:
        output_complex.append(line[0])
        output_box.append(line[0])

with open('train data/output_complex_and.csv', newline='') as f:
    reader = csv.reader(f)
    for line in reader:
        output_and.append(line[0])

for input_item in input:
    input_box.append(input_item)

items = random.sample(set(itertools.product(input_and_or, input)), 2000)
for item in items:
    input_box.append(f"{item[0]} {item[1]}")

items = random.sample(set(itertools.product(output_and, output_complex)), 2000)
for item in items:
    output_box.append(f"{item[0]} {item[1]}")

items = random.sample(set(itertools.product(input_box, output_box)), 10000)
for item in items:
    sentence.append(f"{item[0]} {item[1]}")

with open('sentence.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerows(sentence)
print(sentence)