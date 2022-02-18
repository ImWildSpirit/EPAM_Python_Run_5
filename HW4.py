#  ---Homework #2 refactoring---

hashable_types = [int, float, str, tuple]  #  seed for random function can be hashable type only

#  ensures that generated values will be the same with every run
def random_manipulator(n):
    from random import seed
    if type(n) in hashable_types:
        return seed(n)
    else:
        print('Seed value must be hashable type!')
        exit

#  generates list of dictionaries with given amount, length, min. value, max. value and random seed (optional)
def list_of_dicts_generator(length, amount, min_value, max_value, seed = 1):
    from random import choice, randint
    from string import ascii_lowercase

    sample = []

    if type(length) != int or length < 2 or length > 10:
        print('Dictionary length should be in range from 2 to 10!')
        exit
    elif type(amount) != int or amount < 2 or amount > 10:
        print('Amount of dictionaries in the list should be in range from 2 to 10!')
        exit
    elif type(min_value) != int or type(max_value) != int:
        print('Minimum and maximum values should be integer type!')
        exit
    else:
        if type(seed) in hashable_types:
            random_manipulator(seed)
            sample = [{choice(ascii_lowercase): randint(min_value, max_value) for i in range(length)} for j in range(amount)]
        else:
            random_manipulator([0])
            exit 
    return sample 

#  builds result dictionary from the given list of dictionaries
def dict_builder(sample_list):
    from collections import defaultdict
    
    if type(sample_list) != list:
        print(f'Error: dict_builder function expects a list as argument, but {type(sample_list)} found')
        exit
    
    else:
        result = {}

        tmp = defaultdict(lambda: [-1, -1, 0])
        
        try:
            for i, j in enumerate(sample_list, 1):
                for key, value in j.items():
                    tmp[key][2] += 1
                    if value > tmp[key][0]:
                        tmp[key][:2] = [value, i]
    
            for i, (max_value, index, amount) in tmp.items():
                key = i if amount == 1 else f"{i}_{index}"
                result[key] = max_value
        except AttributeError:
            return 'Values inside the list must be dictionaries!'

        return result

#  ---Homework #3 refactoring---

#  Normalizes the given string from letter cases point of view. Also adds spaces before quotes
def text_normalizer(input):
    import re

    if type(input) != str:
        print(f'Error: text_normalizer function expects a string as an argument, but {type(input)} found')
        exit
    
    step0 = input.lower().splitlines()
    step0a = input.lower()

    i = 0
    while i < len(step0):
        if step0[i] == '' or step0[i] == ' ':
            step0.remove(step0[i])             
        else:
           
            i+=1
    
    step1 = [i.strip().capitalize() for i in step0]
    
    step2 = '\n'.join(step1)

    step3 = re.split(r'([.!?:;](\s))', step2)
    
    i = 0
    while i < len(step3):
        if step3[i] == '' or step3[i] == ' ':
            step3.remove(step3[i]) 
        else:
            step3[i] = step3[i].capitalize()
            i += 1
        
    step4 = ''.join(step3).replace('\n\n','\n').strip()

    tmp = []
    for i in range(len(step4.split(' '))):
        if re.findall('\D“', step4.split(' ')[i]):
            tmp.append(' “'.join(step4.split(' ')[i].split('“')))
        elif re.findall('\D"', step4.split(' ')[i]):
            tmp.append(' "'.join(step4.split(' ')[i].split('"')))
        elif re.findall("\D'", step4.split(' ')[i]):
            tmp.append(" '".join(step4.split(' ')[i].split("'")))
        else:
            tmp.append(step4.split(' ')[i])
    
    result = ' '.join(tmp)
    
    return result

#  adds the sentence to the end that made of last words of each sentence of the given string
def last_words_sentence(input):
    import re

    if type(input) != str:
        print(f'Error: last_words_sentence function expects a string as an argument, but {type(input)} found')
        exit
    
    tmp = input.split()
    last_words_list = []

    for i in range(len(tmp)):
        if re.findall('[:.?!]', tmp[i]):  
            last_words_list.append(re.sub('[:.?!]', '', tmp[i]))

    sentence = input + ' ' + ' '.join(last_words_list) + '.'
    
    return sentence

#  counts every whitespace (spaces, tab, new line symbols) in the given string
def whitespaces_counter(input):
    if type(input) != str:
        print(f'Error: whitespace_counter function expects a string as an argument, but {type(input)} found')
        exit
    
    counter = input.count(' ') + input.count('\n') + input.count('\t')

    return counter

#  --- Testing playground ---
input = """homEwork:

  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View! also, create? one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE?

 

  last iz TO calculate nuMber OF; Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""
# -- Positive tests: --
#print(list_of_dicts_generator(3, 3, 1, 100, 1))
#print(dict_builder(list_of_dicts_generator(3, 3, 1, 100, 1)))
#print(text_normalizer(input))
#print(last_words_sentence(text_normalizer(input)))
#print(whitespaces_counter(last_words_sentence(text_normalizer(input))))

# -- Negative tests: --
#print(random_manipulator(None))
#print(list_of_dicts_generator(-1, 3, 1, 100))
#print(list_of_dicts_generator(3, 11, 1, 1000))
#print(list_of_dicts_generator(3, 3, 'hello', 1000, 5))
#print(list_of_dicts_generator(3, 3, 1, 3.14, 5))
#print(dict_builder([2,3]))
#print(dict_builder('hello world'))