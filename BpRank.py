#-*- coding: UTF-8 -*-   
import sys


import redis
import urllib2
import re
import json

r = redis.Redis(host='127.0.0.1', port=6379)

def getUserList(page=168): 
    try:
        res = urllib2.urlopen('https://osu.ppy.sh/p/pp/?c=CN&m=0&s=3&o=1&f=&page='+str(page),timeout=3)
        print 'getting page:'+str(page)
        html = res.read()
        pattern = re.compile("<tr class='' onclick='document.location="+r'"/u/(\d*)"'+"'>")
        result = pattern.findall(html)
    except:
        print 'error page:'+str(page)
        result=[]
    
    return result

def getBp(uid=2646251):
    try:
        
        res = urllib2.urlopen('https://osu.ppy.sh/api/get_user_best?k=b68fc239f6b8bdcbb766320bf4579696c270b349&u='+str(uid)+'&limit=10',timeout=2)
        print 'getting user:'+str(uid)
        html = res.read()
        result = json.loads(html)
        
        
    except:
        print 'error user:'+str(uid)
        result=[]

    return result


def getBpList(startpage=31,endpage=32):
    r.delete('BpRank')
    num = endpage - startpage
    for p in range(num):
        u_list = getUserList(p+startpage)
        while not u_list:
            u_list = getUserList(p+startpage)

        #print u_list
        if u_list:
            for uid in u_list:
                BpList = getBp(uid)
                while not BpList:
                    BpList = getBp(uid)
                #print BpList
                if BpList:
                    for bp in BpList:
                        bp_id = bp.get('beatmap_id')
                        if r.zadd('BpRank',bp_id=1):
                            pass
                        else:
                            r.zincrby('BpRank',bp_id,1)

    

def write(ppinfo,f='BpRank.txt'):
    l = r.zrange('BpRank',0,9,True,True) #l 结果元组列表

    print "creating log .."
    with open(f,'a') as f:
        f.write('***********BP热度统计结果***********\n\n')
        f.write('统计范围:'+ppinfo+'\n\n')
        for index,i in enumerate(l):#i[0]:beatmap_id,i[1]:次数
            beatmap = getBeatMap(i[0])
            while not beatmap:
                beatmap = getBeatMap(i[0])

            title = beatmap[0].get('title')
            print title
            star = beatmap[0].get('difficultyrating')
            
            star = round(float(star),1)#小数点精度
            line = str(index+1)+'.https://osu.ppy.sh/b/'+str(i[0])+ '   热度:'+str(i[1])+'次     星数:'+str(star)+'\n曲名:'+str(title)+'\n\n'
            f.write(line)

        f.write('\n***********BP热度统计结果***********\n\n\n')
    print "finish!"

def getBeatMap(bid=814293):
    try:
        res = urllib2.urlopen('https://osu.ppy.sh/api/get_beatmaps?k=b68fc239f6b8bdcbb766320bf4579696c270b349&b='+str(bid),timeout=2)
        print 'getting beatmap:'+str(bid)
        html = res.read()
        result = json.loads(html)
        
    except:
        print 'error beatamp:'+str(bid)
        result=[]

    return result

if __name__=="__main__":
    #起始页码
    getBpList(61,76)
    write('2k1-2k4')

    

    