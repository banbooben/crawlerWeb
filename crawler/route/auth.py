#!/usr/local/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/22 11:36
# @Author  : shangyameng@aliyun.com
# @Site    : 
# @File    : auth.py

from flask import Blueprint, current_app, jsonify, g, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

from models.user import User


auth = Blueprint("auth", __name__)


@auth.route('/', methods=['POST'])
def login():
    if 'openid' not in request.json or 'session_key' not in request.json:
        return jsonify({'Bad Request': 'Incomplete information'}), 401

    user = User.query.filter_by(id=request.json['user_id']).first()

    if not user:
        return jsonify({'Bad Request': 'Invalid openid'}), 401
    elif user.name != request.json['username']:
        return jsonify({'Bad Request': 'Invalid session_key'}), 401

    # 生成token并返回
    s = Serializer(
        current_app.config['SECRET_KEY'],
        current_app.config['TOKEN_LIFETIME']
    )
    token = s.dumps({'name': user.name, 'password': user.password})
    return jsonify({'access_token': token.decode('utf8')})


# 请求认证
@auth.before_app_request
def authenticate():
    # 获取路由白名单
    white_list = current_app.config['URL_WHITE_LIST']
    # print("request.path", request.path)
    if request.path in white_list:
        # 判断请求方法
        if request.method in white_list[request.path]:
            return

    # 身份认证
    s = Serializer(current_app.config['SECRET_KEY'])

    if 'Authorization' not in request.headers:
        return jsonify({'Bad request': 'No Authorization in headers'}), 401
    try:
        user = s.loads(request.headers['Authorization'].encode('utf8'))
        # 认证成功，将token信息保存以便请求后续
        g.user = user
    except SignatureExpired:
        return jsonify({'Bad request': 'Signature has expired'}), 401
    except BadSignature:
        return jsonify({'Bad request': 'Bad Signature'}), 401
