import pyodbc
import argparse
from HW9 import ArticleFromXML, ArticleFromJSON, ArticleFromFile, Review, News, PrivateAd
from HW7 import CSVStatistic
from os import path, stat, remove
from re import findall, sub
from HW4 import text_normalizer
from datetime import datetime
import json
import xml.etree.ElementTree as etree

class DBPublisher(ArticleFromXML, ArticleFromJSON, ArticleFromFile, PrivateAd, Review, News):
    def __init__(self, article, from_file=None, file_name='Publication.txt'):
        self.from_file = from_file
        self.file_name = file_name
        self.article = article
        self.validator = True
        self.err_msg = ''
        self.err_path = 'Errors_' + self.file_name
        self.record = 1
        self.unpublished = 0
        super().__init__(from_file, file_name)

   
    def __set_text(self):
        try:
            output = input(f'Type the text of the {self.article}: ')
            return output
        except KeyboardInterrupt:
            print('\nTerminated.')
            exit()
    
    def get_text(self):
        return self.__set_text()

    def publish(self):
        #Edit config.ini to make it work on your own database
        with open('config.ini', 'r') as config:
            tmp = config.read().splitlines()
            for i in range(len(tmp)):
                if findall('DB_Server=', tmp[i]):
                    self.db_server = sub('DB_Server=', '', tmp[i])
                elif findall('DB_name=', tmp[i]):
                    self.db_name = sub('DB_name=', '', tmp[i])
                elif findall('DB_user=', tmp[i]):
                    self.db_user = sub('DB_user=', '', tmp[i])
                        
        if self.db_name is None:
            print('Database was not specified')
            exit()
        
        else:
            with pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
            f'SERVER={self.db_server};'
            f'DATABASE={self.db_name};'
            f'UID={self.db_user};'
            'Trusted_Connection=yes') as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f'USE {self.db_name};')
                    cursor.execute("IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='News' and xtype='U') \
                        CREATE TABLE News(Text varchar(MAX) NOT NULL, City varchar(58) NOT NULL, Date datetime2 NOT NULL)")
                    cursor.execute("IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='PrivateAd' and xtype='U') \
                        CREATE TABLE PrivateAd(Text varchar(MAX) NOT NULL, Expiration_Date datetime2 NOT NULL)")
                    cursor.execute("IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Review' and xtype='U') \
                        CREATE TABLE Review(Title varchar(100) NOT NULL, Text varchar(MAX) NOT NULL, Rate tinyint NOT NULL, Author varchar(50) NOT NULL, Date datetime2 NOT NULL)")
            
                    if self.article == 'News':
                        self.text = self.get_text()
                        self.city = self.get_city()
                        self.time = self.get_time()

                        if self.text != '' and self.city != '':
                            cursor.execute(f"SELECT * FROM News WHERE Text = '{self.text}' AND City = '{self.city}';")
                            query = cursor.fetchall()
                            if query == []:
                                cursor.execute(f"INSERT INTO News VALUES('{self.text}', '{self.city}', '{self.time}');")
                            else:
                                print("Record already exists in database!")
                                #exit() -> Should i quit and dont add data to file?

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
                            print('Missing News text or city')
                            exit()
                    
                    elif self.article == 'PrivateAd':
                        self.text = self.get_text()
                        self.exp_date = self.get_expiration_date()
                        self.expire_count = self.get_days_till_expire()

                        if self.text != '' and self.exp_date is not None:
                            cursor.execute(f"SELECT * FROM PrivateAd WHERE Text='{self.text}' AND Expiration_Date='{self.exp_date}'")
                            query = cursor.fetchall()
                            if query == []:
                                cursor.execute(f"INSERT INTO PrivateAd VALUES('{self.text}','{self.exp_date}')")
                            else:
                                print("Record already exists in database!")

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
                            print('Missing PrivateAd text or expiration date')
                            exit()
                    
                    elif self.article == 'Review':
                        self.author = self.get_author()
                        self.title = self.get_title()
                        self.text = self.get_text()
                        self.rate = self.get_rating()
                        self.time = self.get_time()

                        if self.author != '' and self.title != '' and self.text != '' and self.rate != '':
                            cursor.execute(f"SELECT * FROM Review WHERE Title='{self.title}' AND Text='{self.text}' AND Author='{self.author}' AND Rate={int(self.rate)}")
                            query = cursor.fetchall()
                            if query == []:
                                cursor.execute(f"INSERT INTO Review VALUES('{self.title}', '{self.text}', {int(self.rate)}, '{self.author}', '{self.time}')")
                            else:
                                print('Record already exists in database!')
                            
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
                            print('Missing Review title, text, author or rating')
                            exit()
                    
                    elif self.article == 'File':
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
                                        cursor.execute(f"SELECT * FROM News WHERE Text='{self.text}' AND City='{self.city}'")
                                        query = cursor.fetchall()

                                        if query == []:
                                            cursor.execute(f"INSERT INTO News VALUES('{self.text}','{self.city}','{self.time}')")

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
                                        cursor.execute(f"SELECT * FROM PrivateAd WHERE Text='{self.text}' AND Expiration_Date='{self.exp_date}'")
                                        query = cursor.fetchall()

                                        if query == []:
                                            cursor.execute(f"INSERT INTO PrivateAd VALUES('{self.text}','{self.exp_date}')")

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
                                        cursor.execute(f"SELECT * FROM Review WHERE Title='{self.title}' AND Text='{self.text}' AND Author='{self.author}' AND Rate={int(self.rate)}")
                                        query = cursor.fetchall()
                                        if query == []:
                                            cursor.execute(f"INSERT INTO Review VALUES('{self.title}', '{self.text}', {int(self.rate)}, '{self.author}', '{self.time}')")

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
                    
                    elif self.article == 'JSON':
                        if self.from_file is None:
                            print('File for reading was not specified')
                            exit()
                        else:
                            with open(self.from_file, 'r') as jsonfile:
                                tmp = json.load(jsonfile)
                                
                                for i in tmp:
                                    try:
                                        if i['type'] == 'news':
                                            try:
                                                if not i['text'] is None and i['text'] != '':
                                                    self.text = i['text']
                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing news text.\n'
                                                                            
                                                if not i['city'] is None and i['city'] != '':
                                                    self.city = i['city']

                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing city.\n'
                                                                            
                                                self.time = self.get_time()
                                            
                                            except KeyError:
                                                self.validator = False
                                                self.err_msg += 'One of the required news components is missing.\n'
                                                                            
                                            if self.validator:
                                                cursor.execute(f"SELECT * FROM News WHERE Text = '{self.text}' AND City = '{self.city}';")
                                                query = cursor.fetchall()
                                                if query == []:
                                                    cursor.execute(f"INSERT INTO News VALUES('{self.text}', '{self.city}', '{self.time}');")
                                                
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
                                        
                                        elif i['type'] == 'ad':
                                            try:
                                                if not i['text'] is None and i['text'] != '':
                                                    self.text = i['text']
                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing private ad text.\n'
                                                    
                                                if not i['expiration'] is None and i['expiration'] != '':
                                                    self.exp_date = datetime.strptime(i['expiration'], '%d/%m/%Y').date()
                                                    self.expire_count = self.get_days_till_expire(custom_date=self.exp_date)

                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing or invalid private ad expiration date.\n'
                                                    
                                            except KeyError:
                                                self.validator = False
                                                self.err_msg += 'One of the required private ad components is missing.\n'
                                                

                                            if self.validator:
                                                cursor.execute(f"SELECT * FROM PrivateAd WHERE Text='{self.text}' AND Expiration_Date='{self.exp_date}'")
                                                query = cursor.fetchall()
                                                if query == []:
                                                    cursor.execute(f"INSERT INTO PrivateAd VALUES('{self.text}','{self.exp_date}')")

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
                                        
                                        elif i['type'] == 'review':
                                            try:
                                                if not i['title'] is None and i['title'] != '':
                                                    self.title = i['title']

                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing review title.\n'
                                                    
                                                if not i['text'] is None and i['text'] != '':
                                                    self.text = i['text']

                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing review text.\n'
                                                
                                                if not i['rate'] is None and i['rate'] != '':
                                                    if 1 <= int(i['rate']) <= 10:
                                                        self.rate = i['rate']

                                                    else:
                                                        self.validator = False
                                                        self.err_msg += 'Review rate out of range.\n'      

                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing review rate.\n'   
                                                
                                                if not i['author'] is None and i['author'] != '':
                                                    self.author = i['author']

                                                else:
                                                    self.validator = False
                                                    self.err_msg += 'Missing review author.\n'   
                                                
                                                self.time = self.get_time()

                                            except KeyError:
                                                self.validator = False
                                                self.err_msg += 'One of the required review components is missing.\n'

                                            if self.validator:
                                                cursor.execute(f"SELECT * FROM Review WHERE Title='{self.title}' AND Text='{self.text}' AND Author='{self.author}' AND Rate={int(self.rate)}")
                                                query = cursor.fetchall()
                                                if query == []:
                                                    cursor.execute(f"INSERT INTO Review VALUES('{self.title}', '{self.text}', {int(self.rate)}, '{self.author}', '{self.time}')")
                                                
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
                                    remove(self.from_file)
                                
                                else:
                                    print(self.unpublished, f'publications skipped due to errors in the source file. See all of the issues in the {self.err_path} file')
                    
                    elif self.article == 'XML':
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
                                                cursor.execute(f"SELECT * FROM News WHERE Text = '{self.text}' AND City = '{self.city}';")
                                                query = cursor.fetchall()
                                                if query == []:
                                                    cursor.execute(f"INSERT INTO News VALUES('{self.text}', '{self.city}', '{self.time}');")
                                                
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
                                                cursor.execute(f"SELECT * FROM PrivateAd WHERE Text='{self.text}' AND Expiration_Date='{self.exp_date}'")
                                                query = cursor.fetchall()
                                                if query == []:
                                                    cursor.execute(f"INSERT INTO PrivateAd VALUES('{self.text}','{self.exp_date}')")
                                                
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
                                                cursor.execute(f"SELECT * FROM Review WHERE Title='{self.title}' AND Text='{self.text}' AND Author='{self.author}' AND Rate={int(self.rate)}")
                                                query = cursor.fetchall()
                                                if query == []:
                                                    cursor.execute(f"INSERT INTO Review VALUES('{self.title}', '{self.text}', {int(self.rate)}, '{self.author}', '{self.time}')")
                                                
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
                                    remove(self.from_file)
                                
                                else:
                                    print(self.unpublished, f'publications skipped due to errors in the source file. See all of the issues in the {self.err_path} file')

