from easynmt import EasyNMT

model = EasyNMT('mbart50_m2en')

sentence = ['เลือกบัญชี',' เปิดกว้างสร้างสัมพันธ์ เชื่อมโยงกัน สู่สมดุล']

print(model.translate(sentence, target_lang="en"))
