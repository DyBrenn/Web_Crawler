# Web_Crawler
Hello and welcome to my web crawler. It's written in python and extracts data from a website using requests and beautifulsoup4. Data is extracted from the last table on pge.com.
Data extracted includes company names, dates, and injection / withdrawl of funds which is stored using net injection (injection - withdrawl).
The data is then stored and formatted in excel using xlwt which is then emailed to a mutable list of emails using email.mime. All of this represents the pge_crawl script.

The crawl script is run be another script called pge_modified which checks if the most recent date in the relevant table has changed (meaning new data has been updated to the table).
This is done by storing the most recent date in a text file and crawling the website to extract the most recent datas date, and comparing it to date in the text file. If different, the pge_crawl script is run.
This can be automated to run at a set time every day multiple ways, but I used the built-in windows task scheduler to run pge_modified every 10 minutes between 6 to 9 a.m.
