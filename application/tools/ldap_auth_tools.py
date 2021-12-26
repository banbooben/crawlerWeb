# !/usr/bin/env python
# coding:utf-8
# @Time    : 2021/10/8 15:26
# @Contact : shangyameng@datagrand.com
# @Name    : ldap_auth_tools.py
# @Desc    :
import ldap
from application.initialization.logger_process import logger


class LDAPAuthTools(object):

    def __init__(self,
                 url="ldap://ad-idc.bdo.com.cn:389",
                 authentication="simple",
                 base_dn="dc=bdo,dc=com,dc=cn",
                 credentials="idSecure.2012",
                 ):
        """
        url:                ldap://ad-idc.bdo.com.cn:389/
        authentication:     simple
        root:               DC=bdo,DC=com,DC=cn
        credentials:        idSecure.2012
        """
        # self.username = username
        # self.password = password
        self.url = url
        self.authentication = authentication
        self.base_dn = base_dn
        self.credentials = credentials

    def auth(self,
             username,
             password,) -> tuple:
        try:
            ldap_conn = ldap.initialize(self.url)

            ldap_conn.protocol_version = ldap.VERSION3
            ldap_conn = ldap_conn.simple_bind_s(f"cn={username},{self.base_dn}", password)

            return True, ldap_conn
        except Exception as e:
            try:
                if e.args[0].get("desc", "") == "Invalid credentials":
                    return False, []
                else:
                    return False, ["connect error"]
            except Exception as ee:
                logger.exception(ee)
                return False, list(e.args)


if __name__ == '__main__':
    l = LDAPAuthTools(url="ldap://127.0.0.1:389", base_dn="dc=sarmn,dc=cn")
    status, res = l.auth("root", "admin")

    a = ""

#
# from ldap3 import Server, Connection, ALL, SIMPLE
#
# if __name__ == "__main__":
#     server = Server('127.0.0.1', get_info=ALL)
#
#     # user必须为 'Domain名称\\用户名' , 或者'域名\\用户名'
#     try:
#         conn = Connection(server, user="cn=sarmn,dc=sarmn,dc=cn", password="admin", authentication=SIMPLE,
#                           auto_bind=True)
#         # 启用tls加密
#         # conn.start_tls()
#         print(conn.extend.standard.who_am_i())
#
#         # 查找所有用户用户
#         conn.search('dc=sarmn, dc=cn', '(objectclass=person)')
#         print(conn.entries)
#         print('========================================================')
#         # 查找某一ou下的用户
#         conn.search('ou=zsb, dc=sarmn, dc=cn', '(objectclass=person)')
#         print(dir(conn.entries[0]))
#         print(conn.entries[0].entry_to_json())
#         print('========================================================')
#         # 查找所有管理员帐户
#         conn.search('dc=sarmn, dc=cn', '(&(objectclass=person)(uid=admin))')
#         print(conn.entries)
#         print('========================================================')
#         # 添加用户
#         print(conn.add('cn=python,ou=zsb,dc=sarmn, dc=cn', 'User',
#                        {'givenName': 'Python测试', 'sn': 'test', 'departmentNumber': 'vvvv',
#                         'telephoneNumber': 1313131313}))
#     except Exception as e:
#         print(e)
#         print('认证失败,请检查用户名密码')
#     # print(server.info)
#     # print(server.schema)
