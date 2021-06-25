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
from yamlprofiles import YAML, get_yaml_config, get_nested_dict_value

cur_dir = os.path.abspath(os.path.dirname(__file__))
yaml_file = os.path.join(cur_dir, 'app.yml')

if __name__ == '__main__':
    # YAML object can be reused
    # Specify profile
    yaml = YAML(yaml_file)
    config = yaml.get_profile('prod')
    print(config.get('mysql'))
    config = yaml.get_profile('dev')
    print(config['mysql'])

    # When the profile parameter is not specified, it is read from the command line parameter `-- profile`, if it is not specified, the `app.profile.active` field in the configuration file is read
    print('--- cmd argument or app.profile.active---')
    config = yaml.get_profile()
    print(config)

    # Convenience function `get_yaml_config(yaml_file, profile=None)`
    config = get_yaml_config(yaml_file)
    print(config.get('mysql'))
    print(config['app']['server']['port'])
    print(get_nested_dict_value(config,'app.server.port'))
    
    # Multi-level key direct reading
    print(config['app.server.port'])
    # read list
    print(config['urls'])
    # read list index
    print(config['urls.[1]'])
```
