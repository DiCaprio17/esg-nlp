# encoding:utf-8
import fastText as ft
import re
import jieba


# 读停用词文件
def stopwordslist():
    stopwords = [line.strip() for line in
                 open(r'../data/stop_words.txt', 'r',
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


def apply(title, content):
    data_dict = {}
    get_title = get_chinese(title)
    get_content = get_chinese(content)
    if get_title == "" or get_content == "":
        data_dict['is_esg'] = ["NESG", 1]
        data_dict['message'] = "not_esg"
        return data_dict
    print(get_title + get_content)

    # 一级
    model = ft.load_model('../model/label1_lr0.05_epoch10.model')
    data = model.predict(get_title + ' ' + get_content)
    data_dict['is_esg'] = [data[0][0][9:], '%.3f' % data[1][0]]
    print(data)
    if data[0][0][9:] == 'NESG' and data[1][0] > 0.5:
        data_dict['message'] = "not_esg"
    else:
        # 二级
        model = ft.load_model('../model/label2_lr0.07_epoch135.model')
        data = model.predict(get_title + ' ' + get_content)
        data_dict['esg'] = [data[0][0][9:], '%.3f' % data[1][0]]
        print(data)
        # 三级
        model = ft.load_model('../model/label3_lr1_epoch55.model')
        data = model.predict(get_title + ' ' + get_content)
        data_dict['label'] = [data[0][0][9:], '%.3f' % data[1][0]]
        print(data)
        data_dict['message'] = "is_esg"
    return data_dict


if __name__ == "__main__":
    apply("asasd", "asdfe")
