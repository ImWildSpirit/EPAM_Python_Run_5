import re  #  imports python regexp library

#  initial text
input = """homEwork:

  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

#print(repr(input))  #  repr prints all symbols inside the string, including invisible (like \n), comment if not required

step0 = input.lower().splitlines()  #  lowercases all symbols inside the initial string and then splitting it line by line into the list
#print(repr(step0))

i = 0  #  initial iterator value
while i < len(step0):  #  while iterator < length of the list:
    if step0[i] == '' or step0[i] == ' ':  #  if value is empty string or whitespace:
        step0.remove(step0[i])             #  removing it from the list
    else:
        i+=1                               #  checking next value otherwise
#print(repr(step0))

step1 = [i.strip().capitalize() for i in step0]  #  trims and capitalizes every value inside the list
#print(repr(step1))

step2 = ' '.join(step1)  #  creating a string from the list, using whitespace as separator
#print(repr(step2))

#  the point of steps3, step4 and step5 is to capitalize sentences inside the line, that wasn't capitalized on the step0
step3 = re.split('[:.] ', step2)  #  splitting string to the list again, using punctuation symbols as the split separator
#print(step3)

step4 = [i.capitalize() for i in step3]  #  capitalizing every string in the list. 
#print(step4)

step5 = '. '.join(step4)  #  creating a string from the list, using dot and whitespace as separator
#print(step5)

step6 = step5.replace('Homework.', 'Homework:').replace('tex.', 'text.').replace('“iz”', ' “iz”').replace(' iz ', ' is ')  #  replacing typos
#print(step6)  #  <- Final version of the processed initial text is contained in step6

#  the next step is creating additional sentence with last words of each existing sentence at the end of the processed text (step6)
step7 = step6.split()  #  splitting the text word by word (separator - whitespace)
#print(step7)

last_words_list = []  #  creating empty list, where words of our sentence will be

for i in range(len(step7)):  #  for every word in the list
    if re.findall('[:.]', step7[i]):  #  if it contains punctuation
        last_words_list.append(re.sub('[:.]', '', step7[i]))  #  removing the punctuation symbol and appending this word to the list

final_text = step6 + ' ' + ' '.join(last_words_list) + '.'  #  adding the sentence to the processed text
#print(final_text)

whitespace_counter = '\n\nWhitespaces in text: ' + str(final_text.count(' '))  #  counting all whitespaces

result = 'Before:\n\n' + input + '\n\nAfter:\n\n' + final_text + whitespace_counter  #  forming the result for printing

print(result)  #  printing the result
