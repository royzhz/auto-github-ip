import requests
import time
import ctypes, os,sys
import subprocess
url="https://api.github.com/meta"
host="C:\Windows\System32\drivers\etc\hosts"

def get_ip_data():
    page=requests.get(url)
    if page.status_code != 200:
        print("找不到ip地址")
    return page.text

def is_ip_address(ip):
    content=ip.split('.')
    for i in content:
        if i.isnumeric()==False:
            return False
    return True

def handle_ip(ip):
    num=ip.find('/')
    if(num!=-1):
        return ip[:num]
    elif(ip.isalpha()==True):
        return ip

def check_ip_available(ip):
    cmd = "ping -n 4 -w 1 "+ip

    exit_code = subprocess.getstatusoutput(cmd)
    if exit_code[0]==1:
        print("网络不通:"+ip)
        return False
    else:
        return True

def get_ip_address(text):
    fhost=open(host,"r",encoding='UTF-8')
    host_content=fhost.read()
    fhost.close()

    host_check=host_content.split('\n')
    host_clean=[]
    for i in host_check:
        if i=="" or i.lstrip()[0]=='#'or i.find("github")==-1:
            host_clean.append(i)

    black_ip=open("blackip.txt")

    black=black_ip.read().split()

    all_ip=text.split('\"')
    ip_list=[]

    for i in all_ip:
        t=handle_ip(i)
        if(t is not None and len(t)<20):
            ip_list.append(t)

    web_name=""
    web_end="github.com"
    has_done=0
    host_ip_has_found=""
    for i in ip_list:
        if(i.isalpha()==True):
            has_done=0
            if(i=="web"):
                web_name=""+web_end
            elif(i=="actions"):
                return
            else:
                web_name=i+'.'+web_end
        elif(has_done==1):
            continue
        elif(i in black):
            print("ip"+i+"正在黑名单中！")
        elif(check_ip_available(i)==True):
            has_done=1
            print(i+" "+web_name+'\n'+"成功找到ip地址！")
            host_ip_has_found+=i+" "+web_name+'\n'

        fhost = open(host, "w", encoding='UTF-8')
        for i in host_clean:
            # print(i)
            fhost.write(i + '\n')

        fhost.write(host_ip_has_found)
    return

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False




ip=get_ip_data()
print("已经获得ip地址，正在检查")
if is_admin():
    get_ip_address(ip)
    os.system("ipconfig /flushdns")
    print("host修改已经完成，若打不开请把ip加入黑名单再运行本程序")
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)



