import csv
import re
import os
import fasttext
import jieba

"""把标签及其对应数量统计到csv文件中"""


# 统计每个标签含有的新闻数量
def label2csv(path):
    # '/home/puluwen/workspace/industry/text-classification-cnn-rnn-master/data/label/label_count.csv', 'w',
    f_tf_dic = open(
        path, 'w',
        newline='', encoding='utf-8-sig')
    # dic = {'新能源利用': 57, '绿色地产': 1, '节能降耗': 4, '环保力度升级': 160, '环保市场机遇': 118, '环保技术升级': 34, '关停落后产能': 26, '新能源车政策': 3,
    #        '新能源政策': 2, '禁止垃圾进口': 2, '温室气体减排': 26, '水污染治理': 23, '极端天气': 3, '新能源车发展': 36, '新能源车补贴': 2, '大气污染治理': 7,
    #        '垃圾分类': 6, '生态多样性保护': 96, '加强环保信披': 3, '绿色金融': 1, '碳交易': 12, '水资源保护': 6, '垃圾处理': 16, '土壤污染防治': 5,
    #        '大气污染防治': 38, '水利建设': 1, '固废处理': 6, '危废处理': 4, '煤改气': 8, '环保建材': 1, '关停限产': 0, '自然灾害': 2, '绿色物流': 3,
    #        '非洲猪瘟': 7, '禽流感': 1, '家禽福利': 1, '员工降薪': 2, '偷工减料': 2, '产品质量安全': 6, '食品安全问题': 5, '信息安全': 19, '游戏上瘾': 11,
    #        '游戏审查': 24, '消费升级': 3, '老龄化机遇': 5, '健康生活': 2, '金融产品安全': 43, '国企改革': 4, '员工权利保护': 1, '职业健康与安全': 7,
    #        '知识产权保护': 11, '未成年人保护': 7, '员工职业道德': 1, '商业贿赂': 1, '网络安全': 6, '产业扶贫': 19, '食品安全政策': 4, '食品安全稽查': 4,
    #        '生产安全稽查': 1, '员工自杀': 1, '安全事故': 9, '裁员': 1, '逃税漏税': 0, '消费者投诉': 2, '反垄断调查': 1, '信息泄露': 0, '黑客攻击': 0,
    #        '霸王条款': 0, '客户隐私保护': 0, '工商处罚': 0, '企业内部腐败': 1, '慈善扶贫': 3, '信用体系建设': 9}
    # dic = {'保险业': 300, '林业': 300, '航空运输业': 300, '金属制品业': 30, '餐饮业': 300, '煤炭开采和洗选业': 300, '仓储业': 300, '零售业': 300, '畜牧业': 300, '道路运输业': 300, '电力、热力生产和供应业': 300, '房地产业': 300, '电气机械及器材制造业': 300, '农业': 300, '纺织服装、服饰业': 300, '纺织业': 300, '非金属矿采选业': 112, '废弃资源综合利用业': 300, '皮革、毛皮、羽毛及其制品和制鞋业': 300, '互联网和相关服务': 300, '化学纤维制造业': 300, '化学原料及化学制品制造业': 300, '货币金融服务': 300, '汽车制造业': 300, '纺织服装装饰业': 27, '光伏': 300, '有色金属': 36}
    dic = {'新能源利用': 111, '绿色地产': 14, '节能降耗': 12, '环保力度升级': 255, '环保市场机遇': 118, '环保技术升级': 75, '关停落后产能': 26, '新能源车政策': 39, '新能源政策': 30, '禁止垃圾进口': 4, '温室气体减排': 52, '水污染治理': 62, '极端天气': 33, '新能源车发展': 46, '新能源车补贴': 143, '大气污染治理': 173, '垃圾分类': 68, '生态多样性保护': 111, '加强环保信披': 3, '绿色金融': 2, '碳交易': 15, '水资源保护': 13, '垃圾处理': 36, '土壤污染防治': 11, '大气污染防治': 75, '水利建设': 1, '固废处理': 17, '危废处理': 71, '煤改气': 11, '环保建材': 49, '关停限产': 40, '自然灾害': 11, '绿色物流': 81, '非洲猪瘟': 12, '禽流感': 35, '家禽福利': 1, '国六标准': 85, '动物福利': 62, '噪音污染防治': 8, '员工降薪': 6, '偷工减料': 16, '产品质量安全': 29, '食品安全问题': 15, '信息安全': 19, '游戏上瘾': 12, '游戏审查': 24, '消费升级': 13, '老龄化机遇': 10, '健康生活': 14, '金融产品安全': 58, '国企改革': 8, '员工权利保护': 11, '职业健康与安全': 10, '知识产权保护': 14, '未成年人保护': 94, '员工职业道德': 4, '商业贿赂': 12, '网络安全': 16, '产业扶贫': 41, '食品安全政策': 14, '食品安全稽查': 11, '安全生产': 84, '员工自杀': 1, '安全事故': 20, '裁员': 7, '逃税漏税': 0, '消费者投诉': 13, '反垄断调查': 6, '信息泄露': 28, '黑客攻击': 8, '霸王条款': 5, '客户隐私保护': 0, '工商处罚': 0, '企业内部腐败': 3, '慈善扶贫': 16, '信用体系建设': 24, '消费者权利保护': 18, '交通运输安全': 13, '客户隐私安全': 2, '性别歧视': 3, '食品质量安全': 31, '同股不同权': 0, '股东大会议案被否决': 0, '控股权之争': 0, '股权激励': 0, '引咎辞职': 19, '会计丑闻': 0, '职务侵占': 18, '违规担保': 14, '利益输送': 9, '审计所被处罚': 0}
    writer = csv.writer(f_tf_dic)  # ['标签', '新闻数量']
    writer.writerow(['标签', '新闻数量'])
    for k, v in dic.items():
        writer.writerow([k, v])
    f_tf_dic.close()


