from HW5 import News, PrivateAd, Review
from HW4 import text_normalizer
from os import path, stat, remove
from re import findall, sub
from datetime import datetime, date, timedelta
import argparse


class ArticleFromFile(PrivateAd, Review, News):
    def __init__(self, from_file=None, file_name='Publication.txt'):
        self.from_file = from_file
        self.file_name = file_name
        self.validator = True
        self.unpublished = 0
        super().__init__(file_name)

    def get_days_till_expire(self, custom_date=''):

        today = date.today()  # Obtains current date

        # Dates subtraction
        if custom_date == '':
            result = self.exp_date - today
        else:
            result = custom_date - today

        if result >= timedelta(days=0):  # If result is more or equal to 0 days:
            return f'{str(result.days)} days till expire.'  # Return string with amount of days till expiration

        else:
            self.validator = False
            self.unpublished += 1

    def publish(self):
        if self.from_file == None:
            print('File for reading was not specified')
            exit()
        else:
            with open(self.from_file, 'r') as file:
                tmp = file.read()
            tmp = tmp.split('###')

            for i in range(len(tmp)):
                if findall(r'(\*N\*)', tmp[i]):
                    elem = tmp[i].splitlines()
                    
                    for i in range(len(elem)):
                        if elem[i] == '*N*':
                            if elem[i+1] != '' or not findall(r'<<\D*>>', elem[i+1]):
                                elem[i] = ''
                            
                            else:
                                self.validator = False
                                self.unpublished += 1
                            
                        elif findall(r'<<\D*>>', elem[i]):
                            _city = sub('<<', '', elem[i])
                            self.city = sub('>>', '', _city).strip()

                            if self.city != '':
                                elem[i] = sub(self.city, '', self.city)
                            else:
                                self.validator = False
                                self.unpublished +=1
                        
                    _text = text_normalizer('\n'.join(elem))
                    if _text != '':
                        self.text = _text
                    else:
                        self.validator = False
                        self.unpublished += 1

                    self.time = self.get_time()

                    if self.validator:
                        if not path.exists(self.file_name):
                            with open(self.file_name, 'w+') as file:
                                file.write(f'News feed:\n\n\n-----News:-----\n{self.text}\n{self.city}, {self.time}')

                        else:
                            if stat(self.file_name).st_size != 0: 
                                with open(self.file_name, 'a') as file:
                                    file.write(f'\n\n\n-----News:-----\n{self.text}\n{self.city}, {self.time}')

                            else:
                                with open(self.file_name, 'w') as file:
                                    file.write(f'News feed:\n\n\n-----News:-----\n{self.text}\n{self.city}, {self.time}')
                    else:
                        self.validator = True
                        continue
                
                elif findall(r'(\*A\*)', tmp[i]):
                    elem = tmp[i].splitlines()

                    for i in range(len(elem)):
                        if findall(r'<<\d\d/\d\d/\d{4}>>', elem[i]):
                            _exp = sub('<<', '', elem[i])
                            _exp = sub('>>', '', _exp).strip()

                            self.exp_date = datetime.strptime(_exp, '%d/%m/%Y').date()
                            self.expire_count = self.get_days_till_expire(custom_date = self.exp_date)

                            if self.validator:
                                elem[i] = sub(datetime.strftime(self.exp_date, '%d/%m/%Y'), '', _exp)

                        elif elem[i] == '*A*':
                            elem[i] = elem[i].replace('*A*', '').strip()
                        
                        elif findall(r'<<>>', elem[i]):
                            self.validator = False
                            self.unpublished += 1
                        
                        self.text = text_normalizer('\n'.join(elem))
                        
                        if self.text == '':
                            self.validator = False
                            self.unpublished += 1

                    if self.validator:
                        if not path.exists(self.file_name):
                            with open(self.file_name, 'w+') as file:
                                file.write(f'News feed:\n\n\n-----Private ad:-----\n{self.text}\nActual until: {self.exp_date}, {self.expire_count}')

                        else:
                            if stat(self.file_name).st_size != 0:
                                with open(self.file_name, 'a') as file:
                                    file.write(f'\n\n\n-----Private ad:-----\n{self.text}\nActual until: {self.exp_date.strftime("%d/%m/%Y")}, {self.expire_count}')
                            else:
                                with open(self.file_name, 'w') as file:
                                    file.write(f'News feed:\n\n\n-----Private ad:-----\n{self.text}\nActual until: {self.exp_date.strftime("%d/%m/%Y")}, {self.expire_count}')
                    else:
                        self.validator = True
                        continue
                
                elif findall(r'\*R\*', tmp[i]):
                    elem = tmp[i].splitlines()

                    for i in range(len(elem)):
                        if elem[i] == '*R*':
                            if elem[i+1] != '':
                                self.title = text_normalizer(elem[i+1].strip())
                            
                            else:
                                self.validator = False
                                self.unpublished += 1

                            elem[i+1] = ''
                            elem[i] = ''

                        elif findall(r'<<\D*>>', elem[i]):
                            _author = sub('<<', '', elem[i])
                            self.author = sub('>>', '', _author).strip()
                            
                            if self.author != '':
                                elem[i] = sub(self.author, '', self.author)
                                
                            else:
                                self.validator = False
                                self.unpublished += 1
                        
                        elif findall(r'<<\d\d?>>', elem[i]):
                            _rate = sub('<<', '', elem[i])
                            self.rate = sub('>>', '', _rate).strip()
                            
                            if self.rate != '' or 1 <= int(self.rate) <= 10:
                                elem[i] = sub(self.rate, '', self.rate)
                                
                            else:
                                self.validator = False
                                self.unpublished += 1

                        elif findall(r'<<>>', elem[i]):
                            self.validator = False
                            self.unpublished += 1
                    
                    _text = text_normalizer('\n'.join(elem))
                    
                    if _text != '':
                        self.text = _text
                    
                    else:
                        self.validator = False
                        self.unpublished += 1

                    self.time = self.get_time()

                    if self.validator:
                        if not path.exists(self.file_name):
                            with open(self.file_name, 'w+') as file:
                                file.write(f'News feed:\n\n\n-----Review:-----\n{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')

                        else:
                            if stat(self.file_name).st_size != 0:
                                with open(self.file_name, 'a') as file:
                                    file.write(f'\n\n\n-----Review:-----\n{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')
                            else:
                                with open(self.file_name, 'w') as file:
                                    file.write(f'News feed:\n\n\n-----Review:-----\n{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')
                    else:
                        self.validator = True
                        continue

            remove(self.from_file)                           
            print(self.unpublished, 'publications skipped due to errors in the source file.') if self.unpublished > 0 else print('Success.')


