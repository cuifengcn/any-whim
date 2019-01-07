配置好Python3.6和pip3
安装EPEL和IUS软件源

yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
安装Python3.6

yum install python36u -y
创建python3连接符

ln -s /bin/python3.6 /bin/python3
安装pip3

yum install python36u-pip -y
