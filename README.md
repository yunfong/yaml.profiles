# YAML Profiles Parser

- YAML syntax support
- Support multi profile configuration

#### Installation
```
pip install yaml.profiles
```

#### Examples

- yaml configuration file: app.yml

```yaml
# global
app:
  name: spark-kyc
  server:
    port: 8082
  profile:
    active: prod
urls:
  - baidu.com
  - aliyun.com
  - tencent.com

# the profile
---
$profile: dev 
mysql:
  host: localhost
  user: root
  password: xxxx
  db: testing

# the other profile
---
$profile: prod
mysql:
  host: localhost
  user: root
  password: xxxx
  db: prod-db
# The same key in profile will be overwrite global key
app:
  server:
    port: 80
```

This yaml configuration file contains two profile: prod, dev。
1. Use`---` single line split profiles
2. Use `$profile` for each profile segment
3. Determine activation priority：
    - Pass the profile parameter when calling the function
    - Command line argument `--profile=xxx`
    - Check the key `app.profiles.active` in the configuration file

- example.py :

```python

import os
from yaml.profiles import YAML, get_yaml_config, get_nested_dict_value

cur_dir = os.path.abspath(os.path.dirname(__file__))
yaml_file = os.path.join(cur_dir, 'app.yml')

if __name__ == '__main__':
    # YAML对象可以重复使用
    # 指定profile
    yaml = YAML(yaml_file)
    config = yaml.get_profile('prod')
    print(config.get('mysql'))
    config = yaml.get_profile('dev')
    print(config['mysql'])

    # 未指定profile参数时，会从命令行参数读取--profile，如果没有这个参数，则会读取配置文件中的app.profile.active字段
    print('--- cmd argument or app.profile.active---')
    config = yaml.get_profile()
    print(config)

    # 便利性函数 get_yaml_config(yaml_file, profile=None)
    config = get_yaml_config(yaml_file)
    print(config.get('mysql'))
    print(config['app']['server']['port'])
    print(get_nested_dict_value(config,'app.server.port'))
    
    #多级key直接读取
    print(config['app.server.port'])
    # 取list
    print(config['urls'])
    # 取list对象的某个下标
    print(config['urls.[1]'])
```