"""
1.去除csv文件中重复的新闻
2.去除csv文件中字段有缺失的新闻
并重新写入csv"""


def del_csv(path):
    with open(
            path, 'r',
            errors='ignore', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        new_data_list = []
        for l in reader:
            if l[3] != '' and l[1] != '' and l[2] != '' and l[0] != '':
                new_data_list.append(l)
            else:
                # print(l)
                pass
    del_data_list = []
    title_list = []
    for i in range(len(new_data_list)):
        flag = 0
        for j in range(len(new_data_list)):
            if i != j:
                # 只提取中文
                d_i = get_chinese(new_data_list[i][0])
                d_j = get_chinese(new_data_list[j][0])

                if d_i == d_j:
                    flag = 1

        if flag == 0:
            del_data_list.append(new_data_list[i])
            c_title = get_chinese(new_data_list[i][0])
            title_list.append(c_title)
        else:
            c_title = get_chinese(new_data_list[i][0])
            if c_title not in title_list:
                del_data_list.append(new_data_list[i])
                title_list.append(c_title)
    # print(del_data_list)
    write_csv("./test2.csv", del_data_list[1:], path)


# 读停用词文件
def stopwordslist():
    stopwords = [line.strip() for line in
                 open(r'./data/stop_words.txt', 'r',
                      encoding='utf-8').readlines()]
    return stopwords


# 提取中文
def get_chinese(data):
    stopwords = stopwordslist()
    # 只提取中文
    re_words = re.compile(r"[\u4e00-\u9fa5]+")
    m = re_words.findall(data)
    lres = ''
    for n in m:
        lres = lres + n
    jieba_seg_list = jieba.cut(lres)
    outstr = ''
    for word in jieba_seg_list:
        if word == '\n' or word == '摘要':
            word = ''
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    outstr = outstr.strip(' ')
    return outstr


def write_csv(path, data_list, url):
    csvfile = open(path, 'a', newline='', encoding='utf-8-sig')
    # fileheader = ["title", "url", "date", "content"]
    writer = csv.writer(csvfile)
    # writer.writerow(fileheader)
    re_words = re.compile(r"[\u4e00-\u9fa5]+")
    m = re_words.findall(url[35:])
    for l in data_list:
        # print(l)
        writer.writerow([l[0], l[1], l[2], l[3], m[0][:-3]])
    csvfile.close()


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        pass
        # print(root)  # 当前目录路径
        # print(files)  # 当前路径下所有非目录子文件
    file_list = []
    for l in files:
        file_list.append(root + "\\" + l)
    # print(file_list)
    return file_list


# 通过模型预测出标签正确的保存到csv文件
def select_label():
    writer_csvfile = open('./data/ESG_news.csv', 'w', newline='', encoding='UTF-8-sig')  # python3下
    writer = csv.writer(writer_csvfile)
    reader_csvfile = open(
        r'./test3.csv', 'r',
        errors='ignore', encoding='gbk')
    reader = csv.reader(reader_csvfile)

    model = fasttext.load_model('./model/label1_lr0.05_epoch10.model')
    # a = model.predict(
    #     "中新网月日电据日媒报道由日本自民党前防卫相稻田朋美担任会长的保守派团体传统与创造会近日在国会召开会议资料图此前日本东京日本防卫大臣稻田朋美在记者会上正式宣布辞职报道指出稻田在月因南苏丹联合国维和行动部队日报隐瞒问题而引咎辞职后一直很少参与政治活动此次重新启动是为了挽回信誉稻田在会议伊始称作为防卫相的一年是非常严峻的考验时期将反省应该反省的地方希望回归政治原点继续开展活动报道指出依靠日本首相安倍晋三这一强大后盾稻田曾出任行政改革担当相该党政调会长等重要职务她曾宣称自己的最终目标是首相希望通过团体活动就安全保障历史认识问题及修改宪法等加强宣传能力据悉出席会议的有日本众参两院名国会议员所谓的传统与创造会以年众院选举中首次当选的保守派议员为主组建其成员在旧金山和约生效日本恢复主权的月日及月日终战纪念日每年都会参拜靖国神社")
    # print(a)
    for l in reader:
        result = model.predict(get_chinese(l[3]))
        # print(l)
        # print(result[0][0])
        # print(result[1][0])
        if result[0][0] == '__label__ESG':
            writer.writerow([l[0], l[1], l[2], l[3], l[4], result[1][0]])
    writer_csvfile.close()
    reader_csvfile.close()


if __name__ == "__main__":
    label2csv("./data/label_count.csv")
    # del_csv(r'C:\Users\hwangnuozhong\Downloads\2020-1-8-18-14-42-31374552261950-引咎辞职的数据-后羿采集器.csv')
    # file_list = file_name(r'C:\Users\hwangnuozhong\Downloads\1')
    # for l in file_list:
    #     try:
    #         del_csv(l)
    #     except:
    #         print(l)
    # select_label()
