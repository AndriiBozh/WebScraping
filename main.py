import os.path
from pathlib import Path

import requests as re
import selectorlib
import dotenv

from send_email import send_mail

website_url = dotenv.get_key('.env', 'URL')


def get_webpage_data(url):
    try:
        resp = re.get(url)
        # html structure of a website as a sting
        data_html = resp.text
        return data_html
    except Exception as e:
        print('Error occurred! ', e)


def extract_data(data):
    web_page_extractor = selectorlib.Extractor.from_yaml_file('selectors.yaml')
    # get data (in form of dictionary)
    # name of the key ('find_this') is specified in 'selectors.yaml' file
    value = web_page_extractor.extract(data)
    find_this = value['find_this']
    return find_this


# create empty file if file does not exist
def create_file(filename):
    try:
        open(filename, "a").close()
        print('The file was created')
    except Exception as e:
        print('Error occurred! ', e)


def store_data_in_file(data, filename):
    try:
        with open(filename, 'a') as file:
            file.write(f'- {data}' + '\n')
            print('The data was written to the file.')
    except Exception as e:
        print('Error occurred! ', e)


def read_file(filename):
    try:
        with open(filename, 'r') as file:
            txt = file.read()
            return txt
    except Exception as e:
        print('Error occurred! ', e)


def check_if_file_exists(filename):
    path = Path(f'./{filename}')
    # check whether a path is pointing to a file
    is_file = os.path.isfile(path)
    # will return True if file (named 'filename') exists or False if not
    return is_file


file_name = 'webpage_data.txt'
webpage_data_str = get_webpage_data(website_url)
extracted_data = extract_data(webpage_data_str)
file_exists = check_if_file_exists(file_name)
# if we do not make such check and do not create (an empty) file, then
# an error with arise when we try to read the non-existent file (below)
if not file_exists:
    create_file(file_name)

data_in_file = read_file(file_name)

if extracted_data not in data_in_file:
    store_data_in_file(extracted_data, file_name)

# send email if a new tour is to be organized
if extracted_data != 'No upcoming tours':
    send_mail(extracted_data)
