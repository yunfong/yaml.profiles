# This is a sample Python script.

import os
from yamlprofiles import YAML, get_yaml_config, get_nested_dict_value

cur_dir = os.path.abspath(os.path.dirname(__file__))
yaml_file = os.path.join(cur_dir, 'app.yml')

if __name__ == '__main__':
    # 指定profile
    print('--- prod ---')
    # YAML对象可以反复使用
    yaml = YAML(yaml_file)
    config = yaml.get_profile('prod')
    print(config)
    print(config.get('mysql'))

    print('--- dev ---')
    config = yaml.get_profile('dev')
    print(config['mysql'])
    print('key[1] : %s' % config['mysql.1'])  # 字段名为正数数1
    print("key['2'] : %s" % config["mysql.2"])  # 字段名为加了引号的数字'2'

    # 未指定profile参数时，会从命令行参数读取--profile，如果没有这个参数，则会读取配置文件中的app.profile.active字段
    print('--- cmd argument or app.profile.active---')
    config = yaml.get_profile()
    print(config)

    # 一次性获取
    print('--- function ---')
    config = get_yaml_config(yaml_file)
    # config = get_yaml_config(yaml_file,'prod')
    print(config.get('mysql'))
    print(config['app']['server']['port'])
    print(get_nested_dict_value(config, 'app.server.port'))
    print('多级key直接访问：app.server.port: %d' % config['app.server.port'])
    print(config.get('app.server.port'))
    # 取数组list
    print(config['urls'])
    # 取数组对象的某个下标
    print(config['urls.[0]'])
