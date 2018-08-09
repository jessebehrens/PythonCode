#Import Packages 
#Python version 3.6.1
import os
import re
import string
from pdfrw import PdfReader #0.4
from bs4 import BeautifulSoup #4.6.1
from urllib.request import urlopen

#Create a function that will open the pdf file using pdfrw and pull the title
#from the metadata
def gettitle(path, file):
    try:
        pdffile=os.path.join(path,file)
        title = PdfReader(pdffile).Info.Title
        title = re.sub('[\W_]', '', str(title))
    except:
        title = 'None'
    return title

#Some books do not have metadata.  Since these are all SAS books - we will the sas store
#and see if we can look up the book names directly.
#Some books are not listed on the website - when there is more than 1 book returned as a 
#result, then we know that a match not found.  When the search returns exactly 1 book,
#it's a match

def gettitleisbn(isbn):
    url='https://www.sas.com/store/search.ep?storeCode=SAS_US&keyWords='+isbn+'&submit=Search'
    page = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    try:
        taglist=soup.find_all('div', attrs={'class': 'title'})
        countTags=sum([ 1 for i in taglist])
        
        if countTags==1:
            name_box = soup.find('div', attrs={'class': 'title'}).text
            title=re.sub('[\W_]', '', str(name_box))
        else:
            title='None'
            
        return title
        
    except:
        title='None'

#List the location where the books live on the PC.  Make sure the path
#only includes pdfs that need to be converted, they are sas publishing,
#and no other files are in the folder
path=r'c:\sasbooks'

ISBN=[]

for file in os.listdir(path):
    NewName=gettitle(path,file) 

    if not NewName or NewName=='None' or NewName is None:
        ISBN.append(file.replace('.pdf',''))

    else:
        if not os.path.exists(os.path.join(path,NewName + ".pdf")):
            os.rename(os.path.join(path,file),os.path.join(path,NewName + ".pdf"))
        else:
            ISBN.append(file.replace('.pdf',''))

for book in ISBN:
    NewName=gettitleisbn(book)
    if not os.path.exists(os.path.join(path,NewName + ".pdf")) and NewName !='None':
        os.rename(os.path.join(path,book+'.pdf'),os.path.join(path,NewName + ".pdf"))
    else:
        print('Unable to find title for', book)