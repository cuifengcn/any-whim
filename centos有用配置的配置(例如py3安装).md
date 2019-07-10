配置好Python3.6和pip3
安装EPEL和IUS软件源

```bash
# 这里是多行处理(不覆盖原来python2的python和pip名字，以python3,pip3使用python3)
# 安装 python36u-devel 是为了处理某些安装异常，例如 twisted。
yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python36u -y
yum install python36u-pip -y
yum install gcc -y
yum install python36u-devel -y
ln -s /bin/python3.6 /bin/python3
ln -s /bin/pip3.6 /bin/pip3

# 用python3覆盖原python和pip名字（强烈不建议覆盖，因为yum工具使用的是py2，所以修改后会导致yum使用异常）
# rm -f /bin/python ; rm -f /bin/pip ; ln -s /bin/python3 /bin/python; ln -s /bin/pip3 /bin/pip

# 关于ss
# pip install shadowsocks ; pip3 install shadowsocks ; systemctl stop firewalld.service ; systemctl disable firewalld.service
# ssserver -p 6666 -k vilame -d start

# 关于连接ss端口进行下载
# sslocal -s xxx.xxx.xxx.xxx -p 6666 -b 127.0.0.1 -l 1080 -k vilame -d start
# you-get -s 127.0.0.1:1080 --skip-existing-file-size-check url1,url2,url3...
# youtube-dl --proxy socks5://127.0.0.1:1080/ url1,url2,url3...
```

安装ffmpeg

```bash
# centos7
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
sudo yum install ffmpeg ffmpeg-devel -y

# centos6
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el6/x86_64/nux-dextop-release-0-2.el6.nux.noarch.rpm
sudo yum install ffmpeg ffmpeg-devel -y
```
