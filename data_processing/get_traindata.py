import csv
import re
import jieba


# 读取关键词txt文件
def open_filter(name):
    get_word = []
    with open(name, encoding='UTF-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n').strip()
        if lines[i] != '':
            # lines.pop(i)
            get_word.append(lines[i])
    # print(get_word)
    return get_word


# 读停用词文件
def stopwordslist():
    stopwords = [line.strip() for line in
                 open(r'./data/stop_words.txt', 'r',
                      encoding='utf-8').readlines()]
    return stopwords


def class_label(classf, l_label, v):
    fw_train = open(
        r'./data/cooking_label2-2.train',
        'a',
        encoding='utf-8')
    fw_valid = open(
        r'./data/cooking_label2-2.valid',
        'a',
        encoding='utf-8')
    fw_unuse = open(r'./data/label/unuse.txt',
                    'a',
                    encoding='utf-8')
    for i in range(len(l_label)):
        title = get_chinese(l_label[i][1])
        outstr = get_chinese(l_label[i][2])
        if outstr == '':
            print(l_label[i])
        if i < v * len(l_label):
            fw_train.write('__label__' + classf + ' ' + title + '  ' + outstr + '\n')
        else:
            fw_valid.write('__label__' + classf + ' ' + title + '  ' + outstr + '\n')
    fw_train.close()
    fw_valid.close()
    fw_unuse.close()


# 2/8 一级ESG标签
# v=0.8,训练测试82分配 csv格式
def csv_train_test_label1(v):
    f_tf_dic = open(
        r'./data/ESG_label.csv', 'r',
        errors='ignore', encoding='GBK')
    f1 = csv.reader(f_tf_dic)
    f_tf_dic = open(
        r'./data/ESG_label.csv', 'r',
        errors='ignore', encoding='GBK')
    f2 = csv.reader(f_tf_dic)
    fw1 = open(r'./data/cooking_label1.train',
               'w',
               encoding='utf-8')
    fw2 = open(r'./data/cooking_label1.valid',
               'w',
               encoding='utf-8')
    lines_code = ['ESG', 'NESG']
    ESG_id = {}
    ESG_id2 = {}
    for i in range(len(lines_code)):
        ESG_id[lines_code[i]] = 0
        ESG_id2[lines_code[i]] = 0
    for l in f1:
        if l[2] != '':
            ESG = 'ESG'
        else:
            ESG = 'NESG'
        ESG_id[ESG] += 1
    print(ESG_id)
    ESG_id8 = {}
    for k in ESG_id:
        ESG_id8[k] = int(ESG_id[k] * v)
    print(ESG_id8)

    for l in f2:
        # 只提取中文
        title = get_chinese(l[0])
        outstr = get_chinese(l[1])
        ESG = ''
        if l[2] != '':
            ESG = 'ESG'
        else:
            ESG = 'NESG'
        if ESG_id2[ESG] < ESG_id8[ESG]:
            ESG_id2[ESG] += 1
            fw1.write('__label__' + str(ESG) + ' ' + title + '  ' + outstr + '\n')
        else:
            fw2.write('__label__' + str(ESG) + ' ' + title + '  ' + outstr + '\n')
    print(ESG_id2)
    f_tf_dic.close()
    fw1.close()
    fw2.close()


