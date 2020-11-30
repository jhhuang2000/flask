# encoding=utf8
from datetime import datetime, timedelta

from flask import Blueprint, g

from config.auth import auth
from config.scheduler import save_meeting_job
from models import db
from models.TaskModel import Task
from services.meeting import Meeting
from utils.helper import *

task = Blueprint('task', __name__)


@task.route('index', methods=(['GET']))
@auth.login_required
def index():
    """
    @api {get} /task/index 任务列表
    @apiName task_index
    @apiGroup task
    @apiParam {Number} [page=1] 当前页码
    @apiParam {Number} [page_size=1] 当前页码
    @apiUse auth
    """
    query = Task.query.filter(Task.em == '{0}'.format(g.user['employeeId263']))
    return list_return(query)


@task.route('save', methods=(['POST']))
@auth.login_required
def save():
    """
    @api {post} /task/save 保存/创建任务(当有id时即为修改)
    @apiName task_save
    @apiGroup task
    @apiParam {Number} [id] 主键id(当有id时即为修改)
    @apiParam {String} city 城市
    @apiParam {String} room 格式(武汉梦工厂3号楼#楼13层贝多芬)更多的详情可以问娇小姐姐
    @apiParam {Date} date 预约日期
    @apiParam {Date} start_time 开始时间
    @apiParam {Date} end_time 结束时间
    @apiParam {String} account 账号
    @apiParam {String} pwd 密码
    @apiUse auth
    """
    form = request.form.to_dict()

    if int(form['end_time'][:2]) - int(form['start_time'][:2]) > 4:
        return error_return("预定时间不能超过4小时~")
    not_start_task = Task.query.filter(
        Task.status_text == '{0}'.format('未开始'),
        Task.account == '{0}'.format(form['account'])
    ).first()
    if not_start_task and not_start_task.pwd != form['pwd']:
        return error_return('是密码输错了嘛~ 再试一次吧小主~')

    choose_date = datetime.datetime.strptime(form['date'], '%Y-%m-%d')
    start_of_week = choose_date - timedelta(days=choose_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    book_num = Task.query.filter(
        Task.account == '{0}'.format(form['account']),
        Task.date.between(start_of_week.date(), end_of_week.date())
    ).count()
    if book_num > 4:
        return error_return(
            '一周['
            + start_of_week.date().strftime('%Y-%m-%d')
            + '-' + end_of_week.date().strftime('%Y-%m-%d')
            + ']内至多只能预订5个~'
        )

    form['em'] = g.user['employeeId263']
    meeting = Meeting(**form)
    (correct, room, owner) = meeting.get_correct_room()
    if not correct:
        if not meeting.login_succeed:
            return error_return('登陆失败 账号密码不对~')
        if owner:
            return error_return('已被: {} 占据'.format(owner))
        return error_return('房间名格式不对~ 应该为跟您客户端看到的房间名完全一致~')
    if 'id' in form:
        task = Task.query.filter(
            Task.id == '{0}'.format(form['id']),
            Task.em == '{0}'.format(g.user['employeeId263'])
        ).first()
        if not task:
            return error_return()
        for key in form:
            if hasattr(task, key):
                setattr(task, key, form[key])
    else:
        task = Task(**form)

    db.session.add(task)
    db.session.commit()
    save_meeting_job(task)
    return success_return()


@task.route('delete', methods=(['POST']))
@auth.login_required
def delete():
    """
    @api {post} /task/delete 删除任务
    @apiName task_delete
    @apiGroup task
    @apiParam {Number} id 主键id
    @apiUse auth
    """
    task_id = request.form.get('id')
    task = Task.query.filter(
        Task.id == '{0}'.format(task_id),
        Task.em == '{0}'.format(g.user['employeeId263'])
    ).first()
    db.session.delete(task)
    db.session.commit()
    from config.scheduler import scheduler
    try:
        scheduler.delete_job(str(task.id))
    except:
        pass
    return success_return()
