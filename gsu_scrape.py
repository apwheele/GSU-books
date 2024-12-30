'''
Scrapping GSU
pages

Andy Wheeler
'''


import requests
import time
from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime

playwright = sync_playwright().start()

def get_terms(base='https://registration.gosolar.gsu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms'):
    url = f'{base}?searchTerm=&offset=1&max=1000'
    terms = requests.get(url)
    return terms.json()

def get_subjects(term='202401',base='https://registration.gosolar.gsu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject'):
    url = f'{base}?searchTerm=&term={term}&offset=1&max=1000'
    subs = requests.get(url)
    return subs.json()

# getting page context
# this is annoying, I know the endpoint
# but something about context returns 0 results
# so use playwright to get nicer page to query from
# this gets current year, but can query whatever
def get_page(headless=True):
    browser = playwright.chromium.launch(headless=headless)
    page = browser.new_page()
    base = 'https://registration.gosolar.gsu.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=search'
    page.goto(base)
    time.sleep(3)
    dropdown = page.query_selector('id=term-search-combobox')
    dropdown.select_text()
    for _ in range(7):
        dropdown.press('Tab')
        time.sleep(0.8)
    dropdown.press('Enter')
    time.sleep(1)
    # If want to go to older
    #dropdown.press('ArrowDown')
    dropdown.press('Enter')
    dropdown.press('Tab')
    dropdown.press('Enter')
    time.sleep(2)
    return browser, page.request


def get_class(term='202401',subject='ACCT',level='US',campus=None,
              base='https://registration.gosolar.gsu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults'):
    # getting the page context
    brow, req = get_page()
    # default subject search
    url = f'{base}?txt_level={level}&txt_subject={subject}&txt_term={term}&pageMaxSize=50'
    res = req.get(url)
    rj = res.json()
    # get total count
    totc = rj['totalCount']
    offset = 0
    res_df = []
    ldf = pd.DataFrame(rj['data'])
    res_df.append(ldf)
    left_over = totc - ldf.shape[0]
    time.sleep(2)
    while left_over > 0:
        offset += ldf.shape[0]
        url2 = url + f"&pageOffset={offset}"
        res = req.get(url2)
        rj = res.json()
        ldf = pd.DataFrame(rj['data'])
        res_df.append(ldf.copy())
        left_over -= ldf.shape[0]
        time.sleep(2)
    res_pdf = pd.concat(res_df,ignore_index=True)
    # need to close the browser
    brow.close()
    return res_pdf


# Terms
terms = get_terms()
tl = [t['code'] for t in terms]
tl = tl[0] # only worrying about 2024 for now

# Subjects
subs = get_subjects(term=tl)
sl = [s['code'] for s in subs]
#sl = ['ACCT','CRJU','LAW']
levels = ['US','UA','GS','LW'] # undergrad, associates, grad, law
#levels = ['US']
#levels = ['US','LW'] # only undergrad and law for now

#acct = get_class()
#crj = get_class(subject='CRJU')
# law school subject is always LAW

res_li = []

for l in levels:
    if l == 'LW':
        s2 = ['LAW']
    else:
        s2 = sl
    for s in s2:
        print(f'Getting level {l} and subject {s} @ {datetime.now()}')
        df = get_class(term=tl,level=l,subject=s)
        if df.shape[0] > 0:
            print(df['subject'].value_counts())
            res_li.append(df.copy())
        else:
            print(f'No results')
        time.sleep(10)

res_df = pd.concat(res_li,ignore_index=True)
res_df.to_csv('GSU_CourseInfo_Fall2024.csv',index=False)