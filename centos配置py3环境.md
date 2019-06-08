配置好Python3.6和pip3
安装EPEL和IUS软件源

```bash
yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python36u -y
ln -s /bin/python3.6 /bin/python3
yum install python36u-pip -y
ln -s /bin/pip3.6 /bin/pip3
pip3 install shadowsocks
ssserver -p 6666 -k vilame -d start
systemctl stop firewalld.service
systemctl disable firewalld.service
```
