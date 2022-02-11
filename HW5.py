from datetime import datetime, date, timedelta
from os import path, stat


# News class implementation
class News:

    # Initialization module. If needed to upload to another file, file name can be specified on initializing.
    # Example: News('Filename.txt')
    def __init__(self, file_name = 'Publication.txt'):
        # Class review. Here all the class variables initialized first
        self.text = None
        self.city = None
        self.time = None
        self.file_name = file_name

        if __name__ == '__main__':
            self.main()

    # Gets and returns the article text from the user input
    def __set_text(self):
        try:
            # self.__class__.__name__ construction allows user to see which class was initialized at this moment.
            # Useful in inherited classes
            output = input(f'Type the text of the {self.__class__.__name__}: ')
            return output

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    # Public method for working with text
    def get_text(self):
        return self.__set_text()

    # Gets and returns the city of the event from the user input
    @staticmethod  # Static method means that method doesn't use any of the class variables
    def __set_city():
        try:
            output = input('Type the city: ')
            return output

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    # Public method for working with the city
    def get_city(self):
        return self.__set_city()

    # Public method to get current date in a format dd/mm/yyyy
    @staticmethod  # Static method means that method doesn't use any of the class variables
    def get_time():
        return datetime.now().strftime('%d/%m/%Y')

    # Public method to publish the news to a specified file
    def publish(self):
        self.text = self.get_text()  # First user has to type the text of the article
        self.city = self.get_city()  # Then user has to type the city of the event
        self.time = self.get_time()  # After that time will be generated automatically

        # Upload section
        if not path.exists(self.file_name):  # If file doesn't exist:
            # Create file, open it, write the following and close it ({with} construction)
            with open(self.file_name, 'w+') as file:
                file.write(f'{self.text}\n{self.city}, {self.time}')

        else:  # If file exists:
            if stat(self.file_name).st_size != 0:  # If file is not empty:
                # Open it, append the following to the end of file and close it ({with} construction)
                with open(self.file_name, 'a') as file:
                    file.write(f'\n\n\n{self.text}\n{self.city}, {self.time}')
            else:  # If file is empty:
                # Open it, write the following and close it ({with} construction)
                with open(self.file_name, 'w') as file:
                    file.write(f'{self.text}\n{self.city}, {self.time}')

    # Entry point for this and inherited classes
    def main(self):
        self.publish()


# PrivateAd class implementation. PrivateAd inherits methods from the News class.
class PrivateAd(News):

    # Initialization module. If needed to upload to another file, file name can be specified on initializing.
    # Example: PrivateAd('Filename.txt')
    def __init__(self, file_name = 'Publication.txt'):
        # Class review. Here all the class variables initialized first
        self.exp_date = None
        self.expire_count = None
        self.file_name = file_name
        super().__init__(self.file_name)  # Calls the parent class initialization module

    # Gets and returns the expiration date for the ad from the user input
    def __set_expiration_date(self):
        try:
            exp_date = input('Enter the expiration date in a format dd/mm/yyyy: ')

            return datetime.strptime(exp_date, '%d/%m/%Y').date()

        # ValueError error handling
        except ValueError:
            print('Invalid date format! dd/mm/yyyy required!')
            self.__set_expiration_date()

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    # Public method to work with the expiration date
    def get_expiration_date(self):
        return self.__set_expiration_date()

    # Public method to calculate the amount of days till ad expiration
    def get_days_till_expire(self):

        today = date.today()  # Obtains current date
        result = self.exp_date - today  # Dates subtraction

        if result >= timedelta(days=0):  # If result is more or equal to 0 days:
            return f'{str(result.days)} days till expire.'  # Return string with amount of days till expiration
        else:
            return 'Outdated.'  # Return 'Outdated.' otherwise

    # Public method to publish the ad to a specified file
    def publish(self):
        self.text = self.get_text()  # First user has to type the text of the ad
        self.exp_date = self.get_expiration_date()  # Then user has to type till what date this ad will be actual
        # After that amount of days till expiration will be calculated automatically
        self.expire_count = self.get_days_till_expire()

        # Upload section (see the News() class for the full logic)
        if not path.exists(self.file_name):
            with open(self.file_name, 'w+') as file:
                file.write(f'{self.text}\nActual until: {self.exp_date}, {self.expire_count}')

        else:
            if stat(self.file_name).st_size != 0:
                with open(self.file_name, 'a') as file:
                    file.write(
                        f'\n\n\n{self.text}\nActual until: {self.exp_date.strftime("%d/%m/%Y")}, {self.expire_count}')
            else:
                with open(self.file_name, 'w') as file:
                    file.write(f'{self.text}\nActual until: {self.exp_date.strftime("%d/%m/%Y")}, {self.expire_count}')


# Custom Review class implementation. Review inherits methods from the News class.
class Review(News):

    # Initialization module. If needed to upload to another file, file name can be specified on initializing.
    # Example: Review('Filename.txt')
    def __init__(self, file_name = 'Publication.txt'):
        # Class review. Here all the class variables initialized first
        self.author = None
        self.title = None
        self.rate = None
        self.file_name = file_name
        super().__init__(self.file_name)  # Calls the parent class initialization module

    # Gets and returns the review author name from the user input
    def __set_author(self):
        try:
            output = input('Enter your name: ')

            #  Empty name error handling
            if output == '':
                print("Name can't be empty!")
                self.__set_author()
            else:
                return output

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    # Public method to work with author name
    def get_author(self):
        return self.__set_author()

    # Gets and returns the article name from the user input
    def __set_title(self):
        try:
            output = input('Enter the review title: ')

            #  Empty title error handling
            if output == '':
                print("Title can't be empty!")
                self.__set_title()
            else:
                return output

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    # Public method to work with article title
    def get_title(self):
        return self.__set_title()

    # Gets and returns the review score from the user input
    def __set_rating(self):
        try:
            output = input('Enter your score (10 points max): ')

            # Integer values error handling
            try:
                if 0 <= int(output) <= 10:
                    return output
                else:
                    print('Your score has to be from 0 to 10!')
                    self.__set_rating()

            # ValueError error handling (other type of value or blank)
            except ValueError:
                print(f'Value for the score must be integer, but {type(output)} found!')
                self.__set_rating()

        # KeyboardInterrupt error handling
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()

    # Public method to work with review score
    def get_rating(self):
        return self.__set_rating()

    # Public method to publish the review to a specified file
    def publish(self):
        self.author = self.get_author()  # First user has to type the author name
        self.title = self.get_title()  # Then user has to type article title
        self.text = self.get_text()  # Then type the article
        self.rate = self.get_rating()  # After that set the score of the product under review
        self.time = self.get_time()  # And finally the time of the upload will be set automatically

        # Upload section (see the News class for the full logic)
        if not path.exists(self.file_name):
            with open(self.file_name, 'w+') as file:
                file.write(f'{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')

        else:
            if stat(self.file_name).st_size != 0:
                with open(self.file_name, 'a') as file:
                    file.write(
                        f'\n\n\n{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')
            else:
                with open(self.file_name, 'w') as file:
                    file.write(f'{self.title}\n{self.text}\nFinal score: {self.rate}/10,\n{self.author}, {self.time}')


# -----------Testing playground-------------
# Script entry point, edit main() function to customize the testing process
def main():
    print('------------Adding news------------')
    News()
    print('------------Adding private ad------------')
    PrivateAd()
    print('------------Adding review------------')
    Review()


# Script will run only if not imported to another module.
if __name__ == '__main__':
    main()
