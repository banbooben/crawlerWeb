import json
import random
import uuid

import pika
import time
from application.initialization.application import logger


class RabbitBase(object):

    def __init__(self,
                 username="guest",
                 password="guest",
                 host="127.0.0.1",
                 port=5672,
                 ack=False,
                 persist=True,
                 ):
        self._port = port or 5672  # 端口
        self._host = host or "127.0.0.1"  # 主机
        self._username = username or "guest"  # 用户名
        self._password = password or "guest"  # 密码
        self._persist = persist
        self._prefetch_count = 1
        self._connection = None
        self._channel = None
        self._ack = ack
        self._delivery_mode = self._get_delivery_mode()
        self.properties = pika.BasicProperties(
            delivery_mode=self._delivery_mode
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def set_username(self, username):
        self._username = username

    def set_password(self, passwd):
        self._password = passwd

    def set_host(self, host):
        self._host = host

    def set_port(self, port):
        self._port = port

    def set_prefetch_count(self, prefetch_count):
        self._prefetch_count = prefetch_count

    def connection_by_url(self, url):
        """
        通过url链接
        :param url:
        :return:
        """
        parameters = pika.connection.URLParameters(url)
        try:
            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()
            self._connection, self._channel = connection, channel
        except Exception as e:
            logger.exception(e)
            raise e

    def _get_delivery_mode(self):
        # delivery_mode为2时表示消息持久化, 其他值时非持久化
        delivery_mode = (2 if self._persist else 0)
        return delivery_mode

    def connect(self):
        """
        根据账号密码等信息创建一个链接
        :return:
        """
        if self._channel and self._connection:
            return
        # 设置账号密码
        if self._username and self._password:
            credentials = pika.PlainCredentials(username=self._username,
                                                password=self._password)
        else:
            credentials = None

        # 创
        parameters = pika.ConnectionParameters(
            host=self._host, port=self._port, credentials=credentials
        ) if credentials else pika.ConnectionParameters(host=self._host,
                                                        port=self._port)
        try:
            # 创建阻塞连接
            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()

            self._connection, self._channel = connection, channel

        except Exception as e:
            logger.exception(e)
            raise e

    def create_exchange(self, exchange_name, exchange_type="", **kwargs):
        """
        注册一个交换机
        Args:
            exchange_name: 交换机名称
            exchange_type: 交换机类型

        Returns:

        """
        self._channel.exchange_declare(exchange=exchange_name,
                                       exchange_type=exchange_type, **kwargs)

    def create_queue(self, queue, **kwargs):
        # if "durable" not in kwargs:
        #     kwargs.update({"durable": True})
        if queue:
            self._channel.queue_declare(queue=queue, **kwargs)
        else:
            queue = self._channel.queue_declare(queue='', **kwargs).method.queue
        return queue
        # self.callback_queue = result.method.queue

    def close(self):
        self._connection.close()
        """ 关闭信道并断开连接 """

        if self._connection and self._connection.is_open:  # 检测连接是否还存活
            self._connection.close()  # 断开连接

        if self._channel and self._channel.is_open:  # 检测信道是否还存活
            self._channel.close()  # 关闭信道


class RabbitPublisher(RabbitBase):
    """"""

    # def __init__(self,
    #              username="guest",
    #              password="guest",
    #              host="127.0.0.1",
    #              port=5672,
    #              ack=False,
    #              persist=True, ):
    #     super().__init__(username, password, host, port, ack, persist)
    #     self.rpc_server_response = None

    def push(self, queue_name='', message='', exchange="", exchange_type="", routing_key=""):
        assert self._connection and self._channel, "no connection"
        assert isinstance(routing_key, list) or isinstance(routing_key, str), 'routing_key type error'

        # 开启消息送达确认(注意这里是送达消息队列即可)
        self._channel.confirm_delivery()
        # self._channel.syncronize()

        if exchange and exchange_type:
            self.create_exchange(exchange, exchange_type, durable=self._persist)
        else:
            self._channel.queue_declare(queue=queue_name, durable=self._persist)
            routing_key = queue_name

        if isinstance(routing_key, str):
            routing_key = [routing_key]

        [self._channel.basic_publish(exchange=exchange,
                                     routing_key=key,
                                     body=message,
                                     properties=self.properties)
         for key in routing_key]


class RabbitConsumer(RabbitBase):
    """"""

    def queue_bind(self, exchange="", exchange_type="", queue_name="", routing_key=""):
        assert isinstance(routing_key, list) or isinstance(routing_key, str), 'routing_key type error'
        self.create_exchange(exchange_name=exchange, exchange_type=exchange_type, durable=self._persist)
        self.create_queue(queue_name, durable=self._persist)
        if isinstance(routing_key, str):
            routing_key = [routing_key]
        [self._channel.queue_bind(queue=queue_name, exchange=exchange, routing_key=key) for key in routing_key]

    def get(self, exchange="", exchange_type="", queue_name='', prefetch_count=1, routing_key="", func=None):
        if not func:
            func = self.callback
        if prefetch_count:
            self._channel.basic_qos(prefetch_count=self._prefetch_count)
        if queue_name:
            self.create_queue(queue_name, durable=self._persist)
        if exchange and exchange_type:
            self.queue_bind(exchange, exchange_type, queue_name, routing_key)

        # 获取任务
        self._channel.basic_consume(queue_name,
                                    func,
                                    auto_ack=self._ack)
        # 等待执行
        self._channel.start_consuming()

    def callback(self, channel, method, properties, body):
        logger.info(f"start compare the message : {body.decode()}")

        # 回调函数中手动消息确认
        channel.basic_ack(delivery_tag=method.delivery_tag)


class RpcRabbitConsumer(RabbitConsumer):

    @staticmethod
    def _get_uuid():
        return str(uuid.uuid4())

    def on_request(self, ch, method, props, body):
        logger.info(f"start deal: {body}")
        body = json.loads(body.decode())
        task = body.get("task", "default")
        if task == "uuid":
            response = self._get_uuid()
            time.sleep(3)
        else:
            response = "没有处理，默认返回"

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


class RpcRabbitPublisher(RabbitPublisher):
    def __init__(self,
                 username="guest",
                 password="guest",
                 host="127.0.0.1",
                 port=5672,
                 ack=False,
                 persist=True, ):
        super().__init__(username, password, host, port, ack, persist)
        self.result = None

    def rpc_server(self, message='', queue_name="rpc_queue"):
        def check(ch, method, props, body):
            if correlation_id == props.correlation_id:
                logger.info(f"调用成功！ {body.decode()}")
                self.result = body.decode()
                # ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_publish(exchange='',
                                 routing_key=props.reply_to,
                                 properties=pika.BasicProperties(correlation_id=props.correlation_id),
                                 body=body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # 声明一个rpc任务的队列，不存在时创建
        self.create_queue(queue=queue_name, durable=self._persist)

        # 声明一个独占的队列，用于当前任务结果获取
        reply_to = self.create_queue(queue="", exclusive=True, durable=self._persist)

        # 生成任务ID
        correlation_id = str(uuid.uuid4())

        # 推送消息任务
        self._channel.basic_publish(exchange='',
                                    routing_key=queue_name,
                                    body=message,
                                    properties=pika.BasicProperties(
                                        reply_to=reply_to,
                                        correlation_id=correlation_id,
                                    ))

        # 限制单个消费者处理任务数
        self._channel.basic_qos(prefetch_count=self._prefetch_count)
        # 在rpc_queue中接收消息，调用on_queue
        self._channel.basic_consume(queue=reply_to, on_message_callback=check)

        logger.info(f"等待接收RPC消息。。。")
        # self._channel.start_consuming()
        # 没有数据就循环收
        while self.result is None:
            # 非阻塞版的start_consuming()
            self._connection.process_data_events()
            time.sleep(0.5)
        return self.result
