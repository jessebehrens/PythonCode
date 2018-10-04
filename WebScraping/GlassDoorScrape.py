import os
from bs4 import BeautifulSoup #4.5.3
import pandas as pd #0.19.2
import re #2.2.1
import requests #2.12.4
from requests.packages.urllib3.exceptions import InsecureRequestWarning #2.12.4

numPages=5000                              #The number of pages to be downloaded
htmlloc='C:\glassdoor\jesse';              #The output for the html files
outputloc='C:\glassdoor\output\output.csv' #The location for the CSV with the final output

output=[]
final_list=[]


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #Disable SSL Warning

for x in range(1,numPages):
    
    url='http://www.glassdoor.com/Reviews/Google-Reviews-E9079_P'+str(x)+'.htm'                #URL For website - needs to be edited based on company
    file='out'+ str(x) +'.html'
    fileloc=os.path.join(htmlloc,file)
    
    r = requests.get(url, headers=headers, allow_redirects=True, verify=False)  # to get content after redirection
    pdf_url = r.url # 'https://media.readthedocs.org/pdf/django/latest/django.pdf'
    with open(fileloc, 'wb') as f:
        f.write(r.content)

    soup = BeautifulSoup(open(fileloc, encoding='utf8'), "html.parser")
    taglist=soup.find('ol', attrs={'class': 'empReviews'})

    for li in taglist.find_all('li',attrs={'class': re.compile(' empReview cf* ')}):
        
        output=[]
        
        output.append(file)
        
        try:             
            output.append(li.find('time').text)
        except:
            output.append(li.find('time'))

        try:    
            output.append(li.find('h2').text)
        except:
            output.append(li.find('h2'))
            
        output.append(str(li.find('span',attrs={'class': 'rating'}))[54:57])
            
        try:
            output.append(li.find('span',attrs={'class': 'authorJobTitle reviewer'}).text)
        except:
            output.append(li.find('span',attrs={'class': 'authorJobTitle reviewer'}))
            
        try:
            output.append(li.find('span',attrs={'class': 'authorLocation'}).text)
        except:
            output.append(li.find('span',attrs={'class': 'authorLocation'}))
            
        try:
            output.append(li.find('p',attrs={'class': ' tightBot mainText'}).text)
        except:
            output.append(li.find('p',attrs={'class': ' tightBot mainText'}))
        
        try:
            output.append(li.find('p',attrs={'class':   re.compile(' pros mainText*')}).text)
        except:
            output.append(li.find('p',attrs={'class':   re.compile(' pros mainText*')}))
        
        try:
            output.append(li.find('p',attrs={'class':   re.compile(' cons mainText*')}).text)
        except:
            output.append(li.find('p',attrs={'class':   re.compile(' cons mainText*')}))

        try:
            output.append(li.find('p',attrs={'class': " adviceMgmt mainText truncateThis wrapToggleStr"}).text)
        except:
            output.append(li.find('p',attrs={'class': " adviceMgmt mainText truncateThis wrapToggleStr"}))
        final_list.append(output)
    
dataframe=pd.DataFrame(final_list,columns=['File','Time','Title','StarRating','JobTitle','Location','Time','Pros','Cons','AdviceForManagement'])
dataframe.to_csv(outputloc,encoding='utf-8', index=False)
