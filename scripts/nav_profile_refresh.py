import urllib
import urllib.parse
import urllib.request
from ast import literal_eval
import psycopg2
import datetime

def sortFirst(val):
    return datetime.datetime.strptime(val[0],'%d-%B-%Y')

uri="https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?expandable=7&flag=0"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

formFields = (
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

user_stock_list=list()
con = psycopg2.connect("dbname='PortFolio_Tracking' user='portfolio_tracking' host='127.0.0.1' port='5432' password='portfolio_tracking'")
cur = con.cursor()
all_users_query='''SELECT DISTINCT user_id FROM stocks.user_stocks_trxn'''
cur.execute(all_users_query)
user_stock_rows=cur.fetchall()
for user in user_stock_rows:
    print(user[0])
    user_stock_trxn_query='''SELECT user_id,security_code,security_count,trxn_date,trxn_type,slb."Security_Id", trim( TRAILING '.' from slb."Security_Name") as Security_Name, trxn_seq_id FROM stocks.user_stocks_trxn ust
JOIN stocks.stock_list_bse slb ON ust.security_code=slb."Security_Code" WHERE ust.user_id=%s and trxn_flag=0 order by ust.trxn_date asc'''
    cur.execute(user_stock_trxn_query, user)
    user_trxns=cur.fetchall()
    for security in user_trxns:
        user_id,security_code,security_count,trxn_date,trxn_type,security_id,security_name,trxn_seq_id=security[0],security[1],security[2],security[3],security[4],security[5],security[6],security[7]
        print(user_id,security_code,security_count,trxn_date,trxn_type,security_id,security_name,trxn_seq_id)
        security_code=str(security_code)
        security_start_date=trxn_date.strftime("%m/%d/%Y")
        txtFromDate=trxn_date.strftime("%d/%m/%Y") #'22/04/2017'
        now = datetime.datetime.now()
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
        print ('security_end_date : ', security_end_date, 'txtToDate :', txtToDate)
        modify_formFields=list(formFields)
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
        formFields=tuple(modify_formFields)
        data = urllib.parse.urlencode(formFields).encode("utf-8")
        req=urllib.request.Request(uri,data,headers)
        res=urllib.request.urlopen(req)
        security_data=list()
        for line in res:
            Date,Open_Price,High_Price,Low_Price,Close_Price,WAP,No_of_Shares,No_of_Trades,Total_Turnover,Deliverable_Quantity,Perc_Deli_Qty_to_Traded_Qty,Spread_HighVSLow,Spread_CloseVSOpen=line.decode('utf-8').replace('\n','').replace('\r','').split(',')
            if Date=='Date':
                continue
            security_data.append((Date,Close_Price))
        security_data.sort(key=sortFirst)
        print(security_data)
        for line in security_data:
            #print(line)
            Date,Close_Price=line[0],line[1]
            nav_initial_query='''SELECT count(nav) FROM stocks.user_stock_profile_daily WHERE stock_date=(SELECT MIN(trxn_date) FROM stocks.user_stocks_trxn where user_id=%s)'''
            cur.execute(nav_initial_query,user)
            nav_initilization_flag=cur.fetchone()
            print(nav_initilization_flag[0])
            if nav_initilization_flag[0]==0:
                nav=100
                units=security_count*float(Close_Price)/nav
                print(user[0],Date,security_count,security_count*float(Close_Price),units,nav)
                profile_insert='''INSERT INTO stocks.user_stock_profile_daily(user_id,stock_date,security_count,profile_value,units,nav) VALUES(%s,%s,%s,%s,%s,%s)'''
                data=(user[0],Date,security_count,security_count*float(Close_Price),units,nav)
                cur.execute(profile_insert,data)
            else:
                check_nav_vale_query='''SELECT nav,units FROM stocks.user_stock_profile_daily WHERE stock_date=%s and user_id=%s'''
                cur.execute(check_nav_vale_query,(Date,user_id))
                check_inser_or_upd=cur.rowcount
                if check_inser_or_upd==0:
                    get_prv_day_units='''SELECT units FROM stocks.user_stock_profile_daily WHERE user_id=%s and stock_date =(SELECT max(stock_date) FROM stocks.user_stock_profile_daily WHERE stock_date< %s)'''
                    get_prv_day_units_data=(user_id,Date)
                    cur.execute(get_prv_day_units,get_prv_day_units_data)
                    prev_day_units=cur.fetchone()
                    nav=security_count*float(Close_Price)/prev_day_units[0]
                    data=(user[0],Date,security_count,security_count*float(Close_Price),prev_day_units[0],nav)
                    profile_insert='''INSERT INTO stocks.user_stock_profile_daily(user_id,stock_date,security_count,profile_value,units,nav) VALUES(%s,%s,%s,%s,%s,%s)'''
                    cur.execute(profile_insert,data)
                else:
                    get_nav='''SELECT nav FROM stocks.user_stock_profile_daily WHERE user_id=%s and stock_date =%s'''
                    get_nav_data=(user_id,Date)
                    cur.execute(get_nav,get_nav_data)
                    nav_data=cur.fetchone()
                    #print(Date,type(Date) ,trxn_date,type(trxn_date), trxn_date.strftime("%d-%B-%Y"))
                    if Date==trxn_date.strftime("%d-%B-%Y"):
                        units=security_count*float(Close_Price)/nav_data[0]
                        print(Date, trxn_date, units)
                    final_units=units
                    print('final_units: ' ,final_units)
                    profile_value_per_stock_per_date=security_count*float(Close_Price)
                    data=(security_count,profile_value_per_stock_per_date,final_units,user_id,Date)
                    if trxn_type=='B':
                        profile_update='''UPDATE stocks.user_stock_profile_daily SET  security_count= security_count+%s , profile_value=profile_value+%s, units=units+%s WHERE user_id=%s AND stock_date=%s'''
                    if trxn_type=='S':
                        profile_update='''UPDATE stocks.user_stock_profile_daily SET  security_count= security_count-%s , profile_value=profile_value-%s, units=units-%s WHERE user_id=%s AND stock_date=%s'''
                    cur.execute(profile_update,data)
        update_nav_query='''UPDATE stocks.user_stock_profile_daily SET nav=profile_value/units WHERE stock_date > %s and user_id=%s'''
        update_nav_query_date=(trxn_date,user_id)
        cur.execute(update_nav_query,update_nav_query_date)
        update_trxn_flag_query='''UPDATE stocks.user_stocks_trxn SET trxn_flag=1 WHERE trxn_seq_id=%s'''
        update_trxn_flag_data=(trxn_seq_id,)
        print(update_trxn_flag_query, update_trxn_flag_data)
        cur.execute(update_trxn_flag_query,update_trxn_flag_data)
con.commit()
cur.close()
con.close()
