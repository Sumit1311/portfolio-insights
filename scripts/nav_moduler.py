import psycopg2
import datetime
from ast import literal_eval
import urllib
import urllib.parse
import urllib.request
import os
import os.path
from ast import literal_eval
import logging
import sys

now = datetime.datetime.now().strftime("%d%m%Y")
log_file_name='portfolio_tracking_calling_block'+now+'.log'
logging.basicConfig(filename=os.path.join("log",'portfolio_insights_'+now+'.log'),format='%(asctime)s:%(levelname)s:%(message)s',level=logging.DEBUG)

class db_connection:
    con = psycopg2.connect("dbname="+os.environ['DB_NAME']+" user="+os.environ['DB_USER']+" host="+os.environ['DB_HOST']+" port="+os.environ['DB_PORT']+" password="+os.environ['DB_PASS'])
    cur = con.cursor()
    def executequery(self, query):
        self.query=query
        self.cur.execute(query)
        return_data=self.cur.fetchall()
        return return_data
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    try:
        url=''
        def handle_starttag(self, tag, attrs):
            if tag == 'input':
                value=''
                name=''
                for attr in attrs:
                    if attr[0] == 'name':
                        name=attr[1]
                    if attr[0] == 'value':
                        value=attr[1]
                if value == '':
                    value='default'
                if name in ['__EVENTVALIDATION','__VIEWSTATE'] and value not in ['deafult',None]:
                    tag_pair=(name, value)
                    #print(self.url)
                    #print(tag_pair)
                    logging.info('connecting to database')
                    con = psycopg2.connect("dbname="+os.environ['DB_NAME']+" user="+os.environ['DB_USER']+" host="+os.environ['DB_HOST']+" port="+os.environ['DB_PORT']+" password="+os.environ['DB_PASS'])
                    cur = con.cursor()
                    logging.info('successfully connected to database')
                    update_session_variables="UPDATE public.session_variables SET var_value=%s WHERE var_site=%s and var_name=%s and var_type='FormFields' and is_active='Y'"
                    cur.execute(update_session_variables,(value,self.url,name))
                    logging.debug('Updated %s ',name)
                    con.commit()
                    cur.close()
                    con.close()
                    logging.info('Cosed connection to database')
    except Exception as e:
        logging.exception("Following is the exception occured: %s", e)
        #print(e)
        sys.exit(11)

