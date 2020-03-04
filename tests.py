from datetime import datetime
import pytz

d = datetime.now()
#.strftime('%Y-%m-%d:%H_%M_%S')
print(d.tzinfo) # Return time zone info

d = pytz.timezone('Europe/Paris').localize(d)
print(d.strftime('%Y-%m-%d %H:%M:%S'))