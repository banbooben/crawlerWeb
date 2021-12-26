
# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from application.config.server_conf import current_config

# 创建对象的基类:
BaseModel = declarative_base()

try:
    # 初始化数据库连接:# 初始化数据库连接
    # ## echo默认为False，当为True的时候，会把sqlalchemy的所有日志包括连接数据库后做的所有操作都会打印出来，对于调试来说是非常方便的
    # ## pool_size是连接池中连接的数量
    # ## max_overflow指允许的最大连接池大小，当超过pool_size后如果仍需要连接仍然可以创建新的连接，而当超过max_overflow后则不会创建新的连接，必须等到之前的连接完成以后，默认为10，为0表示不限制
    # ## pool_recycle表示连接在给定时间之后会被回收，不能超过8小时
    # ## pool_timeout表示等待多少秒后，如果仍然没有获取到连接则放弃获取
    # ## pool_pre_ping表示每次取出一个连接时，会发送一个select 1来检查连接是否有效
    # engine = create_engine('mysql+pymysql://' + current_config.DATABASES_INFO)
    # engine = create_engine(current_config.SQLALCHEMY_DATABASE_URI,
    #                        echo=current_config.SQLALCHEMY_ECHO,
    #                        pool_size=current_config.SQLALCHEMY_POOL_SIZE,
    #                        pool_recycle=current_config.SQLALCHEMY_POOL_RECYCLE,
    #                        max_overflow=current_config.SQLALCHEMY_POOL_MAX_OVERFLOW,
    #                        pool_timeout=current_config.SQLALCHEMY_POOL_TIMEOUT,
    #                        pool_pre_ping=current_config.SQLALCHEMY_POOL_PRE_PING
    #                        )
    engine = create_engine(current_config.SQLALCHEMY_DATABASE_URI)

    # 创建DBSession类型:
    Session = sessionmaker(bind=engine, autocommit=current_config.SQLALCHEMY_COMMIT_ON_TEARDOWN)
    session = Session(bind=engine)
except Exception as e:
    raise e

