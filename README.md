# GSU-books

Scraping data to identify high cost GSU books, the Wallace Method.

Project supported by the Georgia State University Foundation Trustees.

![](https://www.gsu.edu/wp-content/themes/gsu-flex-2/images/logo.png)

Andrew Wheeler, Scott Jacques

# Overview of the Project

We are identifying courses that make students spend exhorbant amount of money on books. These courses GSU should consider licensing the materials for all students at a much lower cost. Here is a snap-shot of the books and materials that students cumulatively spent over $100,000 in Fall of 2024:

| BOOKTITLE                                                                                                                 | ISBN          | Enroll | Price per Book | Total Cost |
| ------------------------------------------------------------------------------------------------------------------------- | ------------- | ------ | -------------- | ---------- |
| MyLab Math with Pearson eText Access Code (18 weeks) for College Algebra: Concepts Through Functions                      | 9780138120887 | 1,281  | 120.00         | 153,720.00 |
| SCOM 1000: FOLLETT DPF CUSTOM SITE ECOMM Connect for Human Communication: A Critical Reader 180 DAYS ACCESS ENTRP         | 9781266712623 | 1,651  | 85.00          | 140,335.00 |
| Custom Authoring Bundle: Understanding the American Way of Government & Politics                                          | 9781774947180 | 1,779  | 75.00          | 133,425.00 |
| Modified Mastering Physics with Pearson eText -- Standalone Access Card -- for College Physics: A Strategic Approach      | 9780134724744 | 657    | 200.00         | 131,400.00 |
| GEORGIA STATE UNIVERSITY- SCOM 2050: FOLLETT CUSTOM SITE CCS ECOMM BILLING Connect for Introduction to Mass Communication | 9781266454493 | 1,207  | 100.00         | 120,700.00 |
| Aventuras 6e Supersite Plus + WebSAM (5M)                                                                                 | 9781543338713 | 767    | 145.50         | 111,598.50 |
| GEORGIA STATE UNIVERSITY ACCT 2101                                                                                        | 9781266245626 | 1,123  | 96.00          | 107,808.00 |
| Georgia State University ECON 2105 Principles of Economics                                                                | 9781265679767 | 1,969  | 53.50          | 105,341.50 |


# Code

The code is organized into three parts:

 - `gsu_scrape.py` scrapes the class registry data from the GSU website, including total enrollments
 - `scrape_bookstore.py` scrapes the data from the bookstore on prices. This requires setting up your computer to the coordinates and installing a Google chrome extension, see the `TutorialChrome.pptx` file.
 - `data_analysis.py`, this combines the two data sources for an easier to see spreadsheet.

See the `BookInfo_Fall2024.xlsx` file for pivot tables showing cost breakdowns and high priced books in 2024.