# 2/8 二级环境、社会标签
# v=0.8,训练测试82分配 csv格式
def csv_train_test_label2(v):
    f_tf_dic = open(
        './data/519.csv', 'r',
        errors='ignore', encoding='GBK')
    f1 = csv.reader(f_tf_dic)
    fw_train = open(
        r'./data/cooking_label2-2.train',
        'w',
        encoding='utf-8')
    fw_valid = open(
        r'./data/cooking_label2-2.valid',
        'w',
        encoding='utf-8')
    fw_train.close()
    fw_valid.close()
    env_label = open_filter(
        './data/label/3_env_label.txt')
    soc_label = open_filter(
        './data/label/3_soc_label.txt')
    # compa_label = open_filter(
    #     '/home/puluwen/workspace/industry/text-classification-cnn-rnn-master/data/label/3_company_label.txt')
    fw_unuse = open(r'./data/label/unuse.txt',
                    'w',
                    encoding='utf-8')
    fw_unuse = open(r'./data/label/unuse.txt',
                    'a',
                    encoding='utf-8')
    # 建立标签字典，统计每个标签的数量
    label_dic = {}
    for l in env_label:
        label_dic[l] = 0
    for l in soc_label:
        label_dic[l] = 0
    # for l in compa_label:
    #     label_dic[l] = 0

    # 建立类别字典，统计每个标签的数量
    class_dic = {}
    class_dic['环境类'] = 0
    class_dic['社会类'] = 0
    # class_dic['公司治理类'] = 0

    l_env_label = []
    l_soc_label = []
    # l_compa_label = []
    for l in f1:
        l_split = l[3].replace(',', '，').split('，')
        if len(l_split) <= 1:
            flag = 1
            if l[3] in env_label:
                l_env_label.append(l)
                class_dic['环境类'] += 1
            elif l[3] in soc_label:
                l_soc_label.append(l)
                class_dic['社会类'] += 1
            # elif l[3] in compa_label:
            #     l_compa_label.append(l)
            #     class_dic['公司治理类'] += 1
            else:
                flag = 0
                fw_unuse.write(str(l[3]) + '\n')
            if flag == 1:
                label_dic[l[3]] += 1
        else:
            for l_s in l_split:
                flag = 1
                if l_s in env_label:
                    l_env_label.append(l)
                    class_dic['环境类'] += 1
                elif l_s in soc_label:
                    l_soc_label.append(l)
                    class_dic['社会类'] += 1
                # elif l_s in compa_label:
                #     l_compa_label.append(l)
                #     class_dic['公司治理类'] += 1
                else:
                    flag = 0
                    fw_unuse.write(str(l[3]) + '\n')
                if flag == 1:
                    label_dic[l_s] += 1

    # 环境标签
    class_label('环境类', l_env_label, v)
    # 社会标签
    class_label('社会类', l_soc_label, v)
    # 公司治理标签
    # class_label('公司治理类', l_compa_label, v)
    f_tf_dic.close()
    fw_unuse.close()
    print(label_dic)
    print(class_dic)


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


# 2/8 三级标签
# v=0.8,训练测试82分配 csv格式
def csv_train_test_label3(v):
    f_tf_dic = open(
        './data/1246+1212.csv', 'r',
        errors='ignore', encoding='GBK')
    f1 = csv.reader(f_tf_dic)
    f_tf_dic = open(
        './data/1246+1212.csv', 'r',
        errors='ignore', encoding='GBK')
    f2 = csv.reader(f_tf_dic)
    fw_train = open(
        r'./data/cooking_label3+1212.train',
        'w',
        encoding='utf-8')
    fw_valid = open(
        r'./data/cooking_label3+1212.valid',
        'w',
        encoding='utf-8')
    env_label = open_filter(
        './data/label/3_env_label.txt')
    soc_label = open_filter(
        './data/label/3_soc_label.txt')
    compa_label = open_filter(
        './data/label/3_company_label.txt')

    # 建立标签字典，统计每个标签的数量
    label_dic = {}
    label_dic_count = {}
    for l in env_label:
        label_dic[l] = 0
        label_dic_count[l] = 0
    for l in soc_label:
        label_dic[l] = 0
        label_dic_count[l] = 0
    for l in compa_label:
        label_dic[l] = 0
        label_dic_count[l] = 0

    for l in f1:
        l_split = l[3].split('，')
        if len(l_split) <= 1:
            if l[3] in label_dic:
                label_dic[l[3]] += 1
        else:
            for l_s in l_split:
                if l_s in label_dic:
                    label_dic[l_s] += 1
    print(label_dic)

    for l in f2:
        l_split = l[3].split('，')
        if len(l_split) <= 1:
            if l[3] in label_dic:
                title = get_chinese(l[1])
                outstr = get_chinese(l[2])
                if label_dic_count[l[3]] < v * label_dic[l[3]]:
                    fw_train.write('__label__' + l[3] + ' ' + title + '  ' + outstr + '\n')
                    label_dic_count[l[3]] += 1
                else:
                    fw_valid.write('__label__' + l[3] + ' ' + title + '  ' + outstr + '\n')

        else:
            for l_s in l_split:
                if l_s in label_dic:
                    title = get_chinese(l[1])
                    outstr = get_chinese(l[2])
                    if label_dic_count[l_s] < v * label_dic[l_s]:
                        fw_train.write('__label__' + l_s + ' ' + title + '  ' + outstr + '\n')
                        label_dic_count[l_s] += 1
                    else:
                        fw_valid.write('__label__' + l_s + ' ' + title + '  ' + outstr + '\n')
    f_tf_dic.close()
    fw_train.close()
    fw_valid.close()


if __name__ == "__main__":
    # csv_train_test_label1(0.8)
    # csv_train_test_label2(0.8)
    # csv_train_test_label3(0.8)
    print(1)
