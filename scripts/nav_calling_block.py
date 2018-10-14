#cd F:\VIDEOS\python1\New folder
#C:\Users\Rajendra\AppData\Local\Programs\Python\Python36-32\Python.exe F:\VIDEOS\python1\New folder\portfolio-insights\scripts\nav_calling_block.py
#C:\Users\Rajendra\AppData\Local\Programs\Python\Python36-32\Python.exe F:\VIDEOS\python1\New folder\portfolio-insights\scripts\nav_calling_block.py bslu
#C:\Users\Rajendra\AppData\Local\Programs\Python\Python36-32\Python.exe F:\VIDEOS\python1\New folder\portfolio-insights\scripts\nav_calling_block.py crpv 5
#C:\Users\Rajendra\AppData\Local\Programs\Python\Python36-32\Python.exe F:\VIDEOS\python1\New folder\portfolio-insights\scripts\nav_calling_block.py rpv 5
#C:\Users\Rajendra\AppData\Local\Programs\Python\Python36-32\Python.exe F:\VIDEOS\python1\New folder\portfolio-insights\scripts\nav_calling_block.py dpv 5
import sys
import os
import logging
from nav_moduler import user_profile_ops
from nav_moduler import bse_ops
import datetime
import time

class ErrorInSubProc(Exception):
   """Base class for other exceptions"""
   pass

try:
    now = datetime.datetime.now().strftime("%d%m%Y")
    log_file_name='portfolio_tracking_calling_block'+now+'.log'
    logging.basicConfig(filename=os.path.join("log",'portfolio_insights_'+now+'.log'),format='%(asctime)s:%(levelname)s:%(message)s',level=logging.DEBUG)
    #deleting the logs file older than 4 days
    days_to_remove=4
    directory_to_clean=os.getcwd()+"\log"
    for dirpath, dirnames, filenames in os.walk(directory_to_clean):
       for file in filenames:
          curpath = os.path.join(dirpath, file)
          file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
          if datetime.datetime.now() - file_modified > datetime.timedelta(hours=days_to_remove*24):
             logging.info('Deleting the file : %s',curpath)
             os.remove(curpath)
    usage_text='''Comammand line arguments are not properly provided. Usage is as mentioned below:
    1. To update all bse stock list
        nav_calling_block.py bslu

    2.To calculate todays profile value:
        nav_calling_block.py dpv <user_id>

    3.To refresh profile after stocks modification:
        nav_calling_block.py rpv <user_id>

    4.To complete refrsh profile:
        nav_calling_block.py crpv <user_id>'''
    profile_value_ops=['dpv','rpv','crpv']
    program_name=sys.argv[0]
    number_of_arguments=len(sys.argv)
    return_code=0
    if number_of_arguments < 2:
        logging.error('command issued is %s \n%s',str(sys.argv),usage_text)
    else:
        logging.info('Program name: %s number of arguments: %s command issued: %s',program_name,number_of_arguments,str(sys.argv))
        module_call=sys.argv[1]
        upo=user_profile_ops()
        boo=bse_ops()
        if number_of_arguments == 2 and module_call == 'bslu':
            logging.debug('Calling nav_stock_list_bse.py')
            return_code=boo.get_bse_stocks()
            if return_code is not None and return_code != 0:
                    raise ErrorInSubProc
            logging.debug('Exited from nav_stock_list_bse.py')
        elif number_of_arguments == 2 and module_call != 'bslu':
            logging.error('command issued is %s \%s',str(sys.argv),usage_text)
        elif number_of_arguments ==3 and module_call in profile_value_ops:
            user_inpt=sys.argv[2]
            if module_call == 'dpv':
                logging.debug('Calling upo.user_profile_value_daily(%s)',user_inpt)
                return_code=upo.user_profile_value_daily(user_inpt)
                if return_code is not None and return_code != 0:
                    raise ErrorInSubProc
                logging.debug('Exited from upo.user_profile_value_daily(%s)',user_inpt)
            if module_call == 'rpv':
                logging.debug('Calling upo.user_profile_refresh(%s,''only_changed'')',user_inpt)
                return_code=upo.user_profile_refresh(user_inpt, 'only_changed')
                logging.debug('retuned code %s',return_code)
                if return_code is not None and return_code != 0:
                    raise ErrorInSubProc
                logging.debug('Exited from upo.user_profile_refresh(%s,''only_changed'')',user_inpt)
            if module_call == 'crpv':
                logging.debug('Calling upo.user_profile_refresh(%s,''full'')',user_inpt)
                return_code=upo.user_profile_refresh(user_inpt, 'full')
                print(return_code)
                if return_code is not None and return_code != 0:
                    raise ErrorInSubProc
                logging.debug('Exited from upo.user_profile_refresh(%s,''full'')',user_inpt)
        elif number_of_arguments ==3 and module_call not in profile_value_ops:
            logging.error('command issued is %s \n%s',str(sys.argv),usage_text)
        else:
            logging.error('command issued is %s \n%s',str(sys.argv),usage_text)
except Exception as e:
    logging.exception("Following is the exception occured calling block:")
    #print(e)
    sys.exit(12)
