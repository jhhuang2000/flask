# encoding=utf8
import atexit
import fcntl
from datetime import datetime, timedelta

from flask_apscheduler import APScheduler

from models.TaskModel import Task
from services.meeting import Meeting

scheduler = APScheduler()


def init_app(app):
    try:
        f = open('scheduler.lock', 'wb')
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()

        for task in Task.query.filter(Task.status_text == '未开始').all():
            save_meeting_job(task)
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)


def save_meeting_job(task):
    if datetime.today().date() + timedelta(days=6) < task.date:
        next_run_time = (task.date + timedelta(days=-6)).strftime('%Y-%m-%d 10:59:59')
    elif datetime.now().strftime('%H:%M:%S') <= '10:59:59':
        next_run_time = datetime.now().strftime('%Y-%m-%d 10:59:59')
    else:
        next_run_time = datetime.now()

    meeting_kwargs = task.to_dict()
    meeting_kwargs['start_grab'] = True
    scheduler.add_job(
        id=str(task.id),
        name=task.room,
        func=Meeting,
        next_run_time=next_run_time,
        kwargs=meeting_kwargs,
        replace_existing=True
    )
