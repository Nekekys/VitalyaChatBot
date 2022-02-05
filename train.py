import re
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

f = open('dialoguesVK.txt', 'r', encoding="utf-8")
content = f.read()
dialogs = [line.split('\n') for line in content.split('\n\n')]


import_data = []
for dig in dialogs:
    if len(dig) > 1:
        reDig1 = re.sub('[^А-Яа-яё\s]+', '', dig[0])
        reDig2 = re.sub('[^А-Яа-яё\s]+', '', dig[1])
        reDig1 = ' '.join(reDig1.split())
        reDig2 = ' '.join(reDig2.split())
        import_data.append(reDig1)
        import_data.append(reDig2)



Tagged_Document = gensim.models.doc2vec.TaggedDocument
def X_train(sentence):
    x_train = []
    for i,text in enumerate(sentence):
        word_list = text.split(' ')
        document = Tagged_Document(word_list,tags = [i])
        x_train.append(document)
    return x_train
result = X_train(import_data)


# Модельное обучение
model = Doc2Vec(result, dm=1, vector_size=200, window=10, min_count=1, workers=8,epochs = 500,sample=20)
 # Сохранить модель
model.save('models_doc2vec_200_vector_size_vk/ko_d2v.model')