import schedule
from datetime import datetime
import time


def job(t):
   return print ("its running")

now = datetime.now()

# Example 3
s = now.strftime("%-I %p %S")
print('\nExample 3:', s)

print(now)
 
schedule.every().day.at("01:00").do(job)

 