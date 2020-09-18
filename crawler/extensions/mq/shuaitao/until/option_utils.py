#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import datetime
from queue import Queue

from src.until.db_until import SQLManager
from src.device.common_device_tools import add_face, del_face, edit_face
from src.device.device_api.jd_device_utils import JD
from src.device.device_api.tv_device_utils import TV
from src.until.conmon_utils import get_str_time, get_code_in_device_from_people_code
import json


class PeopleDeviceOption:

    def __init__(self, opt_data):
        self.people_code = opt_data.get("people_code", '')
        self.name = opt_data.get("name", '')
        self.people_data = json.loads(opt_data.get("people_data", ''))  # 人员数据
        self.device_imei = opt_data.get("device_imei", '')  # 设备的代码 即imei
        self.device_type = opt_data.get("device_type", '')  # 设备的类型 6002,6003 为EGC-E900， 6004为同为
        self.device_ip = opt_data.get("device_ip", '')
        self.id = opt_data.get("id")  # 这条操作数据的id
        self.operate = opt_data.get("operate")
        self.user_id = opt_data.get("user_id")
        self.device_people_id = opt_data.get("device_people_id")
        if self.device_type == "6004":
            self.obj = TV
            self.device_port = "80"
        elif self.device_type == "6002" or self.device_type == "6003":
            self.obj = JD
            self.device_port = "9300"

    def result_deal(self, res):
        """
        处理下发结果
        :param res:operate 1 增加  2 修改 3删除
        :return: sync_status：
        """
        res_code = res.get("StatusCode")
        res_describe = res.get("Describe")
        msg = "响应码：" + res_code + ", 描述：" + res_describe
        if self.operate == "1":
            if res.get("StatusCode") == "0" and res.get("RegisterID"):
                update_sql = f"""update utodoption set sync_result='{msg}',sync_status='1',sync_time='{get_str_time()}' where id='{self.id}'"""
                SQLManager.moddify(update_sql)
                return True
            else:
                data = {"sync_result": "下发失败====" + json.dumps(res), "sync_status": "2", "sync_time": get_str_time()}
                update_sql = f"""update utodoption set sync_result='{msg}',sync_status='2',sync_time='{get_str_time()}' where id='{self.id}'"""
                SQLManager.moddify(update_sql)
                print(data)
                return False
        elif self.operate == "2":
            if res.get("StatusCode") == "0":
                data = {"sync_result": "修改成功====" + json.dumps(res), "sync_status": "1", "sync_time": get_str_time()}
                update_sql = f"""update utodoption set sync_result='{msg}',sync_status='1',sync_time='{get_str_time()}' where id='{self.id}'"""
                SQLManager.moddify(update_sql)
                return True
            else:
                data = {"sync_result": "修改失败====" + json.dumps(res), "sync_status": "2", "sync_time": get_str_time()}
                update_sql = f"""update utodoption set sync_result='{msg}',sync_status='2',sync_time='{get_str_time()}' where id='{self.id}'"""
                SQLManager.moddify(update_sql)
                return False
        elif self.operate == "3":
            if res.get("StatusCode") == "0":
                update_sql = f"""update utodoption set sync_result='{msg}',sync_status='1',sync_time='{get_str_time()}' where id='{self.id}'"""
                SQLManager.moddify(update_sql)
                delsql = f"DELETE FROM device_people WHERE people_code='{self.people_code}' and device_code='{self.device_imei}'"
                print("删除人员code",self.people_code)
                SQLManager.moddify(delsql)
                return True
            else:
                update_sql = f"""update utodoption set sync_result='{msg}',sync_status='2',sync_time='{get_str_time()}' where id='{self.id}'"""
                SQLManager.moddify(update_sql)
                return False

    def add(self):
        """
        调用设备添加人员接口，下发成功写入device_people表
        :return:
        """
        res = add_face(self.obj, self.device_ip, self.device_port, self.device_imei, self.people_data)
        resp = self.result_deal(res)
        if resp:
            people_code = self.people_code
            registerID = res.get("RegisterID")
            device_code = self.device_imei
            create_time = get_str_time()
            keys = ["people_code", "device_code", "device_people_id", "create_time", "user_id"]
            values = [people_code, device_code, registerID, get_str_time(), self.user_id]
            SQLManager.create_or_update("device_people", (keys, values),
                                        {"device_code": device_code, "people_code": people_code})

    def modify(self):
        peo_in_device = get_code_in_device_from_people_code(self.people_data.get("job_number"),
                                                            self.people_data.get("imei"))
        self.people_data["register_id"] = peo_in_device
        res = edit_face(self.obj, self.device_ip, self.device_port, self.device_imei, self.people_data)
        print(res)
        self.result_deal(res)
        pass

    def delete(self):
        # peo_in_device = get_code_in_device_from_people_code(self.people_data.get("job_number"),
        #                                                     self.people_data.get("imei"))
        print("删除人员编号",self.device_people_id)
        res = del_face(self.obj, self.device_ip, self.device_port, self.device_imei, self.device_people_id)
        self.result_deal(res)
        pass

    def get_device_people(self):
        # res = add_face(self.obj,self.device_ip,self.device_port,self.device_imei,self.people_data)
        # self.result_deal(res)
        pass


#

# 查询数据库的下发任务
def distribute_work(flag=True):
    try:
        sql = "SELECT a.*,b.device_people_id FROM utodoption a LEFT JOIN device_people b on a.people_code = b.people_code where a.sync_status='0' and is_done= '0' and task_type='1' order by a.operate_time limit 10"
        work_lists = SQLManager.get_list(sql)
        if flag:
            if len(work_lists) > 0:
                for works in work_lists:
                    now_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
                    if works.get("operate_time", "") < now_time.strftime('%Y-%m-%d %H:%M:%S'):
                        try:
                            opt = PeopleDeviceOption(works)
                            if works.get("operate") == '1':  # 本地添加人员，同步到设备
                                opt.add()
                            elif works.get("operate") == '2':  # 本地修改人员头像，同步到设备
                                opt.modify()
                            elif works.get("operate") == '3':  # 本地删除人员，同步到设备
                                opt.delete()
                            elif works.get("operate") == '4':  # 设备同步到本地
                                opt.get_device_people()
                        except Exception as e:
                            print(e)
                            print(e, '下发任务报错了!!!!!!')
                        flag = True
                        distribute_work(flag)
            else:
                flag = False
                distribute_work(flag)
        else:
            return True
    except Exception as e:
        print(e)
