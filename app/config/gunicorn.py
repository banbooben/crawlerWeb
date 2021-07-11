
import os

# from configs import sysconf
from config.server_conf import current_config

bind = current_config.BIND
# 启动的进程数
workers = current_config.WORK_NUMS
# timeout
timeout = 800
# 如果部署的时候开启了debug模式, 可以启用auto_reload
# reload = True


#
# x_forwarded_for_header = 'X-FORWARDED-FOR'
#
# loglevel = current_config.LOG_LEVEL
#
#
# file_name = os.path.join(current_config.LOG_DIR, "log.log")
#
