from bs4 import BeautifulSoup
import requests
import xlwt
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

#request relevant page, in this case pge.com
browser = requests.get("http://www.pge.com/pipeline/operations/cgt_pipeline_status.page?#storage_activity")
soup = BeautifulSoup(browser.content,'lxml')
data = {}
date = []
date2 = []
table = soup.find_all('table')[8]
#flag keeps track if we will be adding or subtracting funds from the daily update
flag = False
exp = False
row = table.find_all('tr')[0]
#counter to track where to insert data from table becuase it must match the date
i = -1
for date in row.find_all('th'):
    #track three most recent dates in table
    for j in date:
        if isinstance(j, str):
            date[i] = j
    if i>=0:
        #for some reason regular date list wouldn't work so I made date2
        date2.append(date[i])
    i += 1
for tr in table.find_all('tr'):
    if tr.th is not None:
        #Track if adding or withdrawing funds from company value and break when we don't need further data
        if tr.th.string == 'Injection':
            flag = True
        if tr.th.string == 'Withdrawal':
            flag = False
        if tr.th.string == 'Balancing Gas':
            break
    count = 0
    name = None
    for td in tr.find_all('td'):
        #PG&E Storage company name can't be extracted from table so we create it ourselves
        if td.string == None:
            if exp == True:
                name = 'PG&E Storage'
                exp = False
            else:
                exp = True
        if count == 0:
                if name == None:
                    #Pipeline balancing contains injection and withdrawl in name so we reduce name so we can add and subtract funds into same dictionary
                    if td.string == 'Pipeline Balancing Injection' or td.string == 'Pipeline Balancing Withdrawal':
                        name = 'Pipeline Balancing'
                    else:
                        name = td.string
                if flag == True:
                    if name != None:
                        data[name] = []
        else:
            #adds funds to dictionary with company key
            if flag == True:
                data[name].append(int(td.string))
            #subtracts funds from dictionary with company key
            if flag == False:
                data[name][count-1] -= int(td.string)
        count += 1
#records data in excel file
book = xlwt.Workbook()
ws = book.add_sheet('pge_data')
r = 0
c = 1
done = False
#formats data into excel
while done != True:
    for i in date2:
        ws.write(r,c,i)
        c+=1
    c=0
    r=1
    for i in data:
        ws.write(r,c,i)
        for j in data[i]:
            c+=1
            ws.write(r,c,j)
        r+=1
        c=0
    done = True
book.save('pge_data.xls')
text = ''
for i in date2:
    text+=str(i)
    text+=' '
text+='\n'
for i in data:
    text+=str(i)
    text += ' '
    for j in data[i]:
        text+=str(j)
        text+= ' '
    text+='\n'
#sends email with excel data and text data
def send_mail(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    with open(files, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(files)
        )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(files)
        msg.attach(part)


    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('Username','Password')
    server.sendmail(send_from, send_to, msg.as_string())
    server.quit()

send_mail('from_email', ['list_of_to_email'], 'PGE.com update', text, 'C:\\Users\\Dylan\\Desktop\\HT_Backup\\UConn\\Code\\PGE_data.xls')
