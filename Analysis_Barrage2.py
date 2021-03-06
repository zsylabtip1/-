import pandas as pd
import matplotlib.pyplot as plt
import os
import jieba.posseg as pseg
import pyecharts

'''绘制密度图'''
def barrage_compress_plt(data,num):
    line = pyecharts.Line("弹幕密度图")
    keys = []
    values = []
    for i in data:
        keys.append(data.index)
        values.append(data)
    line.add("弹幕数随时间的变化",keys,values)
    return line

'''计算弹幕的时间密度'''
def barrage_compress(data):
    df = data.drop_duplicates()
    dd = df.copy()
    a = [1] * 3002
    i = 0
    #向下取"整数秒"
    for item in dd.弹幕出现时间:
        a[i] = int(item)
        i += 1
    a.sort()
    dc = pd.DataFrame(a,columns=['弹幕出现时间'])
    result = dc['弹幕出现时间'].value_counts()
    final_result = result.sort_index()
    return final_result

'''统计弹幕长度'''
def static_barrage_length(data):
    df = data.drop_duplicates()
    dd = df.copy()
    dd['弹幕长度'] = [len(str(item)) for item in df.弹幕信息] #统计每条弹幕的长度
    d1 = dd.loc[:,['用户ID','弹幕信息','弹幕长度']]
    dr = d1.copy()
    return dr

'''每一集用户发送弹幕数量排序'''
def every_episode_usersort(data):
    df = data.drop_duplicates()
    dd = df.groupby("用户ID").count()
    user_sort = dd.sort_values(by = '弹幕信息',ascending=False).loc[:,['弹幕信息']]
    return user_sort

'''计算共有多少用户发弹幕'''
def every_episode_user(data):
    df = data.drop_duplicates()
    dd = df.groupby("用户ID").count()
    user_sum = len(dd)
    return user_sum

'''计算共有多少弹幕'''
def every_episode_comment(data):
    df = data.drop_duplicates()
    barrage_sum = len(df)
    return barrage_sum

'''计算发送弹幕数量排名--柱形图'''
def top_user_barrage(data):
    x = []
    y = []
    for i in range(5):
        x.append(data.index[i])
        y.append(data.弹幕信息.values[i])
    bar = pyecharts.Bar("弹幕发送数量排名")
    bar.add("发弹幕数Top5用户", x, y)
    return bar

'''每一集弹幕变化总量--折线图'''
def every_episode_comment_change(episode_comment_dic):
    line = pyecharts.Line("每一集弹幕变化总量",'2018-12-27',width=1200,height=600)
    keys = []
    values = []
    for i in episode_comment_dic:
        keys.append("第%d集" % i)
        values.append(episode_comment_dic[i])
    '''每一集弹幕总量的折线变化图'''
    line.add("每一集弹幕总量的折线变化图",keys,values)
    es = pyecharts.EffectScatter()
    es.add("",keys,values)
    overlap = pyecharts.Overlap()
    overlap.add(line)
    overlap.add(es)
    return overlap

'''每一集用户弹幕发送量--饼图'''
def every_episode_barrage_pie(d_tmp,num):
    a1 = len(d_tmp[(d_tmp.弹幕信息 >= 1) & (d_tmp.弹幕信息 <= 2)])
    a2 = len(d_tmp[(d_tmp.弹幕信息 >= 3) & (d_tmp.弹幕信息 <= 8)])
    a3 = len(d_tmp[(d_tmp.弹幕信息 >= 9) & (d_tmp.弹幕信息 <= 15)])
    a4 = len(d_tmp[(d_tmp.弹幕信息) >= 16])
    list = [a1, a2, a3, a4]
    labels = [u'1-2条',u'2-8条',u'9-15条',u'16条以上']
    pie = pyecharts.Pie("全职高手-第%d集" % num)
    pie.add('用户发送弹幕的条数及所占数量',labels,list,is_label_show=True)
    return pie

'''弹幕长度--饼图'''
def barrage_length_pie(d_tmp,i):
    a1 = len(d_tmp[(d_tmp.弹幕长度 >= 1) & (d_tmp.弹幕长度 <= 4)])
    a2 = len(d_tmp[(d_tmp.弹幕长度 >= 5) & (d_tmp.弹幕长度 <= 10)])
    a3 = len(d_tmp[(d_tmp.弹幕长度 >= 11) & (d_tmp.弹幕长度 <= 17)])
    a4 = len(d_tmp[(d_tmp.弹幕长度 >= 18)])
    labels = [u'1-4个字', u'5-10个字', u'11-17个字', u'18个以上字']
    list = [a1,a2,a3,a4]
    pie = pyecharts.Pie("全职高手-第%d集" % i)
    pie.add('用户发送弹幕的长度及所占数量',labels,list,is_label_show=True)
    return pie

