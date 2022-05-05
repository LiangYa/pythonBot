
import logging
import os
import time


def reload_log():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # 日志格式化输出
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
    filepath = os.path.join(os.path.dirname(__file__), "../logs")
    filepath = filepath + "/a.log"
    fp = logging.FileHandler(filepath, encoding='utf-8')
    fs = logging.StreamHandler()
    # 调用
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])
    return logging


Logger = reload_log()


def get_log(logger_name, log_path, log_level):
    """
    # 获取日志对象
    :param logger_name: 日志名称
    :param log_path: 日志目录
    :param log_level: 日志级别
    :return:
    """
    # 创建一个logger
    assert logger_name is not None and isinstance(logger_name, str)
    if os.path.exists(log_path) is False:
        os.makedirs(log_path)
    assert log_level != "" and log_level is not None
    assert log_path != "" and log_path is not None
    log_dict = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG, 'ERROR': logging.ERROR, 'WARN': logging.WARN}
    assert log_dict.get(log_level) is not None
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_dict.get(log_level))

    # 设置日志存放路径，日志文件名
    # 获取本地时间，转换为设置格式
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # 通过字符串拼接设置日志文件名
    all_log_name = log_path + str(logger_name) + "_" + rq + ".log"
    err_log_name = log_path + str(logger_name) + "_" + rq + "_error.log"

    # 写入文件，如果文件超过100M，仅保留5个文件
    fh = logging.handlers.RotatingFileHandler(all_log_name, maxBytes=1024*1024*100, backupCount=5)
    fh.setLevel(log_dict.get(log_level))
    # 创建一个handler写入错误日志
    eh = logging.handlers.RotatingFileHandler(err_log_name, maxBytes=1024*1024*100, backupCount=5)
    eh.setLevel(log_dict.get(log_level))
    # 创建一个handler输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(log_dict.get(log_level))

    # 定义日志输出格式
    # 以时间-日志器名称-日志级别-日志内容的形式展示
    all_log_formatter = logging.Formatter("%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s \
              %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

    # 以时间-日志器名称-日志级别-文件名-函数行号-错误内容定义错误日志
    error_log_formatter = logging.Formatter("%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s \
              %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

    # 将定义好的输出形式添加到handler
    fh.setFormatter(all_log_formatter)
    ch.setFormatter(all_log_formatter)
    eh.setFormatter(error_log_formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    logger = reload_log()
    logger.info("1234567")
    # logging = get_log("anem", 'INFO', )
    # logging.debug("This is a debug log.哈哈")
    # logging.info("This is a info log.")
    # logging.warning("This is a warning log.")
    # logging.error("This is a error log.")
    # logging.critical("This is a critical log.")