def main(from_file=None, file_name='Publication.txt'):
    try:
        article = input("""Please choose the type of article you want to add and press Enter button:
        1 - News
        2 - Private ad
        3 - Review
        4 - Upload from the file\n""")

        if article == '1':
            print('------------Adding news------------')
            News(file_name)

        elif article == '2':
            print('------------Adding private ad------------')
            PrivateAd(file_name)

        elif article == '3':
            print('------------Adding review------------')
            Review(file_name)

        elif article == '4':
                if from_file == None:
                    print('File for reading was not specified. Use -s or --source argument to specify path')
                    exit()
                else:
                    print('------------Uploading------------')
                    ArticleFromFile(from_file, file_name)

        else:
            print('Incorrect article type\n')
            main(file_name)

        # KeyboardInterrupt error handling
    except KeyboardInterrupt:
        print('\nTerminated.')
        exit()

    #Additional article confirmation
    if article == '4':
        try:
            confirm = input('Do you want to upload another file? (Input y to confirm, input any other button to exit)\n')

            if confirm.lower().strip() == 'y':
                try:
                    from_file = input('Please enter the path to the new source file: ')

                    if from_file == '':
                        from_file = None

                except KeyboardInterrupt:
                    print('\nTerminated')
                    exit()
            
                main(from_file, file_name)

            else:
                exit()

        #KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()
    
    else:
        try:
            confirm = input('Do you want to add another article? (Input y to add another article, input any other button to exit)\n')

            if confirm.lower().strip() == 'y':
                main(file_name)

            else:
                exit()

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

# Script entry point. It will run only if not imported to another module.
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type = str, help = 'Path to source file')
    parser.add_argument('-d', '--dest', type = str, help = 'Path to destination file')
    args = parser.parse_args()

    from_file = args.source
    file_name = args.dest

    if from_file == None and file_name == None:
        print('----Script without arguments will run with testing defaults.----\nSource file - Source.txt,\nDestination file - Publication.txt\nUse -h or --help to show available arguments.\n\n')
        main(from_file = 'Source.txt', file_name = 'Publication.txt')
    else:
        main(from_file)
