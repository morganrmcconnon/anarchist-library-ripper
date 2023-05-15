import requests
import re
from pathlib import Path
from os.path import exists

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
    texts_list = get_texts(library)
    text_len = len(texts_list)
    print(f"Found {text_len} texts.. Downloading new texts.")

    current=1

    #Iterate upon list of texts
    for text in texts_list:
        
        url = text+".pdf"
        #Get author and title from link
        title_pattern = "(?<=https:\/\/theanarchistlibrary\.org\/library\/).*?(?=\.pdf)"
        title = re.search(title_pattern,url)
        
        #Save text to file if file does not exist
        filepath = Path("files/"+title[0]+'.pdf')
        if exists(filepath) != True:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            response = requests.get(url)
            filepath.write_bytes(response.content)

            title = title[0].replace("-"," ")
            print(f"Downloaded {title}")
            current +=1

def main():
    write_texts("https://theanarchistlibrary.org/library")

if __name__ == "__main__":
    main()
