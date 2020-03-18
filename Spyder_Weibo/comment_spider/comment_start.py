import sys
sys.path.append("..")
import requests
import time
import random
from bs4 import BeautifulSoup
from tools import Cookie_Process
from tools.Emoji_Process import filter_emoji
from tools.Mysql_Process import mysqlHelper
from tools.Date_Process import time_process
from tools.Mysql_Process import get_db

url_comment = 'https://weibo.cn/comment/{}?&page={}'
'''爬取某个微博的的评论信息'''

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list
def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def fetch_comment_data(wbid,userid):
    cookie = Cookie_Process.read_cookie()   # 获取文件中存储的cookie
    cookies = {
        "Cookie": cookie}
    proxies = get_random_ip(ip_list)
    r_comment = requests.get('https://weibo.cn/comment/{}'.format(wbid), cookies=cookies,proxies=proxies)
    soup_comment = BeautifulSoup(r_comment.text, 'lxml')
    flag = False
    try:
        flag = soup_comment.select('.c')[-1].text.startswith('还没有人针对')
    except Exception as e:
        page_num = 1

    if flag:
        print("--------- 此微博没有人评论！ ---------\n")
        return
    else:
        try:
            page_num = int(soup_comment.select_one(".pa").text.split()[-1].split("/")[-1].split("页")[0])
        except Exception as e:
            page_num = 1


    mh = mysqlHelper(get_db()[0], get_db()[1], get_db()[2], get_db()[3], get_db()[4], int(get_db()[5]))
    sql = "insert into comment(wb_id,comment_content,comment_userid,comment_username,comment_like,comment_createtime,userid) values(%s,%s,%s,%s,%s,%s,%s)"

    page_id = 1
    commentinfos = []
    print("--------- 此微博 {} 的评论页数共有 {} 页 ---------\n".format(wbid,page_num))
    while page_id < page_num + 1:

        time.sleep(random.uniform(4.5,6.5))  #设置睡眠时间

        print("++++++ 正在爬取此微博 {} 的第 {} 页评论...... ++++++\n".format(wbid,page_id))
        r_comment = requests.get(url_comment.format(wbid, page_id), cookies=cookies)
        soup_comment = BeautifulSoup(r_comment.text, 'lxml')
        comment_list = soup_comment.select(".c")

        for l in comment_list:
            if str(l.get("id")).startswith("C_"):
                comment_content = filter_emoji(l.select_one(".ctt").text)
                comment_userid = l.select_one("a").get("href")[3:]
                comment_username = l.select_one("a").text
                comment_like = l.select_one(".cc").text.strip()[2:-1]
                comment_createtime = time_process(l.select_one(".ct").text.strip()[:-5])
                print("评论内容  ：" + comment_content)
                print("评论用户ID：" + comment_userid)
                print("评论用户名：" + comment_username)
                print("评论赞数  ：" + comment_like)
                print("评论时间  ：" + comment_createtime)
                print('----------------------------\n')
                commentinfo = {'wb_id': wbid,  # 生成一条评论信息的列表
                        'comment_content': comment_content,
                        'comment_userid': comment_userid,
                        'comment_username': comment_username,
                        'comment_like': comment_like,
                        'comment_createtime': comment_createtime,
                        'userid': userid
                        }
                commentinfos.append(commentinfo)

        page_id = page_id + 1

        if(len(commentinfos) >= 100):
            mh.open();
            for i in range(len(commentinfos)):
                mh.cud(sql,
                       (commentinfos[i]['wb_id'], commentinfos[i]['comment_content'], commentinfos[i]['comment_userid'],
                        commentinfos[i]['comment_username'], commentinfos[i]['comment_like'],
                        commentinfos[i]['comment_createtime'], userid))
            mh.tijiao();
            mh.close()
            commentinfos = []

    if(len(commentinfos) > 0):
        mh.open();
        for i in range(len(commentinfos)):
            mh.cud(sql,
                   (commentinfos[i]['wb_id'], commentinfos[i]['comment_content'], commentinfos[i]['comment_userid'],
                    commentinfos[i]['comment_username'], commentinfos[i]['comment_like'],
                    commentinfos[i]['comment_createtime'], userid))
        mh.tijiao();
        mh.close()

    print("--------- 此微博的全部评论爬取完毕！---------\n\n")


'''获取所有涉及关键字的微博用户，并进行每个用户的基本信息爬取'''
'''
def search_all_comment(keyword):
    cookie = Cookie_Process.read_cookie()   # 获取文件中存储的cookie
    mhf = mysqlHelper(get_db()[0], get_db()[1], get_db()[2], get_db()[3], get_db()[4], int(get_db()[5]))
    sqlf = "select wb_id from keyword_weibo where keyword = %s "
    all_wbid_temp = mhf.findAll(sqlf, keyword)   #查询涉及到关键字的所有的微博id
    all_wbid = []                   # 对要爬取的微博id列表进行去重
    for i in all_wbid_temp:
        wbid = i[0]
        # print(wbid)
        if wbid not in all_wbid:
            all_wbid.append(wbid)
    wb_num = len(all_wbid)
    print('查询到涉及关键字为 {} 的微博总数量为 {}\n'.format(keyword,str(wb_num)))


    for i in range(len(all_wbid)):
        print("============ 正在爬取第 {} 条微博的评论 ===========".format(int(i)+1))
        fetch_comment_data(str(all_wbid[i]),keyword,cookie)
'''


def search_all_comment_id(userid):
    mhf = mysqlHelper(get_db()[0], get_db()[1], get_db()[2], get_db()[3], get_db()[4], int(get_db()[5]))
    sqlf = "select wb_id from user_weibo where wb_userid =%s"
    all_wbid_temp = mhf.findAll(sqlf, userid)   #查询涉及到关键字的所有的微博id
    all_wbid = []                   # 对要爬取的微博id列表进行去重
    for i in all_wbid_temp:
        wbid = i[0]
        # print(wbid)
        if wbid not in all_wbid:
            all_wbid.append(wbid)
    wb_num = len(all_wbid)
    print("这个家伙有{}条微博已经被爬下来了\n".format(str(wb_num)))
    for i in range(len(all_wbid)):
        print("============ 正在爬取第 {} 条微博的评论 ===========".format(int(i)+1))
        fetch_comment_data(str(all_wbid[i]),userid)

if __name__ == '__main__':
    cookie = Cookie_Process.write_cookie() # 获取文件中存储的cookie
    url = 'http://www.xicidaili.com/nn/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
    ip_list = get_ip_list(url, headers=headers)
    proxies3 = get_random_ip(ip_list)
    print(proxies3)
    proxies4 = get_random_ip(ip_list)
    print(proxies4)    
    time_start = time.time()
    search_all_comment_id(input("请输入要爬评论的博主："))
    time_end = time.time()

    print('本次操作数据全部爬取成功，爬取用时秒数:', (time_end - time_start))

    # fetch_comment_data('H7ZDJzGRe','陈奕迅',cookie)





