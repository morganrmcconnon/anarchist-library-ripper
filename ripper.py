import requests
import re
from pathlib import Path
import os
import sys

#Gets source file of library page to extract text names
def get_texts(library):
    #Open library source file
    source = requests.get(library).content
    #Convert source from byte to string and remove whitespaces
    source = source.decode('UTF-8')
    source = ''.join(source.split())

    #Extract links from texts
    pattern = "(?<=<divclass=\"amw-listing-item\"><ahref=\").*?(?=\"class=\"list-group-item\">)"
    texts_list = re.findall(pattern,source)

    #Removes link to library from source results
    texts_list.pop(1)
    return texts_list

#Get current count of downloaded texts and determine how many new texts script needs to download
def count_current(text_count):
    if (os.path.exists(DIRECTORY)):
        files = os.listdir(DIRECTORY)
        file_count = len(files)
        #If all texts are downloaded, exit script early
        if text_count - file_count == 0:
            print(f"Found {file_count} existing texts.. No new texts to download.")
            return file_count
        print(f"Found {file_count} existing texts.. Downloading {text_count-file_count} new texts to {DIRECTORY}.")
        return file_count
    else:
        print(f"Found {text_count}.. Downloading texts to {DIRECTORY}.")
        return 0

#Downloads and saves texts that are not already saved
def write_texts(library):
    current=1

    #Iterate upon list of texts
    for text in library:
        url = text+".pdf"
        #Get author and title from link
        title_pattern = "(?<=https:\/\/theanarchistlibrary\.org\/library\/).*?(?=\.pdf)"
        title = re.search(title_pattern,url)
        
        #Save text to file if file does not exist
        filepath = Path(DIRECTORY+title[0]+'.pdf')
        
        if os.path.exists(filepath) != True:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            response = requests.get(url)
            filepath.write_bytes(response.content)

            title = title[0].replace("-"," ")
            print(f"Downloaded {title}")
            current +=1

def main(): 
    global DIRECTORY
    DIRECTORY = "texts/"
    if len(sys.argv) == 2:
        DIRECTORY = sys.argv[1] + "/"
    library = get_texts("https://theanarchistlibrary.org/library")
    text_count = len(library)
    file_count = count_current(text_count)
    if text_count - file_count != 0:
        write_texts(library)

if __name__ == "__main__":
    main()
