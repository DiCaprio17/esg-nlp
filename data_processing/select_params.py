import csv
import re
import fastText as fasttext
from tqdm import tqdm
import yagmail
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("select_params—log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_chinese(data):
    re_words = re.compile(r"[\u4e00-\u9fa5]+")
    m = re_words.findall(data)
    lres = ''
    for n in m:
        lres = lres + n
    return lres


def floatrange(start, stop, steps):
    ''' Computes a range of floating value.

        Input:
            start (float)  : Start value.
            end   (float)  : End value
            steps (integer): Number of values

        Output:
            A list of floats

        Example:
            >>> print floatrange(0.25, 1.3, 5)
            [0.25, 0.51249999999999996, 0.77500000000000002, 1.0375000000000001, 1.3]
    '''
    return [start + float(i) * (stop - start) / (float(steps) - 1) for i in range(steps)]


def select_params(path):
    csvfile = open('./select_params/select_params3_02_28.csv', 'w', newline='', encoding='UTF-8')  # python3下
    # 文件头以列表的形式传入函数，列表的每个元素表示每一列的标识
    fileheader = ["lr", "epoch", "precision"]
    writer = csv.writer(csvfile)
    writer.writerow(fileheader)
    dic = {}
    l = []

    # 初步
    for lr2 in tqdm(floatrange(0.05, 1, 5)):
        lr2 = float("%.2f" % lr2)
        for epoch2 in range(5, 150, 20):
            model = fasttext.train_supervised(
                path + ".train",
                lr=lr2, epoch=epoch2, wordNgrams=2,
                label="__label__")
            result = model.test(
                path + '.valid')
            writer.writerow([lr2, epoch2, result[1]])
            dic[result[1]] = [lr2, epoch2]
            l.append(result[1])
    csvfile.close()

    # # 细筛
    # for lr2 in tqdm(floatrange(0.05, 0.3, 6)):
    #     lr2 = float("%.2f" % lr2)
    #     for epoch2 in range(5, 45, 5):
    #         model = fasttext.train_supervised(path + ".train", lr=lr2, epoch=epoch2, wordNgrams=2,
    #                                           label="__label__")
    #         result = model.test(path + '.valid')
    #         writer.writerow([lr2, epoch2, result[1]])
    #         dic[result[1]] = [lr2, epoch2]
    #         l.append(result[1])
    # csvfile.close()

    # # 保存模型
    # save_model(dic[insertionSort4(l)[-1]], path)


# 排序
def insertionSort4(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        curNum, preIndex = nums[i + 1], i  # curNum 保存当前待插入的数
        while preIndex >= 0 and curNum < nums[preIndex]:  # 将比 curNum 大的元素向后移动
            nums[preIndex + 1] = nums[preIndex]
            preIndex -= 1
        nums[preIndex + 1] = curNum  # 待插入的数的正确位置
    return nums


def send_email(content):
    # 登录你的邮箱
    yag = yagmail.SMTP(user='171628543@qq.com', password='procadfykhwhcabh', host='smtp.qq.com')
    # 发送邮件
    yag.send(to=['171628543@qq.com'], subject=content + ':select_params.py',
             contents=['select_params3', 'finish:select_params.py'])


# 得到一定范围内的最优参数后保存模型
def save_model(l, path):
    model = fasttext.train_supervised(
        path + '.train', lr=l[0],
        epoch=l[1], wordNgrams=2,
        label="__label__")
    model.save_model('model3_lr' + str(l[0]) + '_epoch' + str(l[1]) + '.bin')


if __name__ == "__main__":
    # # 1.未打标签的5万篇新闻生成idf，生成idf.txt
    # origin_data = unlabel_open_csv(
    #     r'/home/puluwen/workspace/industry/text-classification-cnn-rnn-master/data/unlabel.txt')
    # idf(origin_data)
    # idf(open_csv_col())
    # # # 2.打了标签的246篇新闻生成tf，生成tf.txt
    # # origin_data = open_csv(r'F:\PycharmProjects\text-classification-cnn-rnn-master\hnz-test\label.csv')
    # # tf(origin_data)
    # # 3.打了标签的246篇新闻tf * 未打标签的5万篇新闻生成tf-idf，生成tf_idf.txt
    # tf_idf()

    # 4.未打标签的任意一篇新闻生成idf，生成unlabel_idf.txt
    # origin_data = unlabel_open_csv(
    #     r'/home/puluwen/workspace/industry/text-classification-cnn-rnn-master/data/unlabel.txt')
    # unlabel_idf(origin_data)
    # open_csv_col()
    # unlabel_idf(open_csv_col())
    # 5.打了标签的246篇新闻tf * 未打标签的任意一篇新闻生成tf-idf，生成unlabel_tf_idf.txt

    time_start = time.time()
    logger.info("Start print log")

    # unlabel_tf_idf()
    try:
        select_params('./data/cooking_label3')
        send_email('SUCCESS')
    except:
        # pass
        send_email('FAIL')
    # save_model([0.86, 140])
    # # 6.对求余弦相似度之前进行数据处理，然后求余弦相似度，生成cos.txt
    # a, b = ready_cos()
    # cosine_similarity2(a, b)
    # # xinzeng()
    time_end = time.time()
    use_time = '%.4fmin' % ((time_end - time_start) / 60)
    if float(use_time[:-3]) > 60:
        use_time = '%.4fh' % (float(use_time[:-3]) / 60)
    print('time cost:', use_time)
    logger.info("Finish,time:{}".format(use_time))