'''词云'''
def extract_words(data, num):
    df = data.drop_duplicates()
    dd = df.copy()
    message_list = [str(item) for item in dd.弹幕信息]

    stop_words = set(line.strip() for line in open('E:/Python工作环境/B战/src/stopwords.txt', encoding ='utf - 8'))
    new_list = []
    for subject in message_list:
        if subject.isspace():
            continue
        word_list = pseg.cut(subject)
        for word, flag in word_list:
            if not word in stop_words and flag == 'n':
                new_list.append(word)
    dc = pd.DataFrame(new_list,columns=['message'])
    result = dc['message'].value_counts()
    final_result = result.sort_index()

    name = final_result[final_result.values>=10]
    values = name.values.tolist()
    final_name = name.index.tolist()
    print(final_name)
    print(values)
    wordcloud = pyecharts.WordCloud("全职高手-词云图")
    wordcloud.add("",final_name,values,word_size_range=[20,100])
    return wordcloud

def main():

    #获取文件路径
    path = os.getcwd()
    path_list = []
    for i in range(1,13):
        path_list.append(path+"\\now{}.csv".format(i))

    episode_comment_dic = {}     #弹幕总量
    user_sum_dic = {}            #各用户发送弹幕数量
    user_sort_dic = {}           #各用户发送弹幕数量排序
    barrage_length_dic = {}      #弹幕长度
    ciyun_data_dic = {}          #词云
    i = 1
    for path in path_list:
        '''读取csv数据源文件'''
        data = pd.read_csv(path.strip(),encoding='gbk',engine='python')

        '''统计每一集的弹幕总量，保存在字典中'''
        episode_comment_dic[i] = every_episode_comment(data)

        '''统计每一集共有多少用户发了弹幕,保存在字典中'''
        user_sum_dic[i] = every_episode_user(data)

        '''统计每一集的弹幕数量，根据弹幕数量，把用户排序，每一集排序后的结果是一个DataFrame'''
        user_sort_dic[i] = every_episode_usersort(data)

        '''统计发送弹幕的字符串长度'''
        barrage_length_dic[i] = static_barrage_length(data)

        '''统计每一集的分词，热词，词云'''
        ciyun_data_dic['i'] = data.copy()

        i += 1
        del data

        '''把经过排序统计处理后的所有DataFrame进行concat。然后就可以统计
        所有用户对12集视频发送弹幕的数量。最后进行排序，得到结果'''
    all_user = pd.concat([item for k,item in user_sort_dic.items()])
    all_user['用户ID'] = all_user.index
    sum = all_user.groupby(all_user.index).弹幕信息.sum()    
    all_barrage_sort = pd.DataFrame(sum).sort_values(by='弹幕信息',ascending=False)

    '''绘制折线图：12集视频,每集弹幕总数'''
    overlap = every_episode_comment_change(episode_comment_dic)

    '''柱形图：12集视频，进30天，所有用户中，发弹幕数量最多的5个用户'''
    bar = top_user_barrage(all_barrage_sort)
    timeline1 = pyecharts.Timeline(is_auto_play=True, timeline_bottom=0)
    page = pyecharts.Page()
    timeline2 = pyecharts.Timeline(is_auto_play=True, timeline_bottom=0)
    '''统计用户发送弹幕数量的百分比分布图'''
    for i in user_sort_dic:
        d_tmp = user_sort_dic[i]
        pie = every_episode_barrage_pie(d_tmp,i)
        timeline1.add(pie,i)
        del d_tmp
    page.add(timeline1)
    '''统计用户发送弹幕的长度分布百分比'''
    for i in barrage_length_dic:
        d_tmp = barrage_length_dic[i]
        pie2 = barrage_length_pie(d_tmp,i)
        timeline2.add(pie2,i)
        del d_tmp
    page.add(overlap)
    page.add(timeline2)
    page.add(bar)

    '''弹幕密度'''
    path2 = os.getcwd()
    now_barrage_list = []
    barrage_compress_dic = {}
    for i in range(1,13):
        now_barrage_list.append(path2+"\\now{}.csv".format(i))
    for item in now_barrage_list:
        data = pd.read_csv(item.strip(),encoding='gbk',engine='python')
        barrage_compress_dic['时间'] = barrage_compress(data)
    keys=[]
    values=[]
    for num,data in barrage_compress_dic.items():
        keys.append(data.index.values)
        values.append(data.values)
    
    keys1=keys[0]
    values1=values[0]
    

    line2 = pyecharts.Line("弹幕密度图")
    line2.add("弹幕数随时间的变化",keys1,values1,is_label_show=True)

    page.add(line2)
    
    '''制作词云'''
    for num,data in ciyun_data_dic.items():
        ciyun = extract_words(data,num)
        
        
    page.add(ciyun)

    page.render('最终.html')

if __name__ == '__main__':
    main()