class bse_ops:
    logging.info('Inside bse_ops class')
    bse_hist_data_uri="https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0"
    bse_hist_data_uri_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

    bse_hist_data_uri_formFields = (
        (r'__EVENTTARGET', r'ctl00$ContentPlaceHolder1$lnkDownload'),
        (r'__EVENTARGUMENT', r''),
        (r'__VIEWSTATE', r'/wEPDwUJNzQ4NDIzODI1D2QWAmYPZBYCAgMPZBYCAgEPZBYOAhcPDxYCHgRUZXh0BQxTdG9jayBQcmljZXNkZAIbDw8WAh8ABQxTdG9jayBQcmljZXNkZAIfDw8WAh8AZWRkAiEPFgIeBXN0eWxlBQlkaXNwbGF5OjtkAiUPFgIfAQUJZGlzcGxheTo7FgYCDw8QDxYGHg1EYXRhVGV4dEZpZWxkBQhZZWFyVGV4dB4ORGF0YVZhbHVlRmllbGQFCVllYXJWYWx1ZR4LXyFEYXRhQm91bmRnFgIeCG9uQ2hhbmdlBQpvbkNoYW5nZSgpEBUdBFlZWVkEMjAxOAQyMDE3BDIwMTYEMjAxNQQyMDE0BDIwMTMEMjAxMgQyMDExBDIwMTAEMjAwOQQyMDA4BDIwMDcEMjAwNgQyMDA1BDIwMDQEMjAwMwQyMDAyBDIwMDEEMjAwMAQxOTk5BDE5OTgEMTk5NwQxOTk2BDE5OTUEMTk5NAQxOTkzBDE5OTIEMTk5MRUdBFlZWVkEMjAxOAQyMDE3BDIwMTYEMjAxNQQyMDE0BDIwMTMEMjAxMgQyMDExBDIwMTAEMjAwOQQyMDA4BDIwMDcEMjAwNgQyMDA1BDIwMDQEMjAwMwQyMDAyBDIwMDEEMjAwMAQxOTk5BDE5OTgEMTk5NwQxOTk2BDE5OTUEMTk5NAQxOTkzBDE5OTIEMTk5MRQrAx1nZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAhMPEA8WBh8CBQhZZWFyVGV4dB8DBQlZZWFyVmFsdWUfBGcWAh8FBRBvbkNoYW5nZVllYXJseSgpEBUdBFlZWVkEMjAxOAQyMDE3BDIwMTYEMjAxNQQyMDE0BDIwMTMEMjAxMgQyMDExBDIwMTAEMjAwOQQyMDA4BDIwMDcEMjAwNgQyMDA1BDIwMDQEMjAwMwQyMDAyBDIwMDEEMjAwMAQxOTk5BDE5OTgEMTk5NwQxOTk2BDE5OTUEMTk5NAQxOTkzBDE5OTIEMTk5MRUdBFlZWVkEMjAxOAQyMDE3BDIwMTYEMjAxNQQyMDE0BDIwMTMEMjAxMgQyMDExBDIwMTAEMjAwOQQyMDA4BDIwMDcEMjAwNgQyMDA1BDIwMDQEMjAwMwQyMDAyBDIwMDEEMjAwMAQxOTk5BDE5OTgEMTk5NwQxOTk2BDE5OTUEMTk5NAQxOTkzBDE5OTIEMTk5MRQrAx1nZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAhUPD2QWAh4Hb25DbGljawUacmV0dXJuIG9uYnRuU3VibWl0X0NsaWNrKClkAicPFgIfAQUJZGlzcGxheTo7Fg4CAQ8PFgIfAAWnATxhIHRhcmdldD0nX2JsYW5rJyBDbGFzcz0ndGFibGVibHVlbGluaycgaHJlZj0naHR0cHM6Ly93d3cuYnNlaW5kaWEuY29tL3N0b2NrLXNoYXJlLXByaWNlL3RhdGEtY29uc3VsdGFuY3ktc2VydmljZXMtbHRkL3Rjcy81MzI1NDAvJz5UQVRBIENPTlNVTFRBTkNZIFNFUlZJQ0VTIExURC48L2E+ZGQCAw8PFgIfAAUGNTMyNTQwZGQCBw8PFgIfAAULMTctTWF5LTIwMTdkZAIJDw8WAh8ABQswMS1NYXktMjAxOGRkAg0PFgIfAQUNZGlzcGxheTpub25lO2QCEQ9kFgYCAQ8WAh8BBTlwb3NpdGlvbjpyZWxhdGl2ZTt0b3A6NTAlO3RleHQtYWxpZ246Y2VudGVyO2Rpc3BsYXk6bm9uZTtkAgMPFgIeCWlubmVyaHRtbAX2lAE8dGFibGUgd2lkdGg9JzY4MHB4JyBib3JkZXI9JzAnIGNlbGxwYWRkaW5nPSc0JyBjZWxsc3BhY2luZz0nMSc+PHRyPjx0ZCB3aWR0aD0nNTBweCcgY2xhc3M9J2lubmVydGFibGVfaGVhZGVyMScgcm93c3Bhbj0nMic+RGF0ZTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0naW5uZXJ0YWJsZV9oZWFkZXIxJyByb3dzcGFuPScyJz5PcGVuPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdpbm5lcnRhYmxlX2hlYWRlcjEnIHJvd3NwYW49JzInPkhpZ2g8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J2lubmVydGFibGVfaGVhZGVyMScgcm93c3Bhbj0nMic+TG93PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdpbm5lcnRhYmxlX2hlYWRlcjEnIHJvd3NwYW49JzInPkNsb3NlPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdpbm5lcnRhYmxlX2hlYWRlcjEnIHJvd3NwYW49JzInPldBUDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0naW5uZXJ0YWJsZV9oZWFkZXIxJyByb3dzcGFuPScyJz5Oby4gb2YgPGJyLz5TaGFyZXM8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J2lubmVydGFibGVfaGVhZGVyMScgcm93c3Bhbj0nMic+Tm8uIG9mIDxici8+VHJhZGVzPC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0naW5uZXJ0YWJsZV9oZWFkZXIxJyByb3dzcGFuPScyJz5Ub3RhbCBUdXJub3ZlcjwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J2lubmVydGFibGVfaGVhZGVyMScgcm93c3Bhbj0nMic+RGVsaXZlcmFibGUgUXVhbnRpdHk8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdpbm5lcnRhYmxlX2hlYWRlcjEnIHJvd3NwYW49JzInPiUgRGVsaS4gUXR5IHRvIFRyYWRlZCBRdHkgPC90ZD48dGQgd2lkdGg9JzE2MHB4JyBjbGFzcz0naW5uZXJ0YWJsZV9oZWFkZXIxJyAgY29sc3Bhbj0nMic+KiBTcHJlYWQ8L3RkPjwvdHI+PHRyPjx0ZCB3aWR0aD0nNTBweCcgY2xhc3M9J2lubmVydGFibGVfaGVhZGVyMSc+SC1MPC90ZD48dGQgd2lkdGg9JzUwcHgnIGNsYXNzPSdpbm5lcnRhYmxlX2hlYWRlcjEnPkMtTzwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjE3LzA1LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQzMS45MDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NjAuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDI0LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ1MS4zNTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NDMuOTQ8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEsMjQsNjQwPC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40LDM4ODwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMwLDQ2LDEyLDQ2MDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+ODAsNzUxPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz42NC43OTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MzYuMDA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjE5LjQ1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MTgvMDUvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDUxLjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU2NS43NTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NDMuMDU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTM0LjEwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUzNi43MTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw4OCwxNTY8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEwLDI5ODwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjczLDA5LDY5LDUzNjwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MSw2MCwyODU8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjU1LjYyPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xMjIuNzA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjgzLjEwPC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MTkvMDUvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTQ2LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU1MC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0ODUuMjA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTA2LjgwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUwNS41NjwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NTMsMTIzPC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zLDQyMjwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEzLDMxLDAyLDYzNzwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTUsNjkzPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yOS41NDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NjQuODA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPi0zOS4yMDwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjIyLzA1LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUwNy4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NTAuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTA3LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUyOS4zMDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1MzEuMDA8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQ4LDI1NzwvdGQ+PHRkIHdpZHRoPSc3NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw4MTQ8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xMiwyMSwzOCw2MTE8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjE5LDU2MjwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NDAuNTQ8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQzLjAwPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yMi4zMDwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjIzLzA1LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUyOS41MDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NjAuNjA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTE0LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUyMC40NTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1MzMuNDM8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQ5LDU4OTwvdGQ+PHRkIHdpZHRoPSc3NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NCw0Mzg8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xMiw1NiwzMCwwNTk8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjE4LDMyNjwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MzYuOTY8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQ2LjYwPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4tOS4wNTwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjI0LzA1LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUyMi40NTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NzAuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTIyLjQ1PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU1Ny44MDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NDMuNTA8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEsMzcsMTkxPC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40LDE0MTwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjM0LDg5LDQ1LDgzNTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NzcsMDA5PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz41Ni4xMzwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NDcuNTU8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjM1LjM1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MjUvMDUvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTcyLjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYzMy4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NjcuNTU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNjE5Ljk1PC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYwMy40NjwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Myw5NSw0Njk8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjYsMjQ5PC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MSwwMiw5NSw4OCw4NjM8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMsMTgsNjI5PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz44MC41NzwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NjUuNDU8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQ3Ljk1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MjYvMDUvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNjI0LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYzNi4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NzEuMDU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTc5LjMwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYwMS4zMzwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Myw0Niw5NjY8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMsODM4PC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+OTAsMjUsNzQsMzA1PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zLDA5LDczODwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+ODkuMjc8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjY0Ljk1PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4tNDQuNzA8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz4yOS8wNS8xNzwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NzkuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTk1Ljg1PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU2Mi4zMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NzEuNTA8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTc4LjkzPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz41MCwwNjY8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMsMzA3PC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTIsOTEsMTYsNzI2PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yMSwwNDA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQyLjAyPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zMy41NTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+LTcuNTA8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz4zMC8wNS8xNzwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NzIuODU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTc1LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUyNS42MDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NTEuNzA8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTUzLjQwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40OCw3OTQ8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMsMDAzPC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTIsNDUsOTAsNjcxPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xNSw2MDA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMxLjk3PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40OS40MDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+LTIxLjE1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MzEvMDUvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTMxLjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU3MS41NTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1MjkuMDU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTQ0LjM1PC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU1MS41NTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NTAsMTE2PC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zLDg0OTwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEyLDc4LDczLDI2MzwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTgsMzk3PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zNi43MTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NDIuNTA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEzLjM1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MS8wNi8xNzwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1MzAuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTYyLjIwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUzMC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NTAuODU8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTU0LjY2PC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40NywxNDQ8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDAyPC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTIsMDQsMzYsNzc5PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yOSw3NDQ8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjYzLjA5PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zMi4yMDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MjAuODU8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz4yLzA2LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU0Mi4yNTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1ODkuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTQyLjI1PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU2MS44NTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NjkuMjQ8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQxLDk2ODwvdGQ+PHRkIHdpZHRoPSc3NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NCwxNjg8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xMCw3OCwyNSw5NjU8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjE5LDAxMTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NDUuMzA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQ2Ljc1PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xOS42MDwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjUvMDYvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTY1LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYyMC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NjAuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNjAxLjA1PC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDU4MC44NDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NzIsMjA5PC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zLDY5OTwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjE4LDYzLDU5LDg2MDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MjAsODA5PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yOC44MjwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NjAuMDA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjM2LjA1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+Ni8wNi8xNzwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw2NDQuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNzA3LjQwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYzMC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw2OTUuNDA8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNjkwLjQwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xLDUzLDY5MjwvdGQ+PHRkIHdpZHRoPSc3NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+OCw3MzI8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40MSwzNCw5MiwzMzY8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQyLDY1NzwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MjcuNzU8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjc3LjQwPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz41MS40MDwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjcvMDYvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNzAwLjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDcwMC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1ODEuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNjE1LjM1PC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYyMy40NTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MSw5NSwzOTk8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEyLDA3NDwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjUxLDI2LDIwLDIzNTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NjgsMTYyPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zNC44ODwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTE5LjAwPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4tODQuNjU8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz44LzA2LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDYxMC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw2MTAuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTE3LjcwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUyMS41MDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NDMuNDM8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEsODEsMjAzPC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xMiwyMzU8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40NiwwOCw3Nyw0NTM8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjYzLDI5MDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MzQuOTM8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjkyLjMwPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4tODguNTA8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz45LzA2LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUxNi4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1NDUuNTA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDg5LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUxMC4yNTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw1MTAuOTE8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEsMDIsODkyPC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz41LDUwNDwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjI1LDgzLDUyLDYwMTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MjEsMTY3PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yMC41NzwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NTYuNTA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPi01Ljc1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MTIvMDYvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNTAwLjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDUxNC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NzIuNDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDg5LjkwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ4MC4xNDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+OCwzNywxOTY8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQsNzU5PC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MiwwNyw2Myw2MCw4NzM8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjcsNzUsNDg3PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz45Mi42MzwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NDEuNjA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPi0xMC4xMDwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjEzLzA2LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ2Ni4yNTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0ODIuNDU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDUwLjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ1My40MDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NjQuMzM8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjU4LDAxNzwvdGQ+PHRkIHdpZHRoPSc3NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Myw3MDY8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xNCwyOSw3MywxMTM8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjE4LDczODwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MzIuMzA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMyLjQ1PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4tMTIuODU8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz4xNC8wNi8xNzwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NTAuMDU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDc3LjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ1MC4wNTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NzAuODA8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDcwLjIzPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz42Myw3Nzg8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjEsOTUxPC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTUsNzUsNDYsMDQzPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz45LDQ4NDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTQuODc8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjI2Ljk1PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yMC43NTwvdGQ+PC90cj48dHIgY2xhc3M9J1RUUm93Jz48dGQgY2xhc3M9J1RUUm93X2xlZnQxMCcgd2lkdGg9JzUwcHgnPjE1LzA2LzE3PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ2NS4wNTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NjkuOTU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDA2LjA1PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQxMS4xMDwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0MzEuMjM8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjc3LDY4MDwvdGQ+PHRkIHdpZHRoPSc3NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NSwwMzU8L3RkPjx0ZCB3aWR0aD0nMTI1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xOCw4OCw1OCwyODU8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjM1LDM0ODwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NDUuNTA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjYzLjkwPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4tNTMuOTU8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz4xNi8wNi8xNzwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0MTEuMTA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDM0LjkwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDM4OS41MDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MiwzOTcuNDU8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDA0LjQzPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz43Miw4MTA8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjQsMzc4PC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTcsNTAsNjYsMjU0PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xNiwzMjc8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIyLjQyPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40NS40MDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+LTEzLjY1PC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MTkvMDYvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDA4LjUwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ0Mi44NTwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0MDYuNTU8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDMxLjkwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQyOS40OTwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+NDgsMTI4PC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4zLDMwNTwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjExLDY5LDI2LDQ5MjwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTIsOTIzPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yNi44NTwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MzYuMzA8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIzLjQwPC90ZD48L3RyPjx0ciBjbGFzcz0nVFRSb3cnPjx0ZCBjbGFzcz0nVFRSb3dfbGVmdDEwJyB3aWR0aD0nNTBweCc+MjAvMDYvMTc8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDI5Ljk1PC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQ0NS4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MiwzODMuMTA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDQxLjUwPC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDQyMy42NjwvdGQ+PHRkIHdpZHRoPSc3MHB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MzksNDQ1PC90ZD48dGQgd2lkdGg9Jzc1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDgzNzwvdGQ+PHRkIHdpZHRoPScxMjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjksNTYsMDEsMDk4PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xMCw3ODI8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjI3LjMzPC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz42MS45MDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTEuNTU8L3RkPjwvdHI+PHRyIGNsYXNzPSdUVFJvdyc+PHRkIGNsYXNzPSdUVFJvd19sZWZ0MTAnIHdpZHRoPSc1MHB4Jz4yMS8wNi8xNzwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0NDEuMDA8L3RkPjx0ZCB3aWR0aD0nNjVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDQxLjAwPC90ZD48dGQgd2lkdGg9JzY1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4yLDM5OC4wMDwvdGQ+PHRkIHdpZHRoPSc2NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+Miw0MDYuMDU8L3RkPjx0ZCB3aWR0aD0nNzBweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjIsNDExLjg3PC90ZD48dGQgd2lkdGg9JzcwcHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40NiwxMzA8L3RkPjx0ZCB3aWR0aD0nNzVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjMsNzMxPC90ZD48dGQgd2lkdGg9JzEyNXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+MTEsMTIsNTksNDQ4PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz4xMywwOTc8L3RkPjx0ZCB3aWR0aD0nNDVweCcgY2xhc3M9J1RUUm93X3JpZ2h0MTAnPjI4LjM5PC90ZD48dGQgd2lkdGg9JzQ1cHgnIGNsYXNzPSdUVFJvd19yaWdodDEwJz40My4wMDwvdGQ+PHRkIHdpZHRoPSc0NXB4JyBjbGFzcz0nVFRSb3dfcmlnaHQxMCc+LTM0Ljk1PC90ZD48L3RyPjwvdGFibGU+PHNwYW4gaWQ9J3NwblNwcmVhZCcgY2xhc3M9J3NwblNwcmVhZCcgPiogU3ByZWFkIDxiciAvPkgtTCA6IEhpZ2gtTG93IDxiciAvPkMtTyA6IENsb3NlLU9wZW48L2JyPjwvc3Bhbj5kAgUPDxYEHwAFEU5vIFJlY29yZHMgRm91bmQuHgdWaXNpYmxlaGRkAhMPFgIfCGdkAikPFgIfAQUNZGlzcGxheTpub25lOxYCAg0PFgIfCGhkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYLBSVjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGJ0bkRvd25sb2FkBSFjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJHJhZF9ubzEFIWN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmFkX25vMgUhY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRyYWRfbm8yBSJjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJHJkYkRhaWx5BSRjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJHJkYk1vbnRobHkFJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmRiTW9udGhseQUjY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRyZGJZZWFybHkFI2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkcmRiWWVhcmx5BSNjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGJ0blN1Ym1pdAUmY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRidG5Eb3dubG9hZDE5wbb+kju7qvWJpCNeZiyy9ICJgg=='),
        (r'__VIEWSTATEGENERATOR', r'EC4662D7'),
        (r'__EVENTVALIDATION', r'/wEWYQLbuI/xBAL8np6XAwLvmaf1CAK+z8H0DgLwg7TiDwLfiJHSBALzqKOFDALHqP+oAgKch8nyDwL6iLPPBgKyg7KzAQK+gdXjCQLV943HAwLJyOyPBQL4jIbOBALQ2tKJCQKtqdp2AtPa0okJAq2p8tcBAt3dmY4JAq7B+LwEAoeU1dMNAuiRk8kBAqviwcsCAqvijcgCAqviicgCAqvitcgCAqviscgCAqvivcgCAqviucgCAqvipcgCAqvi4csCAqvi7csCArTigcgCArTijcgCArTiicgCArns69cIAs6hlY0NAs6hweUPAs6h7YIHAs6hma4MAs6hhcsFAs6hsfACAs6h3Z0KAs6hyboDAs6h9ecIAqWYx/4PAqWY85sHAqWY3/IBAqWYy58JAqWY98QGAqWY4+EPAqWYj40HAqWYu6oMAqWYp9cFAqWY0/wCAuH7uooHAuH7prcMAuH7ko4JAuH7vqsGAuH7qtAPAuH71v0EAuH7wpoMAuH77scFAuH7muMCAq+ZxugBAoyJwJ8FAvvEvkUC+8TqrQIC+8TGygoC+8Sy5gEC+8SugwgC+8SauA8C+8T21QcC+8Ti8g4C+8TerwUCkP3stgICkP3Y0woCkP30ugwCkP3g1wQCkP3cjAsCkP3IqQICkP2kxQoCkP2Q4gECkP2MnwgCkP34tA8C1J6RwgoC1J6N/wEC1J65xgQC1J6V4wsC1J6BmAIC1J79tQkC1J7p0gEC1J7FjwgC1J6xqw8C+NCVogoC1ffRxQNUgPW5MbqDRoZgMXfHgQ6RxZa+OQ=='),
        (r'myDestination', r'#'),
        (r'WINDOW_NAMER', r'1'),
        (r'ctl00$ContentPlaceHolder1$hdnCode', r'532540'),
        (r'ctl00$ContentPlaceHolder1$DDate', r''),
        (r'ctl00$ContentPlaceHolder1$hidDMY', r'D'),
        (r'ctl00$ContentPlaceHolder1$hdflag', r'0'),
        (r'ctl00$ContentPlaceHolder1$hidCurrentDate', r'5/14/2018 12:00:00 AM'),
        (r'ctl00$ContentPlaceHolder1$hidYear', r''),
        (r'ctl00$ContentPlaceHolder1$hidFromDate', r'05/17/2017'),
        (r'ctl00$ContentPlaceHolder1$hidToDate', r'05/01/2018'),
        (r'ctl00$ContentPlaceHolder1$hidOldDMY', r''),
        (r'ctl00$ContentPlaceHolder1$hiddenScripCode', r'532540'),
        (r'ctl00$ContentPlaceHolder1$hidCompanyVal', r'TCS'),
        (r'ctl00$ContentPlaceHolder1$btnDownload.x', r'4'),
        (r'ctl00$ContentPlaceHolder1$btnDownload.y', r'3'),
        (r'ctl00$ContentPlaceHolder1$search', r'rad_no1'),
        (r'ctl00$ContentPlaceHolder1$Hidden1', r''),
        (r'ctl00$ContentPlaceHolder1$GetQuote1_smartSearch', r'TATA CONSULTANCY SERVICES LTD'),
        (r'ctl00$ContentPlaceHolder1$Hidden2', r''),
        (r'ctl00$ContentPlaceHolder1$GetQuote1_smartSearch2', r'Enter Security Name / Code / ID'),
        (r'ctl00$ContentPlaceHolder1$DMY', r'rdbDaily'),
        (r'ctl00$ContentPlaceHolder1$txtFromDate', r'17/05/2017'),
        (r'ctl00$ContentPlaceHolder1$txtToDate', r'01/05/2018')
        )

    try:
        bse_hist_data_uri_formFields_list=list(bse_hist_data_uri_formFields)
        get_session_variables_query="SELECT var_name, case when var_value is null then '' else var_value end as var_value FROM public.session_variables WHERE var_site=%s and var_type='FormFields' and var_name in ('__EVENTVALIDATION','__VIEWSTATE') order by var_seq_id asc"
        logging.info('connecting to database')
        con = psycopg2.connect("dbname="+os.environ['DB_NAME']+" user="+os.environ['DB_USER']+" host="+os.environ['DB_HOST']+" port="+os.environ['DB_PORT']+" password="+os.environ['DB_PASS'])
        cur = con.cursor()
        cur.execute(get_session_variables_query,(bse_hist_data_uri,))
        form=cur.fetchall()
        ff_view_state='(r\'__VIEWSTATE\',r\''+form[0][1]+'\')'
        bse_hist_data_uri_formFields_list[2]=literal_eval(ff_view_state)
        ff_event_validation='(r\'__EVENTVALIDATION\',r\''+form[1][1]+'\')'
        bse_hist_data_uri_formFields_list[4]=literal_eval(ff_event_validation)
        bse_hist_data_uri_formFields=tuple(bse_hist_data_uri_formFields_list)
    except Exception as e:
        logging.exception("Following is the exception occured: %s", e)
        #print(e)
        sys.exit(11)

    def get_bse_stock_data(self, trxn_date, security_code, security_id, security_name, trxn_end_date=datetime.datetime.now()):
        try:
            logging.info('Inside get_bse_stock_data function called get_bse_stock_data(self, %s, %s, %s, %s)',trxn_date, security_code, security_id, security_name)
            user_stock_list=list()
            security_start_date=trxn_date.strftime("%m/%d/%Y")
            txtFromDate=trxn_date.strftime("%d/%m/%Y") #'22/04/2017'
            now = trxn_end_date
            if now.hour < 18 :
                security_end_date=(datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
                txtToDate=(datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%d/%m/%Y")
            else:
                security_end_date=now.strftime("%m/%d/%Y")
                txtToDate=now.strftime("%d/%m/%Y")
            if now.hour > 11:
                date_value=str(now.month)+'/'+str(now.day)+'/'+str(now.year)+' 12:00:00 PM'
            else:
                date_value=str(now.month)+'/'+str(now.day)+'/'+str(now.year)+' 12:00:00 AM'
            #logging.info('security_end_date : %s', security_end_date, 'txtToDate : %s', txtToDate)
            modify_formFields=list(self.bse_hist_data_uri_formFields)
            ff_hdnCode='(r\'ctl00$ContentPlaceHolder1$hdnCode\', r\''+security_code+'\')'
            modify_formFields[7]=literal_eval(ff_hdnCode)
            ff_hidCurrentDate='(r\'ctl00$ContentPlaceHolder1$hidCurrentDate\', r\''+date_value+'\')'
            modify_formFields[11]=literal_eval(ff_hidCurrentDate)
            ff_hidFromDate='(r\'ctl00$ContentPlaceHolder1$hidFromDate\', r\''+security_start_date+'\')'
            modify_formFields[13]=literal_eval(ff_hidFromDate)
            ff_hidToDate='(r\'ctl00$ContentPlaceHolder1$hidToDate\', r\''+security_end_date+'\')'
            modify_formFields[14]=literal_eval(ff_hidToDate)
            ff_hiddenScripCode='(r\'ctl00$ContentPlaceHolder1$hiddenScripCode\', r\''+security_code+'\')'
            modify_formFields[16]=literal_eval(ff_hiddenScripCode)
            ff_hidCompanyVal='(r\'ctl00$ContentPlaceHolder1$hidCompanyVal\', r\''+security_id+'\')'
            modify_formFields[17]=literal_eval(ff_hidCompanyVal)
            ff_GetQuote1_smartSearch='(r\'ctl00$ContentPlaceHolder1$GetQuote1_smartSearch\', r\''+security_name+'\')'
            modify_formFields[22]=literal_eval(ff_GetQuote1_smartSearch)
            ff_txtFromDate='(r\'ctl00$ContentPlaceHolder1$txtFromDate\', r\''+txtFromDate+'\')'
            modify_formFields[26]=literal_eval(ff_txtFromDate)
            ff_txtToDate='(r\'ctl00$ContentPlaceHolder1$txtToDate\', r\''+txtToDate+'\')'
            modify_formFields[27]=literal_eval(ff_txtToDate)
            bse_hist_data_uri_formFields=tuple(modify_formFields)
            logging.info('Reqesting data from bse for stocks')
            #logging.debug('urllib.parse.urlencode(%s).encode("utf-8")',bse_hist_data_uri_formFields)
            data = urllib.parse.urlencode(bse_hist_data_uri_formFields).encode("utf-8")
            #logging.debug('urllib.request.Request(%s,%s,%s)',self.bse_hist_data_uri,data,self.bse_hist_data_uri_headers)
            req=urllib.request.Request(self.bse_hist_data_uri,data,self.bse_hist_data_uri_headers)
            security_data=urllib.request.urlopen(req)
            logging.info('Reurning stocks data from bse')
            return security_data
        except (ValueError, urllib.error.HTTPError) as e:
            logging.exception("Following is the exception occured http: %s", str(e))
            if 'not enough values to unpack' in str(e) or 'HTTP Error 404' in str(e):
                logging.debug('Inside except of get_bse_stocks')
                uri="https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0"
                req=urllib.request.Request(uri)
                res=urllib.request.urlopen(req)
                page_data_str=res.read().decode('utf-8')
                logging.debug('updating session variables for %s', uri)
                parser = MyHTMLParser()
                MyHTMLParser.url=uri
                parser.feed(page_data_str)
                logging.debug('updating session variables for %s completed',uri)
                logging.debug('outside except of get_bse_stocks')
                self.get_bse_stock_data(trxn_date, security_code, security_id, security_name, trxn_end_date)
        except Exception as e:
            logging.exception("Following is the exception occured: %s", e)
            #print(e)
            sys.exit(11)

    def get_bse_stocks(self):
        try:
            logging.info('inside the get_bse_stocks function')

            uri="https://www.bseindia.com/corporates/List_Scrips.aspx"

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            formFields = (
                (r'__EVENTTARGET', r'ctl00$ContentPlaceHolder1$lnkDownload'),
                (r'__EVENTARGUMENT', r''),
                (r'__VIEWSTATE', r'/wEPDwUKMTY1OTcwNzY0MQ9kFgJmD2QWAgIDD2QWAgIDD2QWDAIDDw8WAh4HVmlzaWJsZWdkZAILDxAPFgYeDURhdGFUZXh0RmllbGQFCkdST1VQX0NPREUeDkRhdGFWYWx1ZUZpZWxkBQpHUk9VUF9DT0RFHgtfIURhdGFCb3VuZGdkEBUUBlNlbGVjdAJBIAJCIAJFIAJGIAJGQwJHQwJJIAJJRgJJUAJNIAJNVAJQIAJUIAJXIAJYIAJYRAJYVAJaIAJaUBUUBlNlbGVjdAJBIAJCIAJFIAJGIAJGQwJHQwJJIAJJRgJJUAJNIAJNVAJQIAJUIAJXIAJYIAJYRAJYVAJaIAJaUBQrAxRnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAg0PEA8WBh8BBQ1pbmR1c3RyeV9uYW1lHwIFDWluZHVzdHJ5X25hbWUfA2dkEBV+BlNlbGVjdAwyLzMgV2hlZWxlcnMTQWR2ZXJ0aXNpbmcgJiBNZWRpYQlBZXJvc3BhY2UNQWdyb2NoZW1pY2FscwhBaXJsaW5lcwlBbHVtaW5pdW0VQXNzZXQgTWFuYWdlbWVudCBDb3MuFkF1dG8gUGFydHMgJiBFcXVpcG1lbnQcQXV0byBUeXJlcyAmIFJ1YmJlciBQcm9kdWN0cwVCYW5rcw1CaW90ZWNobm9sb2d5B0JQTy9LUE8YQnJld2VyaWVzICYgRGlzdGlsbGVyaWVzF0Jyb2FkY2FzdGluZyAmIENhYmxlIFRWDENhcmJvbiBCbGFjaxdDYXJzICYgVXRpbGl0eSBWZWhpY2xlcxhDZW1lbnQgJiBDZW1lbnQgUHJvZHVjdHMbQ2lnYXJldHRlcyxUb2JhY2NvIFByb2R1Y3RzBENvYWwYQ29tbS5QcmludGluZy9TdGF0aW9uZXJ5HENvbW0uVHJhZGluZyAgJiBEaXN0cmlidXRpb24TQ29tbWVyY2lhbCBWZWhpY2xlcxNDb21tb2RpdHkgQ2hlbWljYWxzEUNvbXB1dGVyIEhhcmR3YXJlGkNvbnN0cnVjdGlvbiAmIEVuZ2luZWVyaW5nFkNvbnN0cnVjdGlvbiBNYXRlcmlhbHMTQ29uc3VsdGluZyBTZXJ2aWNlcxRDb25zdW1lciBFbGVjdHJvbmljcxZDb250YWluZXJzICYgUGFja2FnaW5nBkNvcHBlchhEYXRhIFByb2Nlc3NpbmcgU2VydmljZXMHRGVmZW5jZRFEZXBhcnRtZW50IFN0b3JlcwxEaXN0cmlidXRvcnMLRGl2ZXJzaWZpZWQLRWRpYmxlIE9pbHMJRWR1Y2F0aW9uEkVsZWN0cmljIFV0aWxpdGllcxVFbGVjdHJvbmljIENvbXBvbmVudHMYRXhwbG9yYXRpb24gJiBQcm9kdWN0aW9uC0ZlcnRpbGl6ZXJzEUZpYnJlcyAmIFBsYXN0aWNzGUZpbmFuY2UgKGluY2x1ZGluZyBOQkZDcykWRmluYW5jaWFsIEluc3RpdHV0aW9ucxZGb29kICYgRHJ1Z3MgUmV0YWlsaW5nCEZvb3R3ZWFyD0ZvcmVzdCBQcm9kdWN0cxtGdXJuaXR1cmUsRnVybmlzaGluZyxQYWludHMRR2VuZXJhbCBJbnN1cmFuY2UbR2lmdCBBcnRpY2xlcyxUb3lzICYgQ2FyZHMgFUhlYWx0aGNhcmUgRmFjaWxpdGllcxNIZWFsdGhjYXJlIFNlcnZpY2VzE0hlYWx0aGNhcmUgU3VwcGxpZXMaSGVhdnkgRWxlY3RyaWNhbCBFcXVpcG1lbnQRSG9sZGluZyBDb21wYW5pZXMGSG90ZWxzFEhvdXNlaG9sZCBBcHBsaWFuY2VzEkhvdXNlaG9sZCBQcm9kdWN0cwlIb3VzZXdhcmUQSG91c2luZyBGaW5hbmNlIBBJbmR1c3RyaWFsIEdhc2VzFEluZHVzdHJpYWwgTWFjaGluZXJ5FEludGVncmF0ZWQgT2lsICYgR2FzG0ludGVybmV0ICYgQ2F0YWxvZ3VlIFJldGFpbBxJbnRlcm5ldCBTb2Z0d2FyZSAmIFNlcnZpY2VzFEludmVzdG1lbnQgQ29tcGFuaWVzFUlyb24gJiBTdGVlbCBQcm9kdWN0cxxJcm9uICYgU3RlZWwvSW50ZXJtLlByb2R1Y3RzGElUIENvbnN1bHRpbmcgJiBTb2Z0d2FyZRdJVCBOZXR3b3JraW5nIEVxdWlwbWVudBRJVCBTb2Z0d2FyZSBQcm9kdWN0cxRJVCBUcmFpbmluZyBTZXJ2aWNlcxRKdXRlICYgSnV0ZSBQcm9kdWN0cw5MaWZlIEluc3VyYW5jZRZNYXJpbmUgUG9ydCAmIFNlcnZpY2VzEU1lZGljYWwgRXF1aXBtZW50Bk1pbmluZxhNaXNjLkNvbW1lcmNpYWwgU2VydmljZXMWTW92aWVzICYgRW50ZXJ0YWlubWVudBdOb24tYWxjb2hvbGljIEJldmVyYWdlcxtOb24tRHVyYWJsZSBIb3VzZWhvbGQgUHJvZC4YT2lsIEVxdWlwbWVudCAmIFNlcnZpY2VzHE9pbCBNYXJrZXRpbmcgJiBEaXN0cmlidXRpb24bT3RoZXIgQWdyaWN1bHR1cmFsIFByb2R1Y3RzHE90aGVyIEFwcGFyZWxzICYgQWNjZXNzb3JpZXMZT3RoZXIgRWxlY3QuRXF1aXAuLyBQcm9kLhhPdGhlciBGaW5hbmNpYWwgU2VydmljZXMTT3RoZXIgRm9vZCBQcm9kdWN0cxZPdGhlciBJbmR1c3RyaWFsIEdvb2RzGU90aGVyIEluZHVzdHJpYWwgUHJvZHVjdHMYT3RoZXIgTGVpc3VyZSBGYWNpbGl0aWVzFk90aGVyIExlaXN1cmUgUHJvZHVjdHMYT3RoZXIgTm9uLUZlcnJvdXMgTWV0YWxzFk90aGVyIFRlbGVjb20gU2VydmljZXMOUGFja2FnZWQgRm9vZHMWUGFwZXIgJiBQYXBlciBQcm9kdWN0cxFQZXJzb25hbCBQcm9kdWN0cw5QZXRyb2NoZW1pY2Fscw9QaGFybWFjZXV0aWNhbHMVUGhvdG9ncmFwaGljIFByb2R1Y3RzEFBsYXN0aWMgUHJvZHVjdHMKUHVibGlzaGluZxZSZWFsIEVzdGF0ZSBJbnZlc3RtZW50BlJlYWx0eRpSZWZpbmVyaWVzLyBQZXRyby1Qcm9kdWN0cwtSZXN0YXVyYW50cxBSb2FkcyAmIEhpZ2h3YXlzCFNoaXBwaW5nFFNwLkNvbnN1bWVyIFNlcnZpY2VzE1NwZWNpYWx0eSBDaGVtaWNhbHMQU3BlY2lhbHR5IFJldGFpbBtTdG9yYWdlIE1lZGlhICYgUGVyaXBoZXJhbHMFU3VnYXIWU3VyZmFjZSBUcmFuc3BvcnRhdGlvbgxUZWEgJiBDb2ZmZWUcVGVsZWNvbSAtIEFsdGVybmF0ZSBDYXJyaWVycw5UZWxlY29tIENhYmxlcxFUZWxlY29tIEVxdWlwbWVudBBUZWxlY29tIFNlcnZpY2VzCFRleHRpbGVzGlRyYW5zcG9ydCBSZWxhdGVkIFNlcnZpY2VzGlRyYW5zcG9ydGF0aW9uIC0gTG9naXN0aWNzF1RyYXZlbCBTdXBwb3J0IFNlcnZpY2VzE1V0aWxpdGllczpOb24tRWxlYy4EWmluYxV+BlNlbGVjdAwyLzMgV2hlZWxlcnMTQWR2ZXJ0aXNpbmcgJiBNZWRpYQlBZXJvc3BhY2UNQWdyb2NoZW1pY2FscwhBaXJsaW5lcwlBbHVtaW5pdW0VQXNzZXQgTWFuYWdlbWVudCBDb3MuFkF1dG8gUGFydHMgJiBFcXVpcG1lbnQcQXV0byBUeXJlcyAmIFJ1YmJlciBQcm9kdWN0cwVCYW5rcw1CaW90ZWNobm9sb2d5B0JQTy9LUE8YQnJld2VyaWVzICYgRGlzdGlsbGVyaWVzF0Jyb2FkY2FzdGluZyAmIENhYmxlIFRWDENhcmJvbiBCbGFjaxdDYXJzICYgVXRpbGl0eSBWZWhpY2xlcxhDZW1lbnQgJiBDZW1lbnQgUHJvZHVjdHMbQ2lnYXJldHRlcyxUb2JhY2NvIFByb2R1Y3RzBENvYWwYQ29tbS5QcmludGluZy9TdGF0aW9uZXJ5HENvbW0uVHJhZGluZyAgJiBEaXN0cmlidXRpb24TQ29tbWVyY2lhbCBWZWhpY2xlcxNDb21tb2RpdHkgQ2hlbWljYWxzEUNvbXB1dGVyIEhhcmR3YXJlGkNvbnN0cnVjdGlvbiAmIEVuZ2luZWVyaW5nFkNvbnN0cnVjdGlvbiBNYXRlcmlhbHMTQ29uc3VsdGluZyBTZXJ2aWNlcxRDb25zdW1lciBFbGVjdHJvbmljcxZDb250YWluZXJzICYgUGFja2FnaW5nBkNvcHBlchhEYXRhIFByb2Nlc3NpbmcgU2VydmljZXMHRGVmZW5jZRFEZXBhcnRtZW50IFN0b3JlcwxEaXN0cmlidXRvcnMLRGl2ZXJzaWZpZWQLRWRpYmxlIE9pbHMJRWR1Y2F0aW9uEkVsZWN0cmljIFV0aWxpdGllcxVFbGVjdHJvbmljIENvbXBvbmVudHMYRXhwbG9yYXRpb24gJiBQcm9kdWN0aW9uC0ZlcnRpbGl6ZXJzEUZpYnJlcyAmIFBsYXN0aWNzGUZpbmFuY2UgKGluY2x1ZGluZyBOQkZDcykWRmluYW5jaWFsIEluc3RpdHV0aW9ucxZGb29kICYgRHJ1Z3MgUmV0YWlsaW5nCEZvb3R3ZWFyD0ZvcmVzdCBQcm9kdWN0cxtGdXJuaXR1cmUsRnVybmlzaGluZyxQYWludHMRR2VuZXJhbCBJbnN1cmFuY2UbR2lmdCBBcnRpY2xlcyxUb3lzICYgQ2FyZHMgFUhlYWx0aGNhcmUgRmFjaWxpdGllcxNIZWFsdGhjYXJlIFNlcnZpY2VzE0hlYWx0aGNhcmUgU3VwcGxpZXMaSGVhdnkgRWxlY3RyaWNhbCBFcXVpcG1lbnQRSG9sZGluZyBDb21wYW5pZXMGSG90ZWxzFEhvdXNlaG9sZCBBcHBsaWFuY2VzEkhvdXNlaG9sZCBQcm9kdWN0cwlIb3VzZXdhcmUQSG91c2luZyBGaW5hbmNlIBBJbmR1c3RyaWFsIEdhc2VzFEluZHVzdHJpYWwgTWFjaGluZXJ5FEludGVncmF0ZWQgT2lsICYgR2FzG0ludGVybmV0ICYgQ2F0YWxvZ3VlIFJldGFpbBxJbnRlcm5ldCBTb2Z0d2FyZSAmIFNlcnZpY2VzFEludmVzdG1lbnQgQ29tcGFuaWVzFUlyb24gJiBTdGVlbCBQcm9kdWN0cxxJcm9uICYgU3RlZWwvSW50ZXJtLlByb2R1Y3RzGElUIENvbnN1bHRpbmcgJiBTb2Z0d2FyZRdJVCBOZXR3b3JraW5nIEVxdWlwbWVudBRJVCBTb2Z0d2FyZSBQcm9kdWN0cxRJVCBUcmFpbmluZyBTZXJ2aWNlcxRKdXRlICYgSnV0ZSBQcm9kdWN0cw5MaWZlIEluc3VyYW5jZRZNYXJpbmUgUG9ydCAmIFNlcnZpY2VzEU1lZGljYWwgRXF1aXBtZW50Bk1pbmluZxhNaXNjLkNvbW1lcmNpYWwgU2VydmljZXMWTW92aWVzICYgRW50ZXJ0YWlubWVudBdOb24tYWxjb2hvbGljIEJldmVyYWdlcxtOb24tRHVyYWJsZSBIb3VzZWhvbGQgUHJvZC4YT2lsIEVxdWlwbWVudCAmIFNlcnZpY2VzHE9pbCBNYXJrZXRpbmcgJiBEaXN0cmlidXRpb24bT3RoZXIgQWdyaWN1bHR1cmFsIFByb2R1Y3RzHE90aGVyIEFwcGFyZWxzICYgQWNjZXNzb3JpZXMZT3RoZXIgRWxlY3QuRXF1aXAuLyBQcm9kLhhPdGhlciBGaW5hbmNpYWwgU2VydmljZXMTT3RoZXIgRm9vZCBQcm9kdWN0cxZPdGhlciBJbmR1c3RyaWFsIEdvb2RzGU90aGVyIEluZHVzdHJpYWwgUHJvZHVjdHMYT3RoZXIgTGVpc3VyZSBGYWNpbGl0aWVzFk90aGVyIExlaXN1cmUgUHJvZHVjdHMYT3RoZXIgTm9uLUZlcnJvdXMgTWV0YWxzFk90aGVyIFRlbGVjb20gU2VydmljZXMOUGFja2FnZWQgRm9vZHMWUGFwZXIgJiBQYXBlciBQcm9kdWN0cxFQZXJzb25hbCBQcm9kdWN0cw5QZXRyb2NoZW1pY2Fscw9QaGFybWFjZXV0aWNhbHMVUGhvdG9ncmFwaGljIFByb2R1Y3RzEFBsYXN0aWMgUHJvZHVjdHMKUHVibGlzaGluZxZSZWFsIEVzdGF0ZSBJbnZlc3RtZW50BlJlYWx0eRpSZWZpbmVyaWVzLyBQZXRyby1Qcm9kdWN0cwtSZXN0YXVyYW50cxBSb2FkcyAmIEhpZ2h3YXlzCFNoaXBwaW5nFFNwLkNvbnN1bWVyIFNlcnZpY2VzE1NwZWNpYWx0eSBDaGVtaWNhbHMQU3BlY2lhbHR5IFJldGFpbBtTdG9yYWdlIE1lZGlhICYgUGVyaXBoZXJhbHMFU3VnYXIWU3VyZmFjZSBUcmFuc3BvcnRhdGlvbgxUZWEgJiBDb2ZmZWUcVGVsZWNvbSAtIEFsdGVybmF0ZSBDYXJyaWVycw5UZWxlY29tIENhYmxlcxFUZWxlY29tIEVxdWlwbWVudBBUZWxlY29tIFNlcnZpY2VzCFRleHRpbGVzGlRyYW5zcG9ydCBSZWxhdGVkIFNlcnZpY2VzGlRyYW5zcG9ydGF0aW9uIC0gTG9naXN0aWNzF1RyYXZlbCBTdXBwb3J0IFNlcnZpY2VzE1V0aWxpdGllczpOb24tRWxlYy4EWmluYxQrA35nZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIRDxYCHwBnZAITDzwrAA0BAA8WBB8DZx4LXyFJdGVtQ291bnQC+z9kFgJmD2QWNAICD2QWEmYPZBYCZg8PFgQeBFRleHQFBjUwMDAwMh4LTmF2aWdhdGVVcmwFSGh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hYmItaW5kaWEtbGltaXRlZC9hYmIvNTAwMDAyL2RkAgEPDxYCHwUFA0FCQmRkAgIPDxYCHwUFEUFCQiBJbmRpYSBMaW1pdGVkZGQCAw8PFgIfBQUGQWN0aXZlZGQCBA8PFgIfBQUCQSBkZAIFDw8WAh8FBQQyLjAwZGQCBg8PFgIfBQUMSU5FMTE3QTAxMDIyZGQCBw8PFgIfBQUaSGVhdnkgRWxlY3RyaWNhbCBFcXVpcG1lbnRkZAIIDw8WAh8FBQZFcXVpdHlkZAIDD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDAzHwYFT2h0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hZWdpcy1sb2dpc3RpY3MtbHRkL2FlZ2lzbG9nLzUwMDAwMy9kZAIBDw8WAh8FBQhBRUdJU0xPR2RkAgIPDxYCHwUFFEFFR0lTIExPR0lTVElDUyBMVEQuZGQCAw8PFgIfBQUGQWN0aXZlZGQCBA8PFgIfBQUCQSBkZAIFDw8WAh8FBQQxLjAwZGQCBg8PFgIfBQUMSU5FMjA4QzAxMDI1ZGQCBw8PFgIfBQUgT2lsIE1hcmtldGluZyAmYW1wOyBEaXN0cmlidXRpb25kZAIIDw8WAh8FBQZFcXVpdHlkZAIED2QWEmYPZBYCZg8PFgQfBQUGNTAwMDA0HwYFTmh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS90b3JyZW50LXBvd2VyLWFlYy1sdGQvdHBhZWMvNTAwMDA0L2RkAgEPDxYCHwUFBVRQQUVDZGQCAg8PFgIfBQUWVE9SUkVOVCBQT1dFUiBBRUMgTFRELmRkAgMPDxYCHwUFCERlbGlzdGVkZGQCBA8PFgIfBQUCQiBkZAIFDw8WAh8FBQUxMC4wMGRkAgYPDxYCHwUFDElORTQyNEEwMTAxNGRkAgcPDxYCHwUFBiZuYnNwO2RkAggPDxYCHwUFBkVxdWl0eWRkAgUPZBYSZg9kFgJmDw8WBB8FBQY1MDAwMDUfBgVQaHR0cHM6Ly93d3cuYnNlaW5kaWEuY29tL3N0b2NrLXNoYXJlLXByaWNlL2FrYXItbGFtaW5hdG9ycy1sdGQvYWthcmxhbWluLzUwMDAwNS9kZAIBDw8WAh8FBQlBS0FSTEFNSU5kZAICDw8WAh8FBRRBS0FSIExBTUlOQVRPUlMgTFRELmRkAgMPDxYCHwUFCERlbGlzdGVkZGQCBA8PFgIfBQUCWERkZAIFDw8WAh8FBQUxMC4wMGRkAgYPDxYCHwUFDElORTk4NEMwMTAxM2RkAgcPDxYCHwUFGUlyb24gJmFtcDsgU3RlZWwgUHJvZHVjdHNkZAIIDw8WAh8FBQZFcXVpdHlkZAIGD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDA2HwYFT2h0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hbHBoYS1kcnVnLWluZGlhLWx0ZC9hbHBoYWRyLzUwMDAwNi9kZAIBDw8WAh8FBQdBTFBIQURSZGQCAg8PFgIfBQUVQUxQSEEgRFJVRyBJTkRJQSBMVEQuZGQCAw8PFgIfBQUIRGVsaXN0ZWRkZAIEDw8WAh8FBQJCIGRkAgUPDxYCHwUFBTEwLjAwZGQCBg8PFgIfBQUMSU5FMjU2QjAxMDI2ZGQCBw8PFgIfBQUGJm5ic3A7ZGQCCA8PFgIfBQUGRXF1aXR5ZGQCBw9kFhJmD2QWAmYPDxYEHwUFBjUwMDAwOB8GBVZodHRwczovL3d3dy5ic2VpbmRpYS5jb20vc3RvY2stc2hhcmUtcHJpY2UvYW1hcmEtcmFqYS1iYXR0ZXJpZXMtbHRkL2FtYXJhamFiYXQvNTAwMDA4L2RkAgEPDxYCHwUFCkFNQVJBSkFCQVRkZAICDw8WAh8FBRlBTUFSQSBSQUpBIEJBVFRFUklFUyBMVEQuZGQCAw8PFgIfBQUGQWN0aXZlZGQCBA8PFgIfBQUCQSBkZAIFDw8WAh8FBQQxLjAwZGQCBg8PFgIfBQUMSU5FODg1QTAxMDMyZGQCBw8PFgIfBQUaQXV0byBQYXJ0cyAmYW1wOyBFcXVpcG1lbnRkZAIIDw8WAh8FBQZFcXVpdHlkZAIID2QWEmYPZBYCZg8PFgQfBQUGNTAwMDA5HwYFXWh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hbWJhbGFsLXNhcmFiaGFpLWVudGVycHJpc2VzLWx0ZC9hbWJhbGFsc2EvNTAwMDA5L2RkAgEPDxYCHwUFCUFNQkFMQUxTQWRkAgIPDxYCHwUFIUFNQkFMQUwgU0FSQUJIQUkgRU5URVJQUklTRVMgTFRELmRkAgMPDxYCHwUFBkFjdGl2ZWRkAgQPDxYCHwUFAlggZGQCBQ8PFgIfBQUFMTAuMDBkZAIGDw8WAh8FBQxJTkU0MzJBMDEwMTdkZAIHDw8WAh8FBQ9QaGFybWFjZXV0aWNhbHNkZAIIDw8WAh8FBQZFcXVpdHlkZAIJD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDEwHwYFW2h0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9ob3VzaW5nLWRldmVsb3BtZW50LWZpbmFuY2UtY29ycGx0ZC9oZGZjLzUwMDAxMC9kZAIBDw8WAh8FBQRIREZDZGQCAg8PFgIfBQUlSE9VU0lORyBERVZFTE9QTUVOVCBGSU5BTkNFIENPUlAuTFRELmRkAgMPDxYCHwUFBkFjdGl2ZWRkAgQPDxYCHwUFAkEgZGQCBQ8PFgIfBQUEMi4wMGRkAgYPDxYCHwUFDElORTAwMUEwMTAzNmRkAgcPDxYCHwUFEEhvdXNpbmcgRmluYW5jZSBkZAIIDw8WAh8FBQZFcXVpdHlkZAIKD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDExHwYFU2h0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hbXJ1dC1pbmR1c3RyaWVzLWx0ZC9hbXJ0bWlsLWJkbS81MDAwMTEvZGQCAQ8PFgIfBQULQU1SVE1JTC1CRE1kZAICDw8WAh8FBRVBTVJVVCBJTkRVU1RSSUVTIExURC5kZAIDDw8WAh8FBQhEZWxpc3RlZGRkAgQPDxYCHwUFAlogZGQCBQ8PFgIfBQUFMTAuMDBkZAIGDw8WAh8FBQxOQSAgICAgICAgICBkZAIHDw8WAh8FBQYmbmJzcDtkZAIIDw8WAh8FBQZFcXVpdHlkZAILD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDEyHwYFVmh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hbmRocmEtcGV0cm9jaGVtaWNhbHMtbHRkL2FuZGhyYXBldC81MDAwMTIvZGQCAQ8PFgIfBQUJQU5ESFJBUEVUZGQCAg8PFgIfBQUaQU5ESFJBIFBFVFJPQ0hFTUlDQUxTIExURC5kZAIDDw8WAh8FBQZBY3RpdmVkZAIEDw8WAh8FBQJYIGRkAgUPDxYCHwUFBTEwLjAwZGQCBg8PFgIfBQUMSU5FNzE0QjAxMDE2ZGQCBw8PFgIfBQUTQ29tbW9kaXR5IENoZW1pY2Fsc2RkAggPDxYCHwUFBkVxdWl0eWRkAgwPZBYSZg9kFgJmDw8WBB8FBQY1MDAwMTMfBgVgaHR0cHM6Ly93d3cuYnNlaW5kaWEuY29tL3N0b2NrLXNoYXJlLXByaWNlL2Fuc2FsLXByb3BlcnRpZXMtLWluZnJhc3RydWN0dXJlLWx0ZC9hbnNhbGFwaS81MDAwMTMvZGQCAQ8PFgIfBQUIQU5TQUxBUElkZAICDw8WAh8FBSpBTlNBTCBQUk9QRVJUSUVTICZhbXA7IElORlJBU1RSVUNUVVJFIExURC5kZAIDDw8WAh8FBQZBY3RpdmVkZAIEDw8WAh8FBQJCIGRkAgUPDxYCHwUFBDUuMDBkZAIGDw8WAh8FBQxJTkU0MzZBMDEwMjZkZAIHDw8WAh8FBQZSZWFsdHlkZAIIDw8WAh8FBQZFcXVpdHlkZAIND2QWEmYPZBYCZg8PFgQfBQUGNTAwMDE0HwYFTWh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hcHBsZS1maW5hbmNlLWx0ZC9hcHBsZWZpbi81MDAwMTQvZGQCAQ8PFgIfBQUIQVBQTEVGSU5kZAICDw8WAh8FBRJBUFBMRSBGSU5BTkNFIExURC5kZAIDDw8WAh8FBQZBY3RpdmVkZAIEDw8WAh8FBQJYVGRkAgUPDxYCHwUFBTEwLjAwZGQCBg8PFgIfBQUMSU5FMDk2QTAxMDEwZGQCBw8PFgIfBQUZRmluYW5jZSAoaW5jbHVkaW5nIE5CRkNzKWRkAggPDxYCHwUFBkVxdWl0eWRkAg4PZBYSZg9kFgJmDw8WBB8FBQY1MDAwMTUfBgVEaHR0cHM6Ly93d3cuYnNlaW5kaWEuY29tL3N0b2NrLXNoYXJlLXByaWNlL2ljaWNpLWx0ZC9pY2ljaWRtLzUwMDAxNS9kZAIBDw8WAh8FBQdJQ0lDSURNZGQCAg8PFgIfBQUKSUNJQ0kgTFRELmRkAgMPDxYCHwUFCERlbGlzdGVkZGQCBA8PFgIfBQUCQiBkZAIFDw8WAh8FBQUxMC4wMGRkAgYPDxYCHwUFDElORTAwNUEwMTAxMWRkAgcPDxYCHwUFBiZuYnNwO2RkAggPDxYCHwUFBkVxdWl0eWRkAg8PZBYSZg9kFgJmDw8WBB8FBQY1MDAwMTYfBgVNaHR0cHM6Ly93d3cuYnNlaW5kaWEuY29tL3N0b2NrLXNoYXJlLXByaWNlL2FydW5hLWhvdGVscy1sdGQvYXJ1bmFodGVsLzUwMDAxNi9kZAIBDw8WAh8FBQlBUlVOQUhURUxkZAICDw8WAh8FBRFBUlVOQSBIT1RFTFMgTFRELmRkAgMPDxYCHwUFBkFjdGl2ZWRkAgQPDxYCHwUFAlhUZGQCBQ8PFgIfBQUFMTAuMDBkZAIGDw8WAh8FBQxJTkU5NTdDMDEwMTlkZAIHDw8WAh8FBQZIb3RlbHNkZAIIDw8WAh8FBQZFcXVpdHlkZAIQD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDE4HwYFPGh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS8tL2FycG9sZG0vNTAwMDE4L2RkAgEPDxYCHwUFB0FSUE9MRE1kZAICDw8WAh8FBQdBUlBPTERNZGQCAw8PFgIfBQUIRGVsaXN0ZWRkZAIEDw8WAh8FBQJCIGRkAgUPDxYCHwUFBTEwLjAwZGQCBg8PFgIfBQUMSU5FMDM1QTAxMDE4ZGQCBw8PFgIfBQUGJm5ic3A7ZGQCCA8PFgIfBQUGRXF1aXR5ZGQCEQ9kFhJmD2QWAmYPDxYEHwUFBjUwMDAxOR8GBUxodHRwczovL3d3dy5ic2VpbmRpYS5jb20vc3RvY2stc2hhcmUtcHJpY2UvYmFuay1vZi1yYWphc3RoYW4tbHRkL2Jvci81MDAwMTkvZGQCAQ8PFgIfBQUDQk9SZGQCAg8PFgIfBQUWQkFOSyBPRiBSQUpBU1RIQU4gTFRELmRkAgMPDxYCHwUFCERlbGlzdGVkZGQCBA8PFgIfBQUCQiBkZAIFDw8WAh8FBQUxMC4wMGRkAgYPDxYCHwUFDElORTMyMEEwMTAxNGRkAgcPDxYCHwUFBUJhbmtzZGQCCA8PFgIfBQUGRXF1aXR5ZGQCEg9kFhJmD2QWAmYPDxYEHwUFBjUwMDAyMB8GBVRodHRwczovL3d3dy5ic2VpbmRpYS5jb20vc3RvY2stc2hhcmUtcHJpY2UvYm9tYmF5LWR5ZWluZy0tbWZnY29sdGQvYm9tZHllaW5nLzUwMDAyMC9kZAIBDw8WAh8FBQlCT01EWUVJTkdkZAICDw8WAh8FBR9CT01CQVkgRFlFSU5HICZhbXA7IE1GRy5DTy5MVEQuZGQCAw8PFgIfBQUGQWN0aXZlZGQCBA8PFgIfBQUCVCBkZAIFDw8WAh8FBQQyLjAwZGQCBg8PFgIfBQUMSU5FMDMyQTAxMDIzZGQCBw8PFgIfBQUIVGV4dGlsZXNkZAIIDw8WAh8FBQZFcXVpdHlkZAITD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDIxHwYFPGh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS8tL2FzaW5jb2YvNTAwMDIxL2RkAgEPDxYCHwUFB0FTSU5DT0ZkZAICDw8WAh8FBQdBU0lOQ09GZGQCAw8PFgIfBQUIRGVsaXN0ZWRkZAIEDw8WAh8FBQJaIGRkAgUPDxYCHwUFBTEwLjAwZGQCBg8PFgIfBQUMTkEgICAgICAgICAgZGQCBw8PFgIfBQUGJm5ic3A7ZGQCCA8PFgIfBQUGRXF1aXR5ZGQCFA9kFhJmD2QWAmYPDxYEHwUFBjUwMDAyMx8GBVpodHRwczovL3d3dy5ic2VpbmRpYS5jb20vc3RvY2stc2hhcmUtcHJpY2UvYXNpYW4taG90ZWxzLShub3J0aCktbGltaXRlZC9hc2lhbmhvdG5yLzUwMDAyMy9kZAIBDw8WAh8FBQpBU0lBTkhPVE5SZGQCAg8PFgIfBQUcQXNpYW4gSG90ZWxzIChOb3J0aCkgTGltaXRlZGRkAgMPDxYCHwUFBkFjdGl2ZWRkAgQPDxYCHwUFAkIgZGQCBQ8PFgIfBQUFMTAuMDBkZAIGDw8WAh8FBQxJTkUzNjNBMDEwMjJkZAIHDw8WAh8FBQZIb3RlbHNkZAIIDw8WAh8FBQZFcXVpdHlkZAIVD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDI0HwYFWGh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hc3NhbS1jb21wYW55LShpbmRpYSktbGltaXRlZC9hc3NhbWNvLzUwMDAyNC9kZAIBDw8WAh8FBQdBU1NBTUNPZGQCAg8PFgIfBQUdQXNzYW0gQ29tcGFueSAoSW5kaWEpIExpbWl0ZWRkZAIDDw8WAh8FBQZBY3RpdmVkZAIEDw8WAh8FBQJUIGRkAgUPDxYCHwUFBDEuMDBkZAIGDw8WAh8FBQxJTkU0NDJBMDEwMjRkZAIHDw8WAh8FBRBUZWEgJmFtcDsgQ29mZmVlZGQCCA8PFgIfBQUGRXF1aXR5ZGQCFg9kFhJmD2QWAmYPDxYEHwUFBjUwMDAyNR8GBUlodHRwczovL3d3dy5ic2VpbmRpYS5jb20vc3RvY2stc2hhcmUtcHJpY2UvYXNzYW1icm9vay1sdGQvYXNzYW1ici81MDAwMjUvZGQCAQ8PFgIfBQUHQVNTQU1CUmRkAgIPDxYCHwUFEUFTU0FNQlJPT0sgTFRELi0kZGQCAw8PFgIfBQUIRGVsaXN0ZWRkZAIEDw8WAh8FBQJYIGRkAgUPDxYCHwUFBTEwLjAwZGQCBg8PFgIfBQUMSU5FMzUzQzAxMDExZGQCBw8PFgIfBQUQVGVhICZhbXA7IENvZmZlZWRkAggPDxYCHwUFBkVxdWl0eWRkAhcPZBYSZg9kFgJmDw8WBB8FBQY1MDAwMjYfBgVPaHR0cHM6Ly93d3cuYnNlaW5kaWEuY29tL3N0b2NrLXNoYXJlLXByaWNlL2F0YXNoLWluZHVzdHJpZXMtbHRkL2F0c2hpbmQvNTAwMDI2L2RkAgEPDxYCHwUFB0FUU0hJTkRkZAICDw8WAh8FBRVBVEFTSCBJTkRVU1RSSUVTIExURC5kZAIDDw8WAh8FBQhEZWxpc3RlZGRkAgQPDxYCHwUFAlogZGQCBQ8PFgIfBQUFMTAuMDBkZAIGDw8WAh8FBQxOQSAgICAgICAgICBkZAIHDw8WAh8FBQYmbmJzcDtkZAIIDw8WAh8FBQZFcXVpdHlkZAIYD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDI3HwYFQGh0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hdHVsLWx0ZC9hdHVsLzUwMDAyNy9kZAIBDw8WAh8FBQRBVFVMZGQCAg8PFgIfBQUJQVRVTCBMVEQuZGQCAw8PFgIfBQUGQWN0aXZlZGQCBA8PFgIfBQUCQSBkZAIFDw8WAh8FBQUxMC4wMGRkAgYPDxYCHwUFDElORTEwMEEwMTAxMGRkAgcPDxYCHwUFDUFncm9jaGVtaWNhbHNkZAIIDw8WAh8FBQZFcXVpdHlkZAIZD2QWEmYPZBYCZg8PFgQfBQUGNTAwMDI4HwYFT2h0dHBzOi8vd3d3LmJzZWluZGlhLmNvbS9zdG9jay1zaGFyZS1wcmljZS9hdHYtcHJvamVjdHMtaW5kaWEtbHRkL2F0dnByLzUwMDAyOC9kZAIBDw8WAh8FBQVBVFZQUmRkAgIPDxYCHwUFF0FUViBQUk9KRUNUUyBJTkRJQSBMVEQuZGQCAw8PFgIfBQUGQWN0aXZlZGQCBA8PFgIfBQUCWFRkZAIFDw8WAh8FBQUxMC4wMGRkAgYPDxYCHwUFDElORTQ0N0EwMTAxNWRkAgcPDxYCHwUFHkNvbnN0cnVjdGlvbiAmYW1wOyBFbmdpbmVlcmluZ2RkAggPDxYCHwUFBkVxdWl0eWRkAhoPZBYSZg9kFgJmDw8WBB8FBQY1MDAwMjkfBgVSaHR0cHM6Ly93d3cuYnNlaW5kaWEuY29tL3N0b2NrLXNoYXJlLXByaWNlL2F1dG9saXRlLShpbmRpYSktbHRkL2F1dG9saXRpbmQvNTAwMDI5L2RkAgEPDxYCHwUFCkFVVE9MSVRJTkRkZAICDw8WAh8FBRVBVVRPTElURSAoSU5ESUEpIExURC5kZAIDDw8WAh8FBQZBY3RpdmVkZAIEDw8WAh8FBQJCIGRkAgUPDxYCHwUFBTEwLjAwZGQCBg8PFgIfBQUMSU5FNDQ4QTAxMDEzZGQCBw8PFgIfBQUaQXV0byBQYXJ0cyAmYW1wOyBFcXVpcG1lbnRkZAIIDw8WAh8FBQZFcXVpdHlkZAIbDw8WAh8AaGRkAhUPDxYCHwVlZGQYAgUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFI2N0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkYnRuU3VibWl0BSBjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJGd2RGF0YQ88KwAKAQgCyAJkHQPEX00ODAP7wXqF3Ee94XQYlyI='),
                (r'__VIEWSTATEGENERATOR', r'CF507786'),
                (r'__EVENTVALIDATION', r'/wEWtwECmv2argYC/J6elwMC5eOC0AICvuzHng4C2MiawQwC/c+kowMCwozr0wYCguj9yA0CxZa2wg8C2fPMrAICz5CzgA4C7vvawAIC0L+KiQsC64z9gQkC+/CRlAoChNPKtAcChdPKtAcCgNPKtAcCgdPKtAcCgdP+qQcCgtP+qQcCvNPKtAcCvNPyqQcCvNOKqQcCuNPKtAcCuNO6qQcCq9PKtAcCt9PKtAcCstPKtAcCo9PKtAcCo9P6qQcCo9O6qQcCrdPKtAcCrdOKqQcCwtWLxAYC86qnhgkCz6iQBgLJ/K+YAQLe5v3wCwKZnauOCwL2v+XKCAKQwrb9CAKb1K9YAtS6iOcPAreDz4AKAp3hwOkPAofZt5QOArXz4zMCjpLv+w4Cl/DsowEC+tDwHAKBq6niCgLp1rCjDgLgx90uAuyQh+EMAuPl+LMFAumO8OUFAq/H2csOAuTIuC8Cy8XB+wMCiI7uqAcCuZL10AMCpe6p6gQC9P3VowcC8MPVwgkCl7SxwgUC86bz6wcCh+mM4wICws7tlQQCzoSDiwsCkNPC9gcC75/d2AcC/OrjrgMCgfyOoQsChI6V6AMCv96B5wcClZrK0gECiJmtrAICqN6CtwgChLru9Q0CmZGfTwK/q/T8CwLy7+/VAwL+/tvYBAL938DSDgKa/c/BDwLGv934DwLGm9GzDwLe6tq+AQKs87CCCgKKmIWsBwLFyrOxCQKk84r9DALXkf++BgLuiJPUCgLw9ve4BQKrx4ZYAtbMj9AFArSknokEArL3m+YMAuqjv+IDApD1geEEAoi5tMYOAqypkJgNAq2b2OcNAr+NqeADAsfE5qsJApj+rscHAqyzlM4PAtu814UDAv/7ybUOAvmEi8EJAtug4RcC4MPX3AcCnI+KqAkCgLWRvAsCn/vbtAQC2u7VqgYC2YTV4gsC0PHs5AUC7O/fvwcCwfLMzAECreiY0goCoanivQ4ClrbhvgUC4+3WhA4CmqTlngwC3IrJ8gcCgbysigwCl+KutgkC76unuAoCxqej+w0Cg+uNxwYC4eOmxg8CvsPC1AkCzOKfHgKZ8cKjAgKvo5LlBgL/xfzlBQKzt/GMCgKg28mJBAK+/OrKCAKOy4jsAgK+1LvHDALZw8mZDQKexp/DBgKHh5bTAgK6yIO4AwKYjo78DALii73uBgLgyaPHBALHzOy1AQLGktX/BQLkwryIBgLSj9eiDgKux/WfCALZg5j4DwLBos3gAgLM0+WgCwKou6DgDAL40JWiCgKN+tDQCAKN+qzQCAKN+rjQCAKN+rTQCAKN+qDQCAKN+rzQCAKN+ojQCAKN+oTQCALj8ODgCQKI2cKdDAKR47WVDgKN+tDQCAKN+qzQCAKN+rjQCAKN+rTQCAKN+qDQCAKN+rzQCAKN+ojQCAKN+oTQCALj8ODgCQKI2cKdDAKR47WVDmdLdmY2YbZccQV4juEWuCDNHek/'),
                (r'myDestination', r'#'),
                (r'WINDOW_NAMER', r'1'),
                (r'ctl00$ContentPlaceHolder1$hdnCode', ''),
                (r'ctl00$ContentPlaceHolder1$ddSegment', 'Segment'),
                (r'ctl00$ContentPlaceHolder1$ddlStatus', 'Select'),
                (r'ctl00$ContentPlaceHolder1$getTExtData', ''),
                (r'ctl00$ContentPlaceHolder1$ddlGroup', 'Select'),
                (r'ctl00$ContentPlaceHolder1$ddlIndustry', 'Select')
                )
            formFields_list=list(formFields)
            get_session_variables_query="SELECT var_name, case when var_value is null then '' else var_value end as var_value FROM public.session_variables WHERE var_site=%s and var_type='FormFields' and var_name in ('__EVENTVALIDATION','__VIEWSTATE') order by var_seq_id asc"
            logging.info('connecting to database')
            con = psycopg2.connect("dbname="+os.environ['DB_NAME']+" user="+os.environ['DB_USER']+" host="+os.environ['DB_HOST']+" port="+os.environ['DB_PORT']+" password="+os.environ['DB_PASS'])
            cur = con.cursor()
            cur.execute(get_session_variables_query,(uri,))
            form=cur.fetchall()
            ff_view_state='(r\'__VIEWSTATE\',r\''+form[0][1]+'\')'
            formFields_list[2]=literal_eval(ff_view_state)
            ff_event_validation='(r\'__EVENTVALIDATION\',r\''+form[1][1]+'\')'
            formFields_list[4]=literal_eval(ff_view_state)
            formFields_list=tuple(formFields_list)
            logging.info('connecting to database')
            con = psycopg2.connect("dbname="+os.environ['DB_NAME']+" user="+os.environ['DB_USER']+" host="+os.environ['DB_HOST']+" port="+os.environ['DB_PORT']+" password="+os.environ['DB_PASS'])
            cur = con.cursor()
            logging.info('successfully connected to database')
            new_stock_insert_query='INSERT INTO stock_list_bse("security_code", "security_id", "security_name", "status", "security_group", "face_value", "isin_no", "industry", "instrument") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
            existring_stock_update_query='''UPDATE stock_list_bse SET "security_name" = %s, "status" = %s, "security_group" = %s, "face_value" = %s, "isin_no" = %s, "industry"  = %s, "instrument" = %s
            WHERE "security_id"= %s'''
            market_segments=open(os.path.join("data","segment.txt"),"r")
            #market_segments=open("F:\\VIDEOS\\python1\\New folder\\segment.txt","r")
            set_existing_stocks=set()
            for segment in market_segments:
                logging.info('Getting stock list for %s segment from bse site %s',segment,uri)
                segment=segment.replace('\n','')
                modify_formFields=list(formFields)
                form_segment='(r\'ctl00$ContentPlaceHolder1$ddSegment\', r\''+segment+'\')'
                modify_formFields[8]=literal_eval(form_segment)
                formFields=tuple(modify_formFields)
                data = urllib.parse.urlencode(formFields).encode("utf-8")
                req=urllib.request.Request(uri,data,headers)
                res=urllib.request.urlopen(req)
                #cur.execute('SELECT "Security_Code" FROM stocks.stock_list_bse;')
                cur.execute('SELECT "security_code" FROM public.stock_list_bse;')
                present_stock_list=cur.fetchall()
                for stocks in present_stock_list:
                    #print(stocks[0])
                    set_existing_stocks.add(int(stocks[0]))
                for line in res:
                    stock_data1=line.decode('utf-8').replace('\n','')
                    stock_data=stock_data1.replace('\r','')
                    if 'Security Code,Security Id,Security Name,Status,Group,Face Value,ISIN No,Industry,Instrument' not in stock_data:
                        Security_Code,Security_Id,Security_Name,Status,Group,Face_Value,ISIN_No,Industry,Instrument=stock_data.split(',')
                        Security_Code_int=int(Security_Code)
                        if Face_Value=="":
                            Face_Value_float=Face_Value
                        else:
                            Face_Value_float=float(Face_Value)
                        if Security_Code_int not in set_existing_stocks:
                            new_stock_data =(Security_Code_int,Security_Id,Security_Name,Status,Group or None,Face_Value_float or None,ISIN_No or None,Industry or None,Instrument)
                            cur.execute(new_stock_insert_query, new_stock_data)
                            set_existing_stocks.add(Security_Code_int)
                            #logging.info('%s %s',new_stock_insert_query,new_stock_data)
                        else:
                            existing_stock_update_data=(Security_Name,Status,Group or None,Face_Value_float or None,ISIN_No or None,Industry or None,Instrument,Security_Id)
                            cur.execute(existring_stock_update_query, existing_stock_update_data)
                            #logging.info('%s %s',existring_stock_update_query,existing_stock_update_data)
            con.commit()
            cur.close()
            con.close()
            logging.info('Cosed connection to database')
        except (ValueError, urllib.error.HTTPError) as e:
            logging.exception("Following is the exception occured http: %s", e)
            if 'not enough values to unpack' in str(e) or 'HTTP Error 404' in str(e):
                logging.debug('Inside except of get_bse_stocks')
                uri="https://www.bseindia.com/corporates/List_Scrips.aspx"
                req=urllib.request.Request(uri)
                res=urllib.request.urlopen(req)
                page_data_str=res.read().decode('utf-8')
                logging.debug('updating session variables for %s',uri)
                parser = MyHTMLParser()
                MyHTMLParser.url=uri
                parser.feed(page_data_str)
                logging.debug('updating session variables for %s completed',uri)
            sys.exit(11)
        except Exception as e:
            logging.exception("Following is the exception occured: %s", e)
            #print(e)
            sys.exit(11)


class user_profile_ops:
    def sortFirst(self, val):
        try:
            self.val=val
            return datetime.datetime.strptime(val[0],'%d-%B-%Y')
        except Exception as e:
            logging.exception("Following is the exception occured: %s", e)
            #print(e)
            sys.exit(11)

    def user_profile_value_daily(self, user_id):
        try:
            #self.user=user
            logging.debug('Inside user_profile_value_daily called by user_profile_value_daily(self, %s)', user_id)
            logging.info('Connecting to database')
            con = psycopg2.connect("dbname="+os.environ['DB_NAME']+" user="+os.environ['DB_USER']+" host="+os.environ['DB_HOST']+" port="+os.environ['DB_PORT']+" password="+os.environ['DB_PASS'])
            cur = con.cursor()
            logging.info('Successfully connected to database')
            sum_of_security_count=0
            sum_of_todays_security=0
            user_stock_trxn_query='''WITH BUY_DATA AS (SELECT user_id,security_code,trxn_type,sum(security_count) as B_security_count
                                      FROM  public.user_stocks_trxn
                                      WHERE trxn_type='Buy' AND trxn_flag=1 AND user_id = %s
                                      GROUP BY user_id,security_code,trxn_type),
            SELL_DATA AS (SELECT user_id,security_code,trxn_type,sum(security_count) as S_security_count
                                      FROM  public.user_stocks_trxn
                                      WHERE trxn_type='Sell' AND trxn_flag=1 AND user_id = %s
                                      GROUP BY user_id,security_code,trxn_type)
                                    SELECT B.user_id,B.security_code,B.B_security_count-COALESCE(S.S_security_count, 0) as final_security_count,slb."security_id",
                                            trim( TRAILING '.' from slb."security_name") as security_name
                                    FROM BUY_DATA B
                                    JOIN public.stock_list_bse slb on slb."security_code"=b.security_code
                                    LEFT JOIN SELL_DATA S ON B.user_id=S.user_id AND B.security_code=S.security_code
                                    WHERE B.B_security_count-COALESCE(S.S_security_count, 0) >0
                                    ORDER BY user_id,security_code'''
            cur.execute(user_stock_trxn_query, (user_id, user_id))
            user_trxns=cur.fetchall()
            logging.debug('Fetching the transactions to process \nFor all user issued SQL to databse %s \nReturned data %s',user_stock_trxn_query,user_trxns)
            is_trxn_exist=0
            for security in user_trxns:
                security_code,security_count,security_id,security_name=security[1],security[2],security[3],security[4]
                security_code=str(security_code)
                trxn_date=datetime.datetime.now() #(datetime.datetime.today() - datetime.timedelta(days=2))
                secobj=bse_ops()
                logging.debug('calling get_bse_stock_data to retrieve bse stocks data get_bse_stock_data(%s, %s, %s, %s)',trxn_date, security_code, security_id, security_name)
                secdata=secobj.get_bse_stock_data(trxn_date, security_code, security_id, security_name)
                security_data=list()
                for line in secdata:
                    #print(line)
                    Date,Open_Price,High_Price,Low_Price,Close_Price,WAP,No_of_Shares,No_of_Trades,Total_Turnover,Deliverable_Quantity,Perc_Deli_Qty_to_Traded_Qty,Spread_HighVSLow,Spread_CloseVSOpen=line.decode('utf-8').replace('\n','').replace('\r','').split(',')
                    if Date=='Date':
                        continue
                    security_data.append((Date,Close_Price))
                security_data.sort(key=self.sortFirst)
                logging.debug('Security data returned after removing headers\n%s',security_data)
                for line in security_data:
                    #print(line)
                    Date,Close_Price=line[0],line[1]
                    sum_of_security_count=sum_of_security_count+security_count
                    sum_of_todays_security=sum_of_todays_security+(security_count*float(Close_Price))
                    #print(sum_of_security_count, sum_of_todays_security)
                    #print(Date,Close_Price,security_count,security_count*float(Close_Price))
                    is_trxn_exist=is_trxn_exist+1
            logging.debug('sum_of_security_count %s\nsum_of_todays_security %s',sum_of_security_count, sum_of_todays_security)
            nav_initial_query='''SELECT count(nav) FROM public.user_stock_profile_daily WHERE stock_date=(SELECT MIN(trxn_date) FROM public.user_stocks_trxn where user_id=%s)'''
            cur.execute(nav_initial_query,(user_id,))
            nav_initilization_flag=cur.fetchone()
            logging.debug('nav_initilization_flag %s',nav_initilization_flag[0])
            if  is_trxn_exist > 0:
                if nav_initilization_flag[0]==0:
                    nav=100
                    units=sum_of_todays_security/nav
                    logging.debug('Initialized the nav to 100 and calculated units to %s',units)
                    #print(user_id,Date,sum_of_security_count,sum_of_todays_security,units,nav)
                    profile_insert='''INSERT INTO public.user_stock_profile_daily(user_id,stock_date,security_count,profile_value,units,nav) VALUES(%s,%s,%s,%s,%s,%s)'''
                    data=(user_id,Date,sum_of_security_count,sum_of_todays_security,units,nav)
                    cur.execute(profile_insert,data)
                    logging.debug('Inserted stock data usisng SQL %s \ndata %s',profile_insert,data)
                else:
                    get_prv_day_units='''SELECT units FROM public.user_stock_profile_daily WHERE user_id=%s and stock_date =(SELECT max(stock_date) FROM public.user_stock_profile_daily WHERE stock_date< %s)'''
                    get_prv_day_units_data=(user_id,Date)
                    cur.execute(get_prv_day_units,get_prv_day_units_data)
                    prev_day_units=cur.fetchone()
                    nav=sum_of_todays_security/prev_day_units[0]
                    logging.debug('Fetched units of previuos day from database units %s calculated todays nav=sum_of_todays_security/prev_day_units[0] nav:%s sum_of_todays_security:%s prev_day_units[0]:%s',prev_day_units[0],nav,sum_of_todays_security,prev_day_units[0])
                    #first delete then insert for same day
                    delete_stock_date_data='''DELETE FROM public.user_stock_profile_daily WHERE stock_date=%s'''
                    cur.execute(delete_stock_date_data,(Date,))
                    data=(user_id,Date,sum_of_security_count,sum_of_todays_security,prev_day_units[0],nav)
                    profile_insert='''INSERT INTO public.user_stock_profile_daily(user_id,stock_date,security_count,profile_value,units,nav) VALUES(%s,%s,%s,%s,%s,%s)'''
                    cur.execute(profile_insert,data)
                    #print(user_id,Date,sum_of_security_count,sum_of_todays_security,prev_day_units[0],nav)
                    logging.debug('Inserted stock data usisng SQL %s \ndata %s',profile_insert,data)
            else:
                logging.debug('No stock data to processs for %s',datetime.datetime.now())
            con.commit()
            cur.close()
            con.close()
            logging.info('Closed connection to database')
        except (ValueError, urllib.error.HTTPError) as e:
            logging.exception("Following is the exception occured http: %s", e)
            if 'not enough values to unpack' in str(e) or 'HTTP Error 404' in str(e):
                logging.debug('Inside except of user_profile_value_daily')
                uri="https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0"
                req=urllib.request.Request(uri)
                res=urllib.request.urlopen(req)
                logging.debug('updating session variables for %s',uri)
                page_data_str=res.read().decode('utf-8')
                parser = MyHTMLParser()
                MyHTMLParser.url=uri
                parser.feed(page_data_str)
                logging.debug('updating session variables for %s completed',uri)
            sys.exit(11)
        except Exception as e:
            logging.exception("Following is the exception occured: %s", e)
            #print(e)
            sys.exit(11)



    def user_profile_refresh(self, user, refreshtype='only_changed'):
        try:
            self.user=user
            self.refresh_type=refreshtype
            logging.debug('Inside user_profile_refresh called by user_profile_refresh(self, %s, %s)',self.user,self.refresh_type)
            logging.info('Connecting to database')
            con = psycopg2.connect("dbname="+os.environ['DB_NAME']+" user="+os.environ['DB_USER']+" host="+os.environ['DB_HOST']+" port="+os.environ['DB_PORT']+" password="+os.environ['DB_PASS'])
            cur = con.cursor()
            logging.info('Successfully connected to database')
            '''if Full refresh deletes the complete profile and recalculate it till todays date else only calculates for changed stocks
            '''
            if self.refresh_type=='full':
                logging.debug('DELETE FROM public.user_stock_profile_daily WHERE user_id=%s',self.user)
                user_profile_delete_query='''DELETE FROM public.user_stock_profile_daily WHERE user_id=%s'''
                cur.execute(user_profile_delete_query, (user,))
                logging.debug('DELETE FROM public.user_stock_profile_daily WHERE user_id=%s completed',self.user)
                logging.debug('update public.user_stocks_trxn set trxn_flag=0 where user_id=%s',self.user)
                user_stock_trxn_update_query='''update public.user_stocks_trxn set trxn_flag=0 where user_id=%s'''
                cur.execute(user_stock_trxn_update_query, (user,))
                logging.debug('update public.user_stocks_trxn set trxn_flag=0 where user_id=%s completed',self.user)
#add is_active flag in where clause
            user_stock_trxn_query='''SELECT user_id,slb.security_code,security_count,trxn_date,trxn_type,slb.security_id, trim( TRAILING '.' from slb.security_name) as security_name,ust._id FROM public.user_stocks_trxn ust
                                     JOIN public.stock_list_bse slb ON ust.security_code=slb.security_code WHERE ust.user_id=%s and trxn_flag=0 order by ust.trxn_date asc'''
            cur.execute(user_stock_trxn_query, (self.user, ))
            user_trxns=cur.fetchall()
            if cur.rowcount < 1:
                logging.debug('No data to refresh the profile')
            for security in user_trxns:
            #check if time_taken set if yes wait till time_taken is NULL max wait should be 1 min.
                            #if time_taken + 5 mins is less than current date take the transaction
                            #check if there are some transactions which need to be rollbacked condition would be parent_id = current id and is_active = 0 and trxn_flag = 0
                            #if yes first rollback them by fetching the data from from trxn_date to that current date and subtracting there values from daily_profile_values
                            #commit after processing each transaction in all cases rollback or successful
                user_id,security_code,security_count,trxn_date,trxn_type,security_id,security_name,trxn_seq_id=security[0],security[1],security[2],security[3],security[4],security[5],security[6],security[7]
                security_code=str(security_code)
                secobj=bse_ops()
                secdata=secobj.get_bse_stock_data(trxn_date, security_code, security_id, security_name)
                security_data=list()
                for line in secdata:
                    #print(line)
                    Date,Open_Price,High_Price,Low_Price,Close_Price,WAP,No_of_Shares,No_of_Trades,Total_Turnover,Deliverable_Quantity,Perc_Deli_Qty_to_Traded_Qty,Spread_HighVSLow,Spread_CloseVSOpen=line.decode('utf-8').replace('\n','').replace('\r','').split(',')
                    if Date=='Date':
                        continue
                    security_data.append((Date,Close_Price))
                security_data.sort(key=self.sortFirst)
                logging.info('Sorted stock data %s',security_data)
                is_calculated='No'
                for line in security_data:
                    user_profile_delete_query='''SELECT count(_id) from nav_user WHERE _id=%s AND need_full_refresh = 1'''
                    cur.execute(user_profile_delete_query, (user,))
                    full_refresh_count=cur.fetchone()
                    if full_refresh_count[0] == 1 :
                          logging.debug('DELETE FROM public.user_stock_profile_daily WHERE user_id=%s',self.user)
                          user_profile_delete_query='''DELETE FROM public.user_stock_profile_daily WHERE user_id=%s'''
                          cur.execute(user_profile_delete_query, (user,))
                          logging.debug('DELETE FROM public.user_stock_profile_daily WHERE user_id=%s completed',self.user)
                          logging.debug('update public.user_stocks_trxn set trxn_flag=0 where user_id=%s',self.user)
                          user_stock_trxn_update_query='''update public.user_stocks_trxn set trxn_flag=0 where user_id=%s'''
                          cur.execute(user_stock_trxn_update_query, (user,))
                          logging.debug('update public.user_stocks_trxn set trxn_flag=0 where user_id=%s completed',self.user)
                          return
                    Date,Close_Price=line[0],line[1]
                    #add is_active flag here
                    nav_initial_query='''SELECT count(nav) FROM public.user_stock_profile_daily WHERE stock_date=(SELECT MIN(trxn_date) FROM public.user_stocks_trxn where user_id=%s)'''
                    cur.execute(nav_initial_query,(user,))
                    nav_initilization_flag=cur.fetchone()
                    logging.debug('nav_initilization_flag %s',nav_initilization_flag[0])
                    if nav_initilization_flag[0]==0:
                        nav=100
                        units=security_count*float(Close_Price)/nav
                        profile_insert='''INSERT INTO public.user_stock_profile_daily(user_id,stock_date,security_count,profile_value,units,nav) VALUES(%s,%s,%s,%s,%s,%s)'''
                        data=(self.user,Date,security_count,security_count*float(Close_Price),units,nav)
                        cur.execute(profile_insert,data)
                        logging.debug('Initialized nav to 100 and calculated units %s for user %s and inserted data for date %s security_count %s profiele value %s',units,self.user,Date,security_count,security_count*float(Close_Price))
                    else:
                        check_nav_vale_query='''SELECT nav,units FROM public.user_stock_profile_daily WHERE stock_date=%s and user_id=%s'''
                        cur.execute(check_nav_vale_query,(Date,user_id))
                        check_inser_or_upd=cur.rowcount
                        if check_inser_or_upd==0:
                            logging.debug('Inside insert clause first stock data to be pushed in database for date %s',Date)
                            get_prv_day_units='''SELECT units FROM public.user_stock_profile_daily WHERE user_id=%s and stock_date =(SELECT max(stock_date) FROM public.user_stock_profile_daily WHERE stock_date< %s)'''
                            get_prv_day_units_data=(user_id,Date)
                            cur.execute(get_prv_day_units,get_prv_day_units_data)
                            prev_day_units=cur.fetchone()
                            logging.debug('Fetched previuos days units %s',prev_day_units[0])
                            nav=security_count*float(Close_Price)/prev_day_units[0]
                            data=(self.user,Date,security_count,security_count*float(Close_Price),prev_day_units[0],nav)
                            profile_insert='''INSERT INTO public.user_stock_profile_daily(user_id,stock_date,security_count,profile_value,units,nav) VALUES(%s,%s,%s,%s,%s,%s)'''
                            cur.execute(profile_insert,data)
                            logging.debug('Inserted records using SQL %s \nwith data %s',profile_insert,data)
                        else:
                            logging.debug('Inside update clause for stock data to be pushed in database for date %s',Date)
                            get_nav='''SELECT nav FROM public.user_stock_profile_daily WHERE user_id=%s and stock_date =%s'''
                            get_nav_data=(user_id,Date)
                            cur.execute(get_nav,get_nav_data)
                            nav_data=cur.fetchone()
                            logging.debug('Fetched previuos days nav %s for date %s',nav_data[0],Date)
                            #print(Date,type(Date) ,trxn_date,type(trxn_date), trxn_date.strftime("%d-%B-%Y"))
                            if Date==trxn_date.strftime("%d-%B-%Y"):
                                units=security_count*float(Close_Price)/nav_data[0]
                                #print(Date, trxn_date, units)
                                is_calculated='Yes'
                            elif is_calculated=='No':
                                #get data for previous days trxn *************************trxn_end_date function modified
                                is_calculated='Yes'
                            final_units=units
                            #print('final_units: ' ,final_units)
                            profile_value_per_stock_per_date=security_count*float(Close_Price)
                            data=(security_count,profile_value_per_stock_per_date,final_units,user_id,Date)
                            if trxn_type=='Buy':
                                profile_update='''UPDATE public.user_stock_profile_daily SET  security_count= security_count+%s , profile_value=profile_value+%s, units=units+%s WHERE user_id=%s AND stock_date=%s'''
                            if trxn_type=='Sell':
                                profile_update='''UPDATE public.user_stock_profile_daily SET  security_count= security_count-%s , profile_value=profile_value-%s, units=units-%s WHERE user_id=%s AND stock_date=%s'''
                            cur.execute(profile_update,data)
                            logging.debug('updating profile value using SQL %s \nand data %s',profile_update,data)
                update_nav_query='''UPDATE public.user_stock_profile_daily SET nav=profile_value/units WHERE stock_date > %s and user_id=%s'''
                update_nav_query_date=(trxn_date,user_id)
                cur.execute(update_nav_query,update_nav_query_date)
                logging.debug('Updated profile for nav using SQL %s \nand data %s',update_nav_query,update_nav_query_date)
                update_trxn_flag_query='''UPDATE public.user_stocks_trxn SET trxn_flag=1 WHERE _id=%s'''
                update_trxn_flag_data=(trxn_seq_id,)
                cur.execute(update_trxn_flag_query,update_trxn_flag_data)
                logging.debug('updated stock trxn table for trxn_flag with SQL %s \nand data %s',update_trxn_flag_query,update_trxn_flag_data)
            if self.refresh_type=='full':
                logging.debug('UPDATE nav_user SET need_full_refresh=0 WHERE user_id=%s',self.user)
                user_profile_delete_query='''UPDATE nav_user SET need_full_refresh=0 WHERE user_id=%s'''
                cur.execute(user_profile_delete_query, (user,))
                logging.debug('UPDATE nav_user SET need_full_refresh=0 WHERE user_id=%s completed',self.user)
            con.commit()
            cur.close()
            con.close()
            logging.info('Closed database connection')
        except (ValueError, urllib.error.HTTPError) as e:
            logging.exception("Following is the exception occured http: %s", e)
            if 'not enough values to unpack' in str(e) or 'HTTP Error 404' in str(e):
                logging.debug('Inside except of user_profile_refresh')
                uri="https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0"
                req=urllib.request.Request(uri)
                res=urllib.request.urlopen(req)
                page_data_str=res.read().decode('utf-8')
                logging.debug('updating session variables for %s', uri)
                parser = MyHTMLParser()
                MyHTMLParser.url=uri
                parser.feed(page_data_str)
                logging.debug('updating session variables for %s completed',uri)
            sys.exit(11)
        except Exception as e:
            logging.exception("Following is the exception occured: %s", e)
            #print(e)
            sys.exit(11)

#obj=db_connection()
#query1='''SELECT * from public.nav_user'''
#data=obj.executequery(query1)
#print(data)
'''secobj=bse_connection()
trxn_date=datetime.datetime.strptime('20180711','%Y%m%d')
security_code='532755'
security_id='TECHM'
security_name='TECH MAHINDRA LTD'
print(trxn_date)
secdata=secobj.get_bse_stock_data(trxn_date, security_code, security_id, security_name)
print(secdata)
for line in secdata:
    print(line)
upo=user_profile_ops()
upo.user_profile_refresh('5')
'''
