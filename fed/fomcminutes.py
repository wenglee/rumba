
from io import BytesIO
from io import StringIO
import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import time
from selenium import webdriver
import urllib.request

with open('src2.txt','r') as infile:
    urls=infile.read().splitlines()
    urls = list(filter(None, urls))

driver = webdriver.Firefox()
# urls=["https://www.federalreserve.gov/newsevents/pressreleases/monetary20091005b.htm"]
# urls=["https://www.federalreserve.gov/newsevents/pressreleases/monetary20161018a.htm"]
#https://www.federalreserve.gov/monetarypolicy/fomcminutes20111213.htm# 20111122a.htm

# urls=["https://www.federalreserve.gov/newsevents/pressreleases/monetary20181219b.htm"]
#urls=["https://www.federalreserve.gov/newsevents/pressreleases/monetary20190130b.htm"]
def download_minutes(driver, url):
    filename= 'fedminutes/' + url.split('/')[-1]

    #url = "https://www.federalreserve.gov/newsevents/pressreleases/monetary20190220a.htm"
    driver.get(url)

    time.sleep(2)
    try:
        htmlelem= driver.find_element_by_xpath(
            ".//a[text()='HTML']"
        )
        if htmlelem is not None:
            htmlelem.click()

            article = driver.find_element_by_id("article")

            with open(filename, 'w') as f:
                f.write(article.text)
    except:
        try:
            htmlelem= driver.find_element_by_xpath(
                ".//a[text()='Attachment (PDF)']"
            )
            if htmlelem is not None:
                htmlelem.click()
            pdflink = driver.current_url

            pdf = 'fedminutes/' + pdflink.split('/')[-1]
            urllib.request.urlretrieve(pdflink, pdf)
            rsrcmgr = PDFResourceManager()
            sio = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            fp = open(pdf, 'rb')
            for page in PDFPage.get_pages(fp):
                interpreter.process_page(page)
            fp.close()
            text = sio.getvalue()
            text = text.replace(chr(272), " ")
            with open(pdf +'.txt', 'w') as f:
                f.write(text)
            os.unlink(pdf)

        except:
            try:
                htmlelem = driver.find_element_by_xpath(
                    ".//a[text()='Projections (PDF)']"
                )
                if htmlelem is not None:
                    htmlelem.click()
                pdflink = driver.current_url

                pdf = 'fedminutes/' + pdflink.split('/')[-1]
                urllib.request.urlretrieve(pdflink, pdf)

            except:

                try:
                    htmlelem = driver.find_element_by_xpath(
                        ".//a[text()='Statement on Longer-Run Goals and Monetary Policy Strategy (PDF)']"
                    )
                    if htmlelem is not None:
                        htmlelem.click()
                    pdflink = driver.current_url

                    pdf = 'fedminutes/' + pdflink.split('/')[-1]
                    urllib.request.urlretrieve(pdflink, pdf)
                    rsrcmgr = PDFResourceManager()
                    sio = StringIO()
                    codec = 'utf-8'
                    laparams = LAParams()
                    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
                    interpreter = PDFPageInterpreter(rsrcmgr, device)

                    fp = open(pdf, 'rb')
                    for page in PDFPage.get_pages(fp):
                        interpreter.process_page(page)
                    fp.close()
                    text = sio.getvalue()
                    text = text.replace(chr(272), " ")
                    with open(pdf + '.txt', 'w') as f:
                        f.write(text)
                    os.unlink(pdf)

                except:
                    try:
                        article = driver.find_element_by_id("article")

                        with open(filename,'w') as f:
                            f.write(article.text)
                    except:
                        try:
                            article = driver.find_element_by_id("leftText")

                            with open(filename, 'w') as f:
                                f.write(article.text)
                        except:
                            try:
                                with open(filename, 'w') as f:
                                    f.write(driver.find_element_by_name('body').text)
                            except:
                                with open(filename, 'w') as f:
                                    f.write(driver.find_element_by_name('pre').text)

for url in urls:
    download_minutes(driver, url)
driver.close()
