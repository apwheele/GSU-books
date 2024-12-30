'''
Analyzing book store data
'''

import pandas as pd
import re
import numpy as np
import json
from collections import defaultdict


enroll = pd.read_csv('GSU_CourseInfo_Fall2024.csv')
books = pd.read_csv('BookPrice.csv')

campus = {'Atlanta':'403',
          'Alpharetta':'3461',
          'Clarkston -Associates courses':'1390',
          'Decatur -Associates courses':'1393',
          'Dunwoody -Associates courses':'1394',
          'FinTech Academy':'',
          'Foreign Campus':'',
          'GA OnMyLine':'3540',
          'Georgia Film Academy':'',
          'Newton -Associates courses':'1745',
          'Off Campus-Perimeter':'',
          'Off Campus-Tech &amp; USG Fee only':'',
          'Off-Campus with Mand. Fees':'',
          'Online':'3540',
          'Online - Atl GR (Mand. Fees)':'403',
          'Online - Atl US (Mand. Fees)':'403'}

enroll['CampusNum'] = enroll['campusDescription'].replace(campus)
enroll = enroll[enroll['CampusNum'] == '403'].reset_index(drop=True)

book_cols = ['SUBJECT','COURSE','SECTION','CAMPUS','BOOKTITLE','REQUIRED',
             'PRICES','DET1','DET2','DET3','DET4','DET5','DET6','DET7']
books.columns = book_cols

mfields = {'subject':'SUBJECT',
           'courseNumber':'COURSE',
           'courseReferenceNumber':'SECTION',
           'CampusNum':'CAMPUS'}

enroll.rename(columns=mfields,inplace=True)
fields = list(mfields.values()) + ['courseTitle','maximumEnrollment','enrollment']

for v in list(mfields.values())[1:]:
    enroll[v] = enroll[v].astype(str)
    books[v] = books[v].astype(str)


# merging enroll totals to the bookstore data
books = books.merge(enroll[fields],how='left',on=list(mfields.values()))

# Parsing out the prices for books, calculate min/max
pattern = r"[$](\d+\.\d{2})"

def minmax(x):
    res = re.findall(pattern,str(x))
    if res:
        res = [float(r) for r in res]
        return [min(res),max(res)]
    else:
        return [None,None]

mm = books[['PRICES']].fillna('').apply(minmax,axis=1,result_type='expand')
books[['MinPrice','MaxPrice']] = mm

# Logic to get min/max for required choose only 1 of 3
books['MinVal'] = books['MinPrice']*books['enrollment']
books.sort_values(by='MinVal',ascending=False,inplace=True,ignore_index=True)
req_books = books[books['REQUIRED'] == 'Required'].reset_index(drop=True)

def js(x):
    x1 = []
    for i in x:
        if i:
            i = i.replace('"',"'")
            if i.count(":") > 1:
                i2 = i.split(":")
                i2 = '"' + i2[0] + '":"' + ' '.join(i2[1:]) + '"'
                x1.append(i2)
            else:
                x1.append('"' + str(i).replace(": ",'":"') + '"')
    jsv = "{" + ', '.join(x1) + "}"
    return json.loads(jsv)

full_info = books[['DET1','DET2','DET3','DET4','DET5','DET6','DET7']].fillna('').apply(js,axis=1)

books['ISBN'] = full_info.apply(lambda x: x.get('ISBN',''))
books['PUBLISHER'] = full_info.apply(lambda x: x.get('Publisher',''))

book_sel = ['SUBJECT','COURSE','SECTION','courseTitle','BOOKTITLE','ISBN','PUBLISHER',
            'REQUIRED','PRICES','MinPrice','enrollment','MinVal']

# What this does is for required 1 of X, takes the lowest price book
sort_v = ['SUBJECT','COURSE','SECTION','REQUIRED','MinPrice']
books.sort_values(by=sort_v,ascending=True,inplace=True,ignore_index=True)
books.drop_duplicates(subset=sort_v[:-1],keep='first',inplace=True,ignore_index=True)

# replacing required/recommended
reprr = {'Required Choose Only 1 of 2': 'Required',
         'Required': 'Required',
         'Required Choose Only 1 of 3': 'Required',
         'Recommended': 'Recommended',
         'Required Choose Only 1 of 1': 'Required',
         'Required Choose Only 0 of 3': 'Recommended'}

books['REQUIRED'] = books['REQUIRED'].replace(reprr).fillna('')

books.sort_values(by='MinVal',ascending=False,inplace=True,ignore_index=True)
books[book_sel].to_csv('BookInfo_Fall2024.csv',index=False)




# Reshape multiple books onto same line
# When Required Choose Only 1 of 2, get min/max
mf = list(mfields.values()) + ['maximumEnrollment','enrollment','REQUIRED']

def agg_book(x):
    if x['required'] == 'Required':
        minx = 
    elif

lr = []
g = books.groupby(mf,as_index=False)['MinPrice'].min()
req = ~g['REQUIRED'].isin(['Recommended','Required Choose Only 0 of 3'])
g['TotVal'] = req*g['enrollment']*g['MinPrice']
g = g.groupby(mf[:-1],as_index=False)['TotVal'].sum()
g.sort_values(by='TotVal',ascending=False,inplace=True,ignore_index=True)
g['PricePerStudent'] = g['TotVal']/g['enrollment']
