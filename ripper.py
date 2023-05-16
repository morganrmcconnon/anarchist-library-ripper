import requests
import re
from pathlib import Path
import os

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

def write_texts(library):
    directory = "files/"
    
    #Check how many texts have already been downloaded and print result
    text_count = len(library)
    if (os.path.exists(directory)):
        files = os.listdir(directory)
        file_count = len(files)
        print(f"Found {file_count} existing texts.. Downloading {text_count-file_count} new texts.")
    else:
        print(f"Found {text_count}.. Downloading texts.")

    current=1

    #Iterate upon list of texts
    for text in library:
        
        url = text+".pdf"
        #Get author and title from link
        title_pattern = "(?<=https:\/\/theanarchistlibrary\.org\/library\/).*?(?=\.pdf)"
        title = re.search(title_pattern,url)
        
        #Save text to file if file does not exist
        filepath = Path(directory+title[0]+'.pdf')
        
        if os.path.exists(filepath) != True:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            response = requests.get(url)
            filepath.write_bytes(response.content)

            title = title[0].replace("-"," ")
            print(f"Downloaded {title}")
            current +=1

def main(): 
    texts_list = get_texts("https://theanarchistlibrary.org/library")
    write_texts(texts_list)

if __name__ == "__main__":
    main()
