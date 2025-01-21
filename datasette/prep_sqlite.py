'''
prepping a sqlite database
for a datasette app
'''

import pandas as pd
import sqlite3

con = sqlite3.connect("books.db")

tf2024 = pd.read_csv('../Data/BookInfo_Fall2024.csv')
ts2025 = pd.read_csv('../Data/BookInfo_Spring2025.csv')

tf2024['Semester'] = '2024-Fall'
ts2025['Semester'] = '2025-Spring'


full = pd.concat([tf2024,ts2025])
full.to_sql('books',con=con,if_exists='replace',index=False)


# Lets make some views

view_topbooks = '''
CREATE VIEW topbooks AS
SELECT
  MIN(BOOKTITLE) AS Title,
  ISBN,
  MIN(PUBLISHER) AS Publisher,
  SUM(MinVal) AS TotalCost,
  MIN(MinPrice) AS MinPrice,
  SUM(enrollment) AS TotalStudents,
  COUNT(*) AS Sections
FROM books
WHERE REQUIRED = 'Required'
GROUP BY ISBN
ORDER BY TotalCost DESC
'''

con.execute(view_topbooks)


top_classes = '''
CREATE VIEW topclasses AS
SELECT
  SUBJECT,
  COURSE,
  MIN(courseTitle) AS courseTitle,
  SUM(MinVal) AS TotalCost,
  MIN(MinPrice) AS MinPrice,
  SUM(enrollment) AS TotalStudents
FROM books
WHERE REQUIRED = 'Required'
GROUP BY SUBJECT, COURSE
ORDER BY TotalCost DESC
'''

con.execute(top_classes)