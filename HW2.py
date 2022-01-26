from string import ascii_lowercase # imports lowercase ascii characters
from random import randint, seed, choice # imports methods for random numbers generator
from collections import defaultdict # imports method for keeping track of unrepeated keys

seed(1) # ensures that generated values will be the same with every run, comment if not required

dictlen = randint(2, 10) # generates dictionaries length
dictamount = randint(2, 10) # generates amount of disctionaries in the list

print('Dict length = ', dictlen) # shows generated dictionary length
print('Amount of dicts in list = ', dictamount) # shows generated amount of dictionaries in the list

# generates list of dictionaries with generated amount and length
sample = [{choice(ascii_lowercase): randint(1, 100) for i in range(dictlen)} for j in range(dictamount)]

print(sample) # prints generated list

result = {} #result dictionary will be here

# creates temporary defaultdict with a format {key: [max_value, index_of_max_value, amount_of_keys_found]}
tmp = defaultdict(lambda: [-1, -1, 0]) 
for i, j in enumerate(sample, 1):  # starts indexing at 1
    for key, value in j.items():
        tmp[key][2] += 1  # always increase count
        if value > tmp[key][0]:
            tmp[key][:2] = [value, i]  # update max and index_max

print(tmp) # prints temporary defaultdict, comment the row if not required

# building result dictionary from the tmp data
for i, (max_value, index, amount) in tmp.items():
    # if {amount_of_keys_found} = 1 -- put the key as is, otherwise -- generate the key name in a {key}_{index_of_max_value} format
    key = i if amount == 1 else "{}_{}".format(i, index)
    result[key] = max_value # put the {max_value} in the result dictionary
print('Result: ', result)
