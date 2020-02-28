import fastText as ft
# import fasttext.FastText as ft

# 成功 训练模型
classifier = ft.train_supervised(input="./data/cooking_label3.train", lr=0.29,
                                 epoch=85)
# model = classifier.save_model('./model/label1_lr0.05_epoch10.model')  # 保存模型

# 成功 加载模型
# model = fasttext.load_model('./model/label2_lr0.07_epoch135.model')
# result = model.test('./data/cooking_label2.train')
# model = fasttext.load_model('./model/label1_lr0.05_epoch10.model')
# model.predict()
result = classifier.test('./data/cooking_label3.train')
result2 = classifier.test('./data/cooking_label3.valid')
print(result)
print(result2)
# (197, 0.7715736040609137, 0.7715736040609137)
