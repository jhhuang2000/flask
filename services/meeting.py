# encoding=utf8
import json
import os
import time

import requests

from models import db
from models.TaskModel import Task


class Meeting(object):
    def __init__(self, start_grab=False, *args, **kwargs):
        from config.scheduler import scheduler
        self.app = scheduler.app
        self.params = dict(kwargs)
        self.login_succeed = True
        self.duration = int(self.params['end_time'][:2]) - int(self.params['start_time'][:2])
        self.time = self.params['start_time'][:2] + '-' + self.params['end_time'][:2]
        self.login_api = '*/mr/login/doLogin'
        self.reserved_api = '*/mr/ajax/getMyRoomInfo.action'
        self.get_rooms_api = '*/mr/ajax/selectRoomInfo.action'
        self.reserve_api = '*/mr/ajax/reserveRoom.action'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
        }
        self.cookie_file = 'cookies/' + self.params['account'] + '|' + self.params['pwd'] + '.txt'
        self.session_req = requests.session()
        self.session_req.headers = self.headers
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file, 'r') as f:
                load_cookies = json.loads(f.read())
            self.session_req.cookies = requests.utils.cookiejar_from_dict(load_cookies)
        else:
            self.login()
        if start_grab:
            self.start_grab()

    def get_correct_room(self):
        room_list = self.get_rooms()
        correct = False
        room = None
        owner = ''
        if not room_list:
            return correct, room, owner
        for row in room_list:
            # 武汉梦工厂3号楼#楼13层贝多芬
            room_name = row['area'] + row['building'] + '#楼' + row['floor'] + '层' + row['roomNum']
            if room_name == self.params['room']:
                for reserve_info in row['revseredList']:
                    if self.params['start_time'][:2] <= reserve_info['beginTime'][:2] < self.params['end_time'][:2]:
                        if reserve_info['used'] == '0':
                            correct = True and not owner
                            room = row
                        else:
                            correct = False
                            reserve_user = reserve_info['reserveInfo']
                            owner += '[{}|{}|{}-{}],'.format(
                                reserve_user['revUserName'],
                                reserve_user['revUserPhone'],
                                reserve_info['beginTime'],
                                reserve_info['endTime'],
                            )
                break
        return correct, room, owner

    def start_grab(self):
        (correct, room, owner) = self.get_correct_room()
        reserved = False
        try_times = 0
        if not correct:
            self.mark_grab_status(reserved, try_times, owner)
            return False

        error_info = None
        while try_times < self.app.config.get('GRAB_MEETING_TRY_TIMES', 31) \
                and not reserved \
                and error_info != '该时间段会议室已被预定，请重新选择！' \
                and error_info != '一周内最多预定次数为5次,已经超过限制！':
            time.sleep(0.1)
            try_times += 1
            (reserved, error_info) = self.reserve_room(room['roomId'])
        self.mark_grab_status(reserved, try_times, owner, error_info)
        return reserved

    def mark_grab_status(self, reserved, try_times, owner, error_info=None):
        task = Task.query.filter(Task.id == self.params['id']).first()
        if reserved:
            task.status_text = '成功, 第{}次时 {}'.format(try_times, owner)
        else:
            self.app.logger.error('account: %s, 预订[%s] 失败, (%s)', self.params['account'], self.params['room'], owner)
            task.status_text = '失败, 共抢{}次 {} {}'.format(try_times, owner, error_info)

        db.session.add(task)
        db.session.commit()

    def reserve_room(self, room_id):
        res = self.session_req.post(self.reserve_api, {
            'id': room_id,
            'date': self.params['date'],
            'title': '例会',
            'remark': '',
            'time': self.time,
        })
        self.app.logger.info('reserve_room[%s] %s', res.status_code, res.text)
        try:
            if res.json()['statusDesc'] == 'ok':
                return True, '预订成功'
            else:
                return False, res.json()['statusDesc']
        except Exception as e:
            self.app.logger.error('reserve_room[%s] %s (%s)', res.status_code, res.text, e)
            return False, 'exception'

    def get_rooms(self, try_times=1):
        res = self.session_req.post(self.get_rooms_api, {
            'pageNo': '1',
            'pageSize': '100',
            'date': self.params['date'],
            'startTime': '',
            'duration': '',
            'building': '',
            'floor': '',
            'minNum': '',
            'maxNum': '',
            'hasProjector': '',
            'area': self.params['city'],
            'hasVideoConferenceSystem': '',
        }, allow_redirects=False)

        if res.status_code == 302 and try_times < 3:
            self.login()
            res = self.get_rooms(try_times + 1)
            if res:
                return res
        elif res.status_code == 200:
            return res.json()['data']['dataList']['rows']
        else:
            self.login_succeed = False
            self.app.logger.error('get_rooms[%s]: %s (%s)', res.status_code, res.text, try_times)

    def login(self):
        self.session_req.cookies = requests.utils.cookiejar_from_dict({})
        login_res = self.session_req.post(self.login_api, {
            'username': self.params['account'],
            'password': self.params['pwd']
        })
        with open(self.cookie_file, 'w') as f:
            cookie_dict = requests.utils.dict_from_cookiejar(login_res.cookies)
            json.dump(cookie_dict, f)
            self.session_req.cookies = requests.utils.cookiejar_from_dict(cookie_dict)

        return True
