from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from myapi.views import *
from mysite.helpers import paystack
import time

def job(text):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} ---- {}'.format(text, t))

def start():
    scheduler = BackgroundScheduler()
    # charge = paystack.charge_pay
    # scheduler.add_job(charge, 'interval', days = 1, id='test', args=['sk_test_0e526a89d659c8eec286e8632df3b9d0159a49af', 
    # 'AUTH_4gouqooq96', 'emmapraise@gmail.com', '10000'], replace_existing = True)
    jobb = SchedulePayment.get_data
    scheduler.add_job(jobb, 'interval', minutes = 1, id='test2', args=['job1'], replace_existing = True) 
    # scheduler.remove_job('test2')
    scheduler.start()