#!coding=utf-8
from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
import subprocess
import sys
import optparse

try:
    sys.argv[1]
except:
    sys.exit("Given a bjobs ID\n Usage:\n python {} bjobs_ID".format(sys.argv[0]))


def get_opt(self):
    parser = optparse.OptionParser(
        usage="%prog [options] jobsID")
    parser.add_option("-s", "--send", dest="send", help="Input mapping file", default='2890481517@qq.com')
    parser.add_option("-r", "--recive", dest="recive", help="Contig fasta file", default='2019204004@njau.edu.cn')
    parser.add_option("-m", "--stmp", dest="stmp", help="stmp code for e-mail", default='sfqvzfmguznidfga')
    parser.add_option("-t", "--system", dest="sys", help="giving job submit system LSF/Local",
                      default='LSF')
    (options, args) = parser.parse_args()
    if not (options.sys):
        sys.exit(parser.print_help())
    return options, args


class local_stats(object):
    def __init__(self, pid):
        self.pid = pid
        name = subprocess.check_output('whoami')
        name = name.strip('\n')
        self.name = name

    def get_pid_state(self):
        pid = self.pid
        name = self.name
        cmd = 'top -c -n 1 -b -u {}'.format(name)
        a = subprocess.check_output(cmd, shell=True)
        a = a.decode()
        a = a.split('\n')[7:]
        a = list(filter(lambda x: x != '', a))
        _ = lambda x: x.split(' ')[0]
        allpid = list(map(_, a))
        self.cmd = a
        if pid in allpid:
            return 0
        else:
            return 1

    def get_local_cmd(self):
        pid = self.pid
        cmd = self.cmd
        cmd_dct = {i.strip().split()[0]: ' '.join(i.strip().split()[11:]) for i in cmd}
        return cmd_dct[pid]


class pid_stats(object):
    def __init__(self, pid):
        self.pid = pid

    def get_pid_cmd(self):
        pid = self.pid
        cmd = 'bjobs -w {}'.format(pid)
        a = subprocess.check_output(cmd, shell=True)
        if len(a) < 1:
            raise ValueError('No such Pid')
        else:
            a = a.split('\n')[1]
            a = list(filter(lambda x: x != '', a.split()))
            cmd = ' '.join(a[5:-3])
        return cmd

    def get_pid_stats(self):
        pid = str(self.pid)
        cmd = 'bjobs'
        a = subprocess.check_output(cmd)
        a = a.decode()
        # _=lambda x:len(x)>1
        # print(a)
        a = filter(lambda x: len(x) > 1, a.split('\n')[1:])
        lst = [str(i.split()[0]) for i in a]
        if pid in lst:
            return 0
        else:
            return 1
    # print(lst)


#  for i in a:
#      lne=i.split()
#      print(lne[0])


name = subprocess.check_output('whoami')
name = name.strip('\n')


def main():
    stats = 0
    options, args = get_opt()
    sender = options.send
    recive = options.recive
    stmp = options.stmp
    system = options.system

    for jobs in args:
        if system=='LSF':
            p = pid_stats(jobs)
            while stats == 0:
                stats = p.get_pid_stats()
            if stats == 1:
                p_cmd = p.get_pid_cmd()
            # 请自行修改下面的邮件发送者和接收者
        elif system=='local':
            p = local_stats(jobs)
            while stats == 0:
                stats = p.get_pid_state()
            if stats == 1:
                p_cmd = p.get_local_cmd()
        sender = options.send #'2890481517@qq.com'  # 发送者的邮箱地址
        receivers =[str(options.recive)] #['2019204004@njau.edu.cn']  # 接收者的邮箱地址
        message = MIMEText('Job {}\n{}\n was done'.format(sys.argv[1], p_cmd), _subtype='plain', _charset='utf-8')
        message['From'] = Header('{}'.format(name), 'utf-8')  # 邮件的发送者
        message['To'] = Header('Qionghou', 'utf-8')  # 邮件的接收者
        message['Subject'] = Header('job {} finished'.format(sys.argv[1]), 'utf-8')  # 邮件的标题
        smtper = SMTP('smtp.qq.com')
            # 请自行修改下面的登录口令
        smtper.login(sender, 'sfqvzfmguznidfga')  # QQ邮箱smtp的授权码
        smtper.sendmail(sender, receivers, message.as_string())
        print('邮件发送完成!')


if __name__ == '__main__':
    main()
