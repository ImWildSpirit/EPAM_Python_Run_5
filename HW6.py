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
        self.err_msg = ''
        self.err_path = 'Errors_' + self.file_name
        self.record = 1
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
            self.err_msg += 'Expiration date missing or in the past.\n'

    def publish(self):
        if self.from_file is None:
            print('File for reading was not specified')
            exit()
        else:
            with open(self.from_file, 'r') as file:
                tmp = file.read()
            tmp = tmp.split('###')

            for i in range(len(tmp)):
                if findall(r'(\*N\*)', tmp[i]):
                    elem = tmp[i].splitlines()

                    for j in range(len(elem)):
                        if elem[j] == '*N*':
                            if elem[j + 1] != '' or not findall(r'<<\b\D*?>>', elem[j + 1]):
                                elem[j] = ''

                            else:
                                self.validator = False
                                self.err_msg += 'Missing news text.\n'

                        elif findall(r'<<\D*?>>', elem[j]):
                            _city = sub('<<', '', elem[j])
                            self.city = sub('>>', '', _city).strip()

                            if self.city != '':
                                elem[j] = sub(self.city, '', self.city)
                            else:
                                self.validator = False
                                self.err_msg += 'Missing city.\n'

                    _text = text_normalizer('\n'.join(elem))
                    if _text != '':
                        self.text = _text
                    else:
                        self.validator = False
                        self.err_msg += 'Missing news text.\n'

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
                        self.record += 1
                    else:
                        self.unpublished += 1

                        if not path.exists(self.err_path):
                            with open(self.err_path, 'w+') as file:
                                file.write(f'Errors log:\nRecord #{self.record}\nType: News\nIssues: {self.err_msg}')

                        else:
                            if stat(self.err_path).st_size != 0:
                                with open(self.err_path, 'a') as file:
                                    file.write(f'\n\n\nRecord #{self.record}\nType: News\nIssues: {self.err_msg}')

                            else:
                                with open(self.err_path, 'w') as file:
                                    file.write(f'Errors log:\n\n\nRecord #{self.record}\nType: News\nIssues: {self.err_msg}')
                        self.validator = True
                        self.err_msg = ''
                        self.record += 1
                        continue

                elif findall(r'(\*A\*)', tmp[i]):
                    elem = tmp[i].splitlines()

                    for j in range(len(elem)):
                        if findall(r'<<\d\d/\d\d/\d{4}>>', elem[j]):
                            _exp = sub('<<', '', elem[j])
                            _exp = sub('>>', '', _exp).strip()

                            self.exp_date = datetime.strptime(_exp, '%d/%m/%Y').date()
                            self.expire_count = self.get_days_till_expire(custom_date=self.exp_date)

                            if self.validator:
                                elem[j] = sub(datetime.strftime(self.exp_date, '%d/%m/%Y'), '', _exp)

                        elif elem[j] == '*A*':
                            elem[j] = elem[j].replace('*A*', '').strip()

                        elif findall(r'<<>>', elem[j]):
                            self.validator = False
                            self.err_msg += 'Missing expiration date.\n'

                        self.text = text_normalizer('\n'.join(elem))

                        if self.text == '':
                            self.validator = False
                            self.err_msg += 'Missing private ad text.\n'

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
                        self.record += 1
                    else:
                        self.unpublished += 1

                        if not path.exists(self.err_path):
                            with open(self.err_path, 'w+') as file:
                                file.write(f'Errors log:\nRecord #{self.record}\nType: Private Ad\nIssues: {self.err_msg}')

                        else:
                            if stat(self.err_path).st_size != 0:
                                with open(self.err_path, 'a') as file:
                                    file.write(f'\n\n\nRecord #{self.record}\nType: Private Ad\nIssues: {self.err_msg}')

                            else:
                                with open(self.err_path, 'w') as file:
                                    file.write(f'Errors log:\n\n\nRecord #{self.record}\nType: Private Ad\nIssues: {self.err_msg}')
                        self.validator = True
                        self.err_msg = ''
                        self.record += 1
                        continue

                elif findall(r'\*R\*', tmp[i]):
                    elem = tmp[i].splitlines()

                    for j in range(len(elem)):
                        if elem[j] == '*R*':
                            if elem[j + 1] != '':
                                self.title = text_normalizer(elem[j + 1].strip())

                            else:
                                self.validator = False
                                self.err_msg += 'Missing review title.\n'

                            elem[j + 1] = ''
                            elem[j] = ''

                        elif findall(r'<<\b\D*?>>', elem[j]):
                            _author = sub('<<', '', elem[j])
                            self.author = sub('>>', '', _author).strip()

                            if self.author != '':
                                elem[j] = sub(self.author, '', self.author)

                            else:
                                self.validator = False
                                self.err_msg += 'Missing review author.\n'

                        elif findall(r'<<\d+>>', elem[j]):
                            _rate = sub('<<', '', elem[j])
                            self.rate = sub('>>', '', _rate).strip()

                            if self.rate != '' and 1 <= int(self.rate) <= 10:
                                elem[j] = sub(self.rate, '', self.rate)

                            else:
                                self.validator = False
                                self.err_msg += 'Missing or out of range review rate (expected 1 to 10).\n'

                        elif findall(r'<<>>', elem[j]):
                            self.validator = False
                            self.err_msg += 'Missing one of the mandatory attributes: title, author or rate.\n'

                    _text = text_normalizer('\n'.join(elem))

                    if _text != '':
                        self.text = _text

                    else:
                        self.validator = False
                        self.err_msg += 'Missing review text.\n'

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
                        self.record += 1
                    
                    else:
                        self.unpublished += 1

                        if not path.exists(self.err_path):
                            with open(self.err_path, 'w+') as file:
                                file.write(f'Errors log:\nRecord #{self.record}\nType: Review\nIssues: {self.err_msg}')

                        else:
                            if stat(self.err_path).st_size != 0:
                                with open(self.err_path, 'a') as file:
                                    file.write(f'\n\n\nRecord #{self.record}\nType: Review\nIssues: {self.err_msg}')

                            else:
                                with open(self.err_path, 'w') as file:
                                    file.write(f'Errors log:\n\n\nRecord #{self.record}\nType: Review\nIssues: {self.err_msg}')
                        self.validator = True
                        self.err_msg = ''
                        self.record += 1
                        continue
                
                elif findall(r'(\*+[^NAR]?\*+)', elem[j]) or not findall(r'\*', elem[j]):
                    self.unpublished += 1
                    self.err_msg += 'Unknown article type.\n'
                    if not path.exists(self.err_path):
                        with open(self.err_path, 'w+') as file:
                            file.write(f'Errors log:\nRecord #{self.record}\nType: Unknown\nIssues: {self.err_msg}')

                    else:
                        if stat(self.err_path).st_size != 0:
                            with open(self.err_path, 'a') as file:
                                file.write(f'\n\n\nRecord #{self.record}\nType: Unknown\nIssues: {self.err_msg}')

                        else:
                            with open(self.err_path, 'w') as file:
                                file.write(f'Errors log:\n\n\nRecord #{self.record}\nType: Unknown\nIssues: {self.err_msg}')
                    self.validator = True
                    self.err_msg = ''
                    self.record += 1
                    continue

            if self.unpublished == 0:
                print('Success.')
                remove(self.from_file)
            else:
                print(self.unpublished, f'publications skipped due to errors in the source file. See all of the issues in the {self.err_path} file')


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
            if from_file is None:
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

    # Additional article confirmation
    if article == '4':
        try:
            confirm = input(
                'Do you want to upload another file? (Input y to confirm, input any other button to exit)\n')

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

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    else:
        try:
            confirm = input(
                'Do you want to add another article? (Input y to add another article, input any other button to exit)\n')

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
    parser.add_argument('-s', '--source', type=str, help='Path to source file')
    parser.add_argument('-d', '--dest', type=str, help='Path to destination file')
    args = parser.parse_args()

    from_file = args.source
    file_name = args.dest

    if from_file is None and file_name is None:
        print(
            '----Script without arguments will run with testing defaults.----\nSource file - Source.txt,\nDestination file - Publication.txt\nUse -h or --help to show available arguments.\n\n')
        main(from_file='Source.txt', file_name='Publication.txt')
    else:
        main(from_file)
