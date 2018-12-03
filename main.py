from flask import Flask, render_template, request
from pprint import pprint
import psutil
import json
import datetime
import socket

app = Flask(__name__)

def gettimef(time):
    return datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")

def getnumf(x, p):
    return round(x, p) if x!=None else 0

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

@app.route('/')
def index():
    
    cputimes = psutil.cpu_times()._asdict()
    for i in cputimes:
        cputimes[i] = secs2hours(cputimes[i])
    cpustats = psutil.cpu_stats()._asdict()
    
    users = []
    for u in psutil.users():
        users.append(u._asdict())
    for u in users:
        u['started'] = gettimef(u['started'])

    processes = []
    for p in psutil.process_iter():
        processes.append(p.as_dict())
    for p in processes:
        p['create_time'] = gettimef(p['create_time'])
        p['cpu_percent'] = getnumf(p['cpu_percent'], 2)
        p['memory_percent'] = getnumf(p['memory_percent'], 2)
        p['num_threads'] = getnumf(p['num_threads'], 2)

    vm = psutil.virtual_memory()._asdict()
    for key in vm:
        if key!='percent':
            vm[key] = str(round(vm[key]/1000000,2)) + ' M'

    sm = psutil.swap_memory()._asdict()
    for key in sm:
        if key!='percent':
            sm[key] = str(round(sm[key]/1000000,2)) + 'M'

    host = socket.gethostname()
    boottime = gettimef(psutil.boot_time())

    return render_template('index.html', cputimes=cputimes, cpustats=cpustats, procs=processes, vm=vm, sm=sm, users=users, host=host, boottime=boottime)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
