#!coding=utf-8
from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
import subprocess
import sys


try:
    sys.argv[1]
except:
    sys.exit("Given a bjobs ID\n Usage:\n python {} bjobs_ID".format(sys.argv[0]))



class pid_stats(object):
    def __init__(self,pid):
        self.pid=pid
    def get_pid_cmd(self):
        pid=self.pid
        cmd='bjobs -w {}'.format(pid)
        a=subprocess.check_output(cmd,shell=True)
        if len(a)<1:
            raise ValueError('No such Pid')
        else:
            a=a.split('\n')[1]
            a=filter(lambda x:x!='',a.split())
            cmd=' '.join(a[5:-3])
        return cmd
    def get_pid_stats(self):
        pid=str(self.pid)
        cmd='bjobs'
        a=subprocess.check_output(cmd)
        a=a.decode()
   # _=lambda x:len(x)>1
    #print(a)
        a=filter(lambda x:len(x)>1,a.split('\n')[1:])
        lst=[str(i.split()[0]) for i in a]
        if pid in lst:
            return 0
        else:
            return 1
    #print(lst)

  #  for i in a:
  #      lne=i.split()
  #      print(lne[0])


name=subprocess.check_output('whoami')
name=name.strip('\n')


def main():
    stats=0
    p=pid_stats(sys.argv[1])
    while stats==0:
        stats=p.get_pid_stats()
    #    print(stats)
    #print(stats)
    if stats ==1:
        p_cmd=p.get_pid_cmd()
    # 请自行修改下面的邮件发送者和接收者
        sender = '2890481517@qq.com'  #发送者的邮箱地址
        receivers = ['2019204004@njau.edu.cn']  #接收者的邮箱地址
        message = MIMEText('Job {}\n{}\n was done'.format(sys.argv[1],p_cmd), _subtype='plain', _charset='utf-8')
        message['From'] = Header('{}'.format(name), 'utf-8')  #邮件的发送者
        message['To'] = Header('Qionghou', 'utf-8')   #邮件的接收者
        message['Subject'] = Header('job {} finished'.format(sys.argv[1]), 'utf-8') #邮件的标题
        smtper = SMTP('smtp.qq.com')
    # 请自行修改下面的登录口令
        smtper.login(sender, 'sfqvzfmguznidfga')  #QQ邮箱smtp的授权码
        smtper.sendmail(sender, receivers, message.as_string())
        print('邮件发送完成!')


if __name__ == '__main__':
    main()
