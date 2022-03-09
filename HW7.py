import csv
from re import sub
from string import ascii_uppercase, ascii_lowercase
from HW6 import ArticleFromFile
import argparse

class CSVStatistic:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name) as file:
            with open('Word_count.csv', 'w') as csvfile:
                wordslist = file.read().lower().split()

                for word in range(len(wordslist)):
                    wordslist[word] = sub(r'\W|\d', '', wordslist[word])

                wordslist = list(filter(None, wordslist))
                result = dict()
            
                for word in wordslist:
                    if word in result:
                        result[word] += 1
                    else:
                        result[word] = 1

                writer = csv.writer(csvfile, delimiter = '-')

                for k, v in result.items():
                    writer.writerow([k, v])

        with open(self.file_name) as file:
            with open('Letter count.csv', 'w') as csvfile:
                _text = file.read()
                letter_count = 0
                lower_count = 0
                upper_count = 0
                letter_dict = dict()
                upper_list = []

                headers = ['letter', 'count_all', 'count_uppercase', 'percentage']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()

                for i in _text:
                    if i.isalpha():
                        if i in ascii_lowercase:
                            lower_count += 1
                            letter_count += 1
                            if i in letter_dict:
                                letter_dict[i] += 1
                            else: 
                                letter_dict[i] = 1
                        elif i in ascii_uppercase:
                            upper_count += 1
                            upper_list.append(i)
                            letter_count += 1
                            if i.lower() in letter_dict:
                                letter_dict[i.lower()] += 1
                            else: 
                                letter_dict[i.lower()] = 1
                        else:
                            continue
                    else:
                        continue
            
                for k, v in letter_dict.items():
                    writer.writerow({'letter': k, 'count_all': v + upper_list.count(k.upper()), 'count_uppercase': upper_list.count(k.upper()), 'percentage': f'{round(int(v + upper_list.count(k.upper())) / letter_count * 100, 2)}%'})


def main(from_file, file_name='Publication.txt'):
    ArticleFromFile(from_file, file_name)
    CSVStatistic(file_name)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, help='Path to source file')
    parser.add_argument('-d', '--dest', type=str, help='Path to destination file')
    args = parser.parse_args()

    from_file = args.source
    file_name = args.dest

    if from_file is None and file_name is None:
        print('----Script without arguments will run with testing defaults.----\nSource file - Source.txt,\nDestination file - Publication.txt\nUse -h or --help to show available arguments.\n\n')
        main(from_file='Source.txt', file_name='Publication.txt')
    else:
        main(from_file)