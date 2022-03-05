import xml.etree.ElementTree as etree
from os import path, stat, remove
from HW5 import News, PrivateAd, Review
from HW6 import ArticleFromFile
from HW8 import ArticleFromJSON
from datetime import datetime
import argparse


class ArticleFromXML(ArticleFromJSON):
    def __init__(self, from_file=None, file_name='Publication.txt'):
        self.from_file = from_file
        self.file_name = file_name
        self.validator = True
        self.err_msg = ''
        self.err_path = 'Errors_' + self.file_name
        self.record = 1
        self.unpublished = 0
        super().__init__(from_file, file_name)

    def publish(self):
        if self.from_file is None:
            print('File for reading was not specified')
            exit()

        else:
            with open(self.from_file, 'r') as xmlfile:
                tmp = etree.parse(xmlfile)
                root = tmp.getroot()
                for i in root.iter('article'):
                    try:
                        if i.attrib['type'] == 'news':
                            try:
                                if i.find('text').text is not None and i.find('text').text != '':
                                    self.text = i.find('text').text
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing news text.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing news text.\n'
                            
                            try:
                                if i.find('city').text is not None and i.find('city').text != '':
                                    self.city = i.find('city').text
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing news city.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing news city.\n'
                            
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

                        elif i.attrib['type'] == 'ad':
                            try:
                                if i.find('text').text is not None and i.find('text').text != '':
                                    self.text = i.find('text').text
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing private ad text.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing private ad text.\n'
                            
                            try:
                                if i.find('expiration').text is not None and i.find('expiration').text != '':
                                    self.exp_date = datetime.strptime(i.find('expiration').text, '%d/%m/%Y').date()
                                    self.expire_count = self.get_days_till_expire(custom_date=self.exp_date)
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing or invalid private ad expiration date.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing or invalid private ad expiration date.\n'

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

                        elif i.attrib['type'] == 'review':
                            try:
                                if i.find('title').text is not None and i.find('title').text != '':
                                    self.title = i.find('title').text
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing review title.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing review title.\n'

                            try:
                                if i.find('text').text is not None and i.find('text').text != '':
                                    self.text = i.find('text').text
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing review text.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing review text.\n'
                            
                            try:
                                if i.find('author').text is not None and i.find('author').text != '':
                                    self.author = i.find('author').text
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing review author.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing review author.\n'

                            try:
                                if i.find('rate').text is not None and i.find('rate').text != '':
                                    if 1<= int(i.find('rate').text) <= 10:
                                        self.rate = i.find('rate').text
                                    else:
                                        self.validator = False
                                        self.err_msg += 'Review rate out of range'
                                else:
                                    self.validator = False
                                    self.err_msg += 'Missing review rate.\n'
                            except AttributeError:
                                self.validator = False
                                self.err_msg += 'Missing review rate.\n'
                            except ValueError:
                                self.validator = False
                                self.err_msg += 'Invalid rate type'
                            
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

                        else:
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

                    except KeyError:
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
                    #remove(self.from_file)
                
                else:
                    print(self.unpublished, f'publications skipped due to errors in the source file. See all of the issues in the {self.err_path} file')

def main(from_file=None, file_name='Publication.txt'):
    try:
        article = input("""Please choose the type of article you want to add and press Enter button:
        1 - News
        2 - Private ad
        3 - Review
        4 - Upload from the file
        5 - Upload from JSON
        6 - Upload from XML\n""")

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
        
        elif article == '5':
            if from_file is None:
                print('File for reading was not specified. Use -s or --source argument to specify path')
                exit()
            else:
                print('------------Uploading------------')
                ArticleFromJSON(from_file, file_name)
        
        elif article == '6':
            if from_file is None:
                print('File for reading was not specified. Use -s or --source argument to specify path')
                exit()
            else:
                print('------------Uploading------------')
                ArticleFromXML(from_file, file_name)

        else:
            print('Incorrect article type\n')
            main(file_name)

        # KeyboardInterrupt error handling
    except KeyboardInterrupt:
        print('\nTerminated.')
        exit()

    # Additional article confirmation
    if article == '4' or article == '5' or article == '6':
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
        print('----Script without arguments will run with testing defaults.----\nSource file - Source.txt,\nDestination file - Publication.txt\nUse -h or --help to show available arguments.\n\n')
        main(from_file='Source.json', file_name='Publication.txt')
    else:
        main(from_file)