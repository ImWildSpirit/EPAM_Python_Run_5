#imports for values generation
from random import seed
from random import randint

#ensures that generated values will be the same with every run
seed(1)

#creating the list of 100 generated int values from 1 to 1000
sample = [randint(1,1000) for i in range(99)] 
#print(sample)

#bubble sort
for i in range(len(sample)):
    for j in range(i+1, len(sample)):
        if sample[i]>sample[j]:
            sample[i], sample[j] = sample[j], sample[i]
#print(sample)

#creating 2 new empty lists for even and odd numbers
even=[]
odd=[]

#appending values to even or odd list
for i in range(len(sample)):
    if sample[i]%2==0:
        even.append(sample[i])
    else:
        odd.append(sample[i])
#print(even)
#print(odd)

#calculating and printing avg values for both lists
even_avg=sum(even)/len(even)
print('Avg of the even numbers: ', round(even_avg, 3))

odd_avg=sum(odd)/len(odd)
print('Avg of the odd numbers: ', round(odd_avg, 3))