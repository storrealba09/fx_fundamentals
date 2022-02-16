import parsedatetime
import pytz
from pytz import timezone
from datetime import datetime


def parsertime(time):
    cal = parsedatetime.Calendar()
    if time[-3:] == 'ago':
        datetime_obj= cal.parseDT(datetimeString=time)

        datetime_obj = datetime_obj[0].timestamp()
        #print(datetime_obj)
        #datetime_obj = datetime.strptime(time)
    else:
        if (len(time) > 19):
            datetime_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
            datetime_obj = datetime_obj.timestamp()
        else:
            datetime_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
            datetime_obj = datetime_obj.timestamp()
        #print(datetime_obj)

    #print(datetime_obj)
    return datetime_obj
