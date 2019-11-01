import configparser
import os

conf= configparser.ConfigParser()
def readConf(name='default'):
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf.read(root_path + '/'+ name +'.conf')  # 文件路径
    return conf