'''
This is code to scrape the bookstore
data, 

1 need the google chrome extension
  and chrome to be default browswer

2 need to figure out the position
  of your browswer for the code to run

 - positions for
   - middle of page
   - X for chrome (to close)
   - second tab location (to close tab)
   - 

'''

import time
import webbrowser as w
from tkinter import Tk
from pynput import mouse, keyboard
import os
import pandas as pd

# Locations on screen
refresh = (-1797,88)
close_tab = (-1227,29)
offer_banner = (-1078,633)
middle_page = (-1133, 518) #(-977, 544)
close_chrome = (-16,17)

# Current sheet to get
cl = 'GSU_CourseInfo_Fall2024.csv'

# Go look up a course and in the URL bar to get this info
# term ID
tid = '100083441'

# program ID for the different campuses
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

rev_campus = {v:k for k,v in campus.items()}

def refresh_tab(refresh_loc=refresh):
    mo = mouse.Controller()
    orig_position = mo.position
    mo.position = refresh_loc
    mo.press(mouse.Button.left)
    mo.release(mouse.Button.left)
    mo.position = orig_position

def close_tab(close_tabloc=close_tab):
    mo = mouse.Controller()
    orig_position = mo.position
    mo.position = close_tabloc
    mo.press(mouse.Button.left)
    mo.release(mouse.Button.left)
    mo.position = orig_position

def get_clip(clear=False):
    try:
        r = Tk()
        r.withdraw()
        res = r.selection_get(selection="CLIPBOARD")
        if clear:
            r.clipboard_clear()
        r.destroy()
        #print("Success")
        print(res)
    except:
        res = 'Failed'
        print('Failed')
    return res

def parse_books(s):
    if (s == '') | (s == 'Failed'):
        return []
    else:
        b = s.split("\n")[1:]
        bf = [r.split("\t") for r in b]
        return bf

# This is the middle of my left screen
def cm(mid_loc=middle_page,offer=offer_banner):
    mo = mouse.Controller()
    orig_position = mo.position
    mo.position = offer
    mo.press(mouse.Button.left)
    mo.release(mouse.Button.left)
    time.sleep(4)
    mo.scroll(0,2)
    mo.position = mid_loc
    ky = keyboard.Controller()
    ky.press(keyboard.Key.enter)
    ky.release(keyboard.Key.enter)
    mo.position = orig_position

def close_chrome(close_loc=close_chrome):
    #os.system("taskkill /im chrome.exe /f")
    mo = mouse.Controller()
    orig_position = mo.position
    mo.position = close_loc
    mo.press(mouse.Button.left)
    mo.release(mouse.Button.left)
    mo.position = orig_position

# Make urls from spreadsheet
data = pd.read_csv(cl)
data.sort_values(by='enrollment',ascending=False,inplace=True,ignore_index=True) # get more common classes first


def make_url(data=data):
    base = 'https://www.bkstr.com/georgiastatestore/course-materials-results?shopBy=course&divisionDisplayName=&departmentDisplayName='
    base = base + data['subject']
    base = base + '&courseDisplayName=' + data['courseNumber'].astype(str)
    base = base + '&sectionDisplayName=' + data['courseReferenceNumber'].astype(str)
    base = base + '&programId=' + data['campusDescription'].replace(campus)
    base = base + '&termId=' + tid
    # only return urls that are in the campus list
    #camp = (data['campusDescription'].replace(campus) != '')
    camp = (data['campusDescription'].replace(campus) == '403')
    return base[camp].tolist()

urls = make_url()

if os.path.exists('FailURLs.csv'):
    fail_url = pd.read_csv('FailURLs.csv')
    fail_url = fail_url[0].tolist()
else:
    fail_url = []

if os.path.exists('BookPrice.csv'):
    old_data = pd.read_csv('BookPrice.csv')
    old_data.columns = ['subject','courseNumber','courseReferenceNumber','campusDescription'] + old_data.columns.tolist()[4:]
    old_data['campusDescription'] = old_data['campusDescription'].astype(str).replace(rev_campus)
    old_urls = make_url(old_data)
    urls = [u for u in urls if u not in old_urls] # this keeps the order
    urls = [u for u in urls if u not in fail_url]

data = []
totd = 0
#clip = get_clip(clear=True)
clip = ""

print(f'Total urls left to go {len(urls)}')

sub_sample = 600

for i,u in enumerate(urls[:sub_sample]):
    print(f'Getting {i+1} out of {sub_sample}')
    # Open up webpage
    print("")
    print(u)
    w.open(u,new=0)
    # sleep for a few seconds
    if totd == 0:
        time.sleep(10)
    else:
        time.sleep(6)
    # Click middle of page & enter
    # needs Chrome extension
    cm()
    # get the data
    prior_clip = clip
    clip = get_clip()
    # sometimes can get stuck and not refresh the clipboard
    if clip == prior_clip:
        totd += 1
        #get_clip(clear=True)
    if clip == 'Failed':
        refresh_tab()
        time.sleep(10)
        clip = get_clip()
        if clip == 'Failed':
            fail_url.append(u)
            close_tab()
            totd += 1
        else:
            data += parse_books(clip)
            close_tab()
    else:
        data += parse_books(clip)
        close_tab()
    if totd > 10:
        print('Too many failures, exiting')
        break

res_data = pd.DataFrame(data)
res_data.to_csv('TempDownload.csv',index=False)

if os.path.exists('BookPrice.csv'):
    old_data = pd.read_csv('BookPrice.csv')
    # If no books, column length will be smaller
    res_data.columns = old_data.columns[:len(list(res_data))]
    comb_data = pd.concat([old_data,res_data])
    comb_data.drop_duplicates(inplace=True,ignore_index=True)
else:
    comb_data = res_data.copy()

comb_data.to_csv('BookPrice.csv',index=False)
print(res_data)

if len(fail_url) > 0:
    fail_data = pd.DataFrame(fail_url)
    fail_data.to_csv('FailURLs.csv',index=False)

# Clearing out the clipboard
get_clip(clear=True)