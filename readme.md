## 环境配置
 + Python versions >=3.8
 + pip install d3graph
 + download get_tb_lineage.py

## 说明
 + 每个文件sink表只有一个，如果存在多个解析时只会保留第一个
 + 目标表识别使用insert 语句作为标识
 + 解析字段依赖可以使用该包 https://github.com/reata/sqllineage

## 使用
 + python get_tb_lineage.py file_name/file_directory
 + python get_tb_lineage.py file_name/file_directory filter_table_name
 + example python3.10 ./get_tb_lineage.py ./example.conf