'''
conda create --name dash2 python=3.10 panel holoviews hvplot pandas folium matplotlib 
pip install param==1.13.0

To check local

panel serve panel_dashboard.py --dev --show

To create WASM app

panel convert panel_dashboard.py --to pyscript --out pyscript

Then need to change to read in data from weburl
'''

import panel as pn
import pandas as pd
from bokeh.models.widgets.tables import NumberFormatter

pn.extension('tabulator')

table_css = '''
/* Alternate row coloring */
tr:nth-child(even) {
  background-color: #DDDDDD;
}

tr:nth-child(odd) {
  background-color: #FFFFFF;
}

/* First column larger */
td:nth-child(2), th:nth-child(2) {
  width: 150px;
}

/* Right align columns example
td:nth-child(2), td:nth-child(3),
th:nth-child(2), th:nth-child(3) {
  text-align: right;
}

*/

/* Background color of header */
th {
  background-color: #999999
}

/* No borders in Table */
/* No vertical borders in header and cells */
table, th, td {
  font-family: Menlo,Monaco,Consolas,"Courier New",monospace;
  border: none;
  border-collapse: collapse;
  border-left: none;
  border-right: none;
  border-bottom: none;
  border-top: none;
}

/* Cell padding */
th, td {
  padding: 0% 2% 0% 2%;
}
'''

html = f'''<p>This is a demonstration dashboard for the GSU Book scraping project. See <a href="https://github.com/apwheele/GSU-books" target="_blank">here</a> 
how data is generated and categorized based. If you are interested in similar services, feel free 
<a href="https://crimede-coder.com/contact" target="_blank">to get in touch</a>.</p>
'''



html_pane = pn.pane.HTML(html,width=450)

tf2024 = pd.read_csv('../Data/BookInfo_Fall2024.csv')
ts2025 = pd.read_csv('../Data/BookInfo_Spring2025.csv')

tf2024['Semester'] = '2024-Fall'
ts2025['Semester'] = '2025-Spring'


classes = pd.concat([tf2024,ts2025])
classes['ISBN'] = classes['ISBN'].astype(str).str.replace(".0","").str.replace("nan","")
classes.sort_values(by='MinVal',ascending=False,ignore_index=True,inplace=True)
classes['SECTION'] = classes['SECTION'].astype(str)
classes['COURSE'] = classes['COURSE'].astype(str)


classes_descript = {}
books_descript = {}



books = classes.groupby(['BOOKTITLE','ISBN','PUBLISHER'],as_index=False)[['enrollment','MinVal']].sum()
books['enrollment'] = books['enrollment'].astype(int)
books.sort_values(by='MinVal',ascending=False,ignore_index=True,inplace=True)

tab_mon = {'type': 'money', 
           'decimal': ",",
           "symbol": "$"}


tabulator_formatters = {
    'minPrice': NumberFormatter(format='$0,0.00'),
    'minValue': NumberFormatter(format='$0,0[.]00'),
}

class_width = {'SUBJECT': 35, 'COURSE': 15, 'SECTION': 15, 'courseTitle': 60, 'BOOKTITLE': 70, 
               'ISBN': 50,
               'PUBLISHER': 60, 'REQUIRED': 5, 'PRICES': 25, 'MinPrice': 35, 'enrollment': 35,
               'minVal': 20, 'Semester': 20}
book_width = {'A': 50, 'B': 50, 'C': 70, 'D': 130}

tab_classes = pn.widgets.Tabulator(classes, width=2000, layout='fit_columns',
                                 pagination='local',page_size=10, header_filters=True, show_index=False,
                                 formatters=tabulator_formatters,
                                 theme='bootstrap5', theme_classes=['thead-dark', 'table-sm'])

tab_books = pn.widgets.Tabulator(books, layout='fit_columns',
                                 pagination='local',page_size=10, header_filters=True, show_index=False,
                                 formatters=tabulator_formatters,
                                 theme='bootstrap5', theme_classes=['thead-dark', 'table-sm'])

pn.extension(raw_css=[table_css],
             css_files=['https://crimede-coder.com/assets/crimedecoder.css'])


#sidebar = pn.layout.WidgetBox(html_pane)

'''
span.tabulator-paginator {
    text-align: left;
}
'''

main = pn.Tabs(('Classes', pn.Column(pn.Row(tab_classes), sizing_mode='stretch_both')),
               ('Books', pn.Column(pn.Row(tab_books), sizing_mode='stretch_both')),
               ('Info', pn.Column(pn.Row(html_pane), sizing_mode='stretch_both')))


pn.Row(main).servable();