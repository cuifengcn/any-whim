import os,re

if not os.path.isdir('new'):
    os.makedirs('new')

def gethtmldirs():
    return filter(lambda i:i.endswith('.html')or
                         i.endswith('.htm'),
                  os.listdir('.'))

def addstatic(htmlname):
    with open(htmlname) as f:
        s = f.read()
        s = re.sub(r'((src|href)=)("[^"]+?\.(css|js|png|jpg|gif)")','\g<1> "{% static \g<3> %}"',s)
        with open('new/'+htmlname,'w') as t:
            t.write(s)

if __name__ == '__main__':
    for htmlname in gethtmldirs():
        addstatic(htmlname)
