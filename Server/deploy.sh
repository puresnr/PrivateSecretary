#!/bin/bash

# 用于把windows格式的文件转换为linux格式的文件
yum install dos2unix

# 安装python3,并把python3设置为默认python
# 注意：python36是安装时选择的python版本，也可以是其它版本
yum install python36
mv /usr/bin/python /usr/bin/python27
mv /usr/bin/python36 /usr/bin/python

# 升级python3后，修复不能再使用yum的问题
# 原因是：yum使用了Python, 由于python2和3版本差异较大，导致yum执行时报异常
# 修复的方法是修改yum的python执行环境，显示的使用python2环境执行yum
# 注意:python27是上一步备份的旧版本python可执行文件的备份名称
cd /usr/bin
for file in `ls yum*`
do
    cp $file ${file}_backup
    sed -i 's/#!\/usr\/bin\/python/#!\/usr\/bin\/python27/g' $file
done
sed -i 's/#! \/usr\/bin\/python/#! \/usr\/bin\/python27/g' /usr/libexec/urlgrabber-ext-down

# 安装python3相关工具
# 注意: 安装与python3版本相同的setuptools
yum -y install python36-setuptools
easy_install-3.6 pip

# 安装python脚本需要使用的环境
pip install beautifulsoup4