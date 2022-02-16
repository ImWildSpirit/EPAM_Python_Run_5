from HW5 import News, PrivateAd, Review
from HW4 import text_normalizer
from os import path, stat, remove
import argparse


class ArticleFromFile(PrivateAd, Review, News):
    def __init__(self, article,from_file=None, file_name='Publication.txt'):
        self.article = article
        self.from_file = from_file
        self.file_name = file_name
        super().__init__(file_name)
    
    def publish(self):
        if self.from_file == None:
            print('File for reading was not specified')
            exit()
        else:
            if self.article == 'News':
                with open(self.from_file, 'r') as container:
                    self.text = text_normalizer(container.read())
                self.city = self.get_city()
                self.time = self.get_time()

                if not path.exists(self.file_name):  # If file doesn't exist:
                    # Create file, open it, write the following and close it ({with} construction)
                    with open(self.file_name, 'w+') as file:
                        file.write(f'News feed:\n\n\n-----News:-----\n{self.text}\n{self.city}, {self.time}')
                    remove(self.from_file)

                else:  # If file exists:
                    if stat(self.file_name).st_size != 0:  # If file is not empty:
                        # Open it, append the following to the end of file and close it ({with} construction)
                        with open(self.file_name, 'a') as file:
                            file.write(f'\n\n\n-----News:-----\n{self.text}\n{self.city}, {self.time}')
                        remove(self.from_file)

                    else:  # If file is empty:
                        # Open it, write the following and close it ({with} construction)
                        with open(self.file_name, 'w') as file:
                            file.write(f'News feed:\n\n\n-----News:-----\n{self.text}\n{self.city}, {self.time}')
                        remove(self.from_file)
        
            elif self.article == 'PrivateAd':
                with open(self.from_file, 'r') as container:
                    self.text = text_normalizer(container.read())
                self.exp_date = self.get_expiration_date()
                self.expire_count = self.get_days_till_expire()

                if not path.exists(self.file_name):
                    with open(self.file_name, 'w+') as file:
                        file.write(f'News feed:\n\n\n-----Private ad:-----\n{self.text}\nActual until: {self.exp_date}, {self.expire_count}')
                    remove(self.from_file)

                else:
                    if stat(self.file_name).st_size != 0:
                        with open(self.file_name, 'a') as file:
                            file.write(f'\n\n\n-----Private ad:-----\n{self.text}\nActual until: {self.exp_date.strftime("%d/%m/%Y")}, {self.expire_count}')
                        remove(self.from_file)

                    else:
                        with open(self.file_name, 'w') as file:
                            file.write(f'News feed:\n\n\n-----Private ad:-----\n{self.text}\nActual until: {self.exp_date.strftime("%d/%m/%Y")}, {self.expire_count}')
                        remove(self.from_file)

            elif self.article == 'Review':
                self.author = self.get_author()
                self.title = self.get_title()
                with open(self.from_file, 'r') as container:
                    self.text = text_normalizer(container.read())
                self.rate = self.get_rating()
                self.time = self.get_time()

                if not path.exists(self.file_name):
                    with open(self.file_name, 'w+') as file:
                        file.write(f'News feed:\n\n\n-----Review:-----\n{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')
                    remove(self.from_file)

                else:
                    if stat(self.file_name).st_size != 0:
                        with open(self.file_name, 'a') as file:
                            file.write(f'\n\n\n-----Review:-----\n{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')
                        remove(self.from_file)

                    else:
                        with open(self.file_name, 'w') as file:
                            file.write(f'News feed:\n\n\n-----Review:-----\n{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')
                        remove(self.from_file)

def main(from_file=None, file_name='Publication.txt'):

    if from_file == None:
        print('File for reading was not specified. Use -s or --source argument to specify path')
        exit()

    else:
        try:
            article = input("""Please choose the type of article you want to upload and press Enter button:
        1 - News
        2 - Private ad
        3 - Review\n""")

            if article == '1':
                print('------------Adding news------------')
                ArticleFromFile('News', from_file, file_name)

            elif article == '2':
                print('------------Adding private ad------------')
                ArticleFromFile('PrivateAd', from_file, file_name)

            elif article == '3':
                print('------------Adding review------------')
                ArticleFromFile('Review', from_file, file_name)

            else:
                print('Incorrect article type\n')
                main(file_name)

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    #Additional article confirmation
    try:
        confirm = input('Do you want to add another article? (Input y to add another article, input any other button to exit)\n')

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