def main(from_file, file_name='Publication.txt'):
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
            DBPublisher('News')
            CSVStatistic(file_name)

        elif article == '2':
            print('------------Adding private ad------------')
            DBPublisher('PrivateAd')
            CSVStatistic(file_name)

        elif article == '3':
            print('------------Adding review------------')
            DBPublisher('Review')
            CSVStatistic(file_name)

        elif article == '4':
            if from_file is None:
                print('File for reading was not specified. Use -s or --source argument to specify path')
                exit()
            else:
                print('------------Uploading------------')
                DBPublisher('File', from_file)
                CSVStatistic(file_name)
        
        elif article == '5':
            if from_file is None:
                print('File for reading was not specified. Use -s or --source argument to specify path')
                exit()
            else:
                print('------------Uploading------------')
                DBPublisher('JSON', from_file)
                CSVStatistic(file_name)
        
        elif article == '6':
            if from_file is None:
                print('File for reading was not specified. Use -s or --source argument to specify path')
                exit()
            else:
                print('------------Uploading------------')
                DBPublisher('XML', from_file)
                CSVStatistic(file_name)

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
        print('----Script without arguments will run with testing defaults.----\nSource file - Source.xml,\nDestination file - Publication.txt\nUse -h or --help to show available arguments.\n\n')
        main(from_file='Source.xml', file_name='Publication.txt')
    else:
        main(from_file)
