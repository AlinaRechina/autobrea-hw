import re
import json
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

# пример неполного словаря
with open('n_final_dict.json', encoding = 'utf-8') as f:
  our_dict = json.load(f)

# ТУТ надо в нач форму our_dict
our_real_dict = {}
for i in our_dict:
  listr = []
  listr.append(our_dict[i][0].lower())
  listr.append(our_dict[i][1].lower())
  listr.append(our_dict[i][2])
  our_real_dict[i] = listr

"""Дальше идут 5 функций, а потом уже ячейка запуска поиска

"""

# ЭТА ОБРАБАТЫВАЕТ КАЖДОЕ СЛОВО, ПОЭТОМУ НЕЛЬЗЯ, НАПРИМЕР, ИСКАТЬ "пойти в", надо "пойти" "в"
def processing_of_item(word):
  word = word.lower()
  if ("\"") in word or ("\'") in word:
    wtype = 1 # тип запроса
    word = word.strip("\"")
    word = word.strip("\'")
    fword = [word,]
  elif ("+") in word:
    wtype = 2
    word = word.split("+") # Напоминаю, что мы берём точную форму первого слова, в противном случае +1 шаг
#    word = " ".join([word[0], "[^\s]+", word[1]])
    fword = [word[0], "[^\s]+", word[1]]
  elif len(set(word).intersection(set("ёйцукенгшщзхъфывапролджэячсмитьбю"))) == 0:
    wtype = 3
    fword = [word,]
  else:
    wtype = 4
    word = morph.parse(word)[0].normal_form
    fword = [word,]
  return(wtype, fword)

# ЭТА НА СТЫКЕ ДВУХ СЛОВ ВЫБИРАЕТ КАКОЙ ПАТТЕРН ДЛЯ РЕГУЛЯРКИ
def middle_pattern(left, right):
  left_num = processing_of_item(left)[0]
  right_num = processing_of_item(right)[0]
  pattern = str(left_num) + str(right_num)
  list_for_pattern = [" ".join(processing_of_item(left)[1]),]
  num_items = 0
  if pattern in ["24", "34", "41", "42"]:
    num_items = 1
  elif pattern in ["11", "12", "23", "33", "44"]:
    num_items = 2
  elif pattern in ["14", "43"]:
    num_items = 3
  elif pattern == "13":
    num_items = 4
  for i in range(num_items):
    list_for_pattern.append("[^\s]+")
  list_for_pattern.append(" ".join(processing_of_item(right)[1]))
  return list_for_pattern

# ЭТА ДЕЛАЕТ ВЕСЬ ПАТТЕРН regexp (она выводит 3 элемента а нужен только 1й но мне было уже тяжело всё почистить потом сделаю)
def making_whole_pattern(request):
  all_words = []
  all_wtypes = []
  if not " " in request: # То есть всего одно слово в запросе
    complete_str = " ".join(processing_of_item(request)[1])
    type_of_first_pattern = str(processing_of_item(request)[0])
    all_words.append(processing_of_item(request)[1][0])
    all_wtypes.append(type_of_first_pattern)
  else:
    complete_list = []
    count = 1
    request_list = request.split(" ")
    for i in range(len(request_list)-1):
      left = request_list[count-1]
      right = request_list[count]
      pattern_list = middle_pattern(left, right)
      if len(complete_list) == 0:
        type_of_first_pattern = str(processing_of_item(left)[0])
        for i in pattern_list:
          complete_list.append(i)
      else:
        for i in pattern_list[1::]:
          complete_list.append(i)
      all_words.append(processing_of_item(left)[1][0])
      all_wtypes.append(processing_of_item(left)[0])
      if count == len(request_list)-1:
        all_words.append(processing_of_item(right)[1][0])
        all_wtypes.append(processing_of_item(right)[0])
      count += 1
    complete_str = " ".join(complete_list)
  return complete_str, all_wtypes, all_words

# ЭТА ДЕЛАЕТ ФИНАЛЬНЫЙ ЗАПРОС И НАХОДИТ ВСЕ ВХОЖДЕНИЯ (НО без пунктуации)
def wordowski_search(pattern, ty):
  dict_of_all = {}
  for i in our_real_dict:
    d_string = " "+our_real_dict[i][1]+" "
    d_pattern = " "+pattern+" "
    if ty == ['1']:  
        if bool (re.search(d_pattern, d_string, flags=re.I)) == True and \
d_string[d_string.find(d_pattern)+len(d_pattern)] not in set('qwertyuiopasdfghjklzxcvbnm'):
          z_pattent = re.search(d_pattern, d_string).group(0)
          left = d_string.partition(z_pattent)[0].split()
          center = d_string.partition(z_pattent)[1].split()
          if len(left)%3 == 1:
            center.insert(0, left[-1])
          elif len(left)%3 == 2:
            center.insert(0, left[-1])
            center.insert(0, left[-2])
          final_final_center = []
          for g in range(len(center)):
            if g%3 == 0:
              final_final_center.append(center[g])
          dict_of_all[i] = " ".join(final_final_center)
    elif ty == ['4']:
        if bool (re.search(d_pattern, d_string, flags=re.I)) == True:
          z_pattent = re.search(d_pattern, d_string).group(0)
          left = d_string.partition(z_pattent)[0].split()
          center = d_string.partition(z_pattent)[1].split()
          if len(left)%3 == 1:
            center.insert(0, left[-1])
          elif len(left)%3 == 2:
            center.insert(0, left[-1])
            center.insert(0, left[-2])
          final_final_center = []
          for g in range(len(center)):
            if g%3 == 0:
              final_final_center.append(center[g])
          dict_of_all[i] = " ".join(final_final_center)
    else:
        if bool (re.search(d_pattern, d_string, flags=re.I)) == True:
          z_pattent = re.search(d_pattern, d_string).group(0)
          left = d_string.partition(z_pattent)[0].split()
          center = d_string.partition(z_pattent)[1].split()
          if len(left)%3 == 1:
            center.insert(0, left[-1])
          elif len(left)%3 == 2:
            center.insert(0, left[-1])
            center.insert(0, left[-2])
          final_final_center = []
          for g in range(len(center)):
            if g%3 == 0:
              final_final_center.append(center[g])
          dict_of_all[i] = " ".join(final_final_center)
  return dict_of_all

# ЭТА для КрАсИвОгО вывода (я потратила половину времени на это)
# В идеале прикручу, чтобы можно было выбирать цвет, но это уже по согласованию с Алиной
# В идеале в идеале сделать чтобы больше одного вхождения выделялось, но это совсем о связи 
def make_beautiful_print(dict_with_words):
  full = []
  if len(dict_with_words) == 0:
    full.append(["",["Извините, по вашему запросу ничего не найдено.", "", ""]])
  else:
    for i in dict_with_words:
      without_punctuation = ""
      for g in range(len(dict_with_words[i].split())):
        without_punctuation += dict_with_words[i].split()[g]
        if g != len(dict_with_words[i].split())-1:
          without_punctuation += "[^\w]*"
      punctuation_pattent = re.search(without_punctuation, our_real_dict[i][0]).group(0)
      mda = " " + our_real_dict[i][0] + " " # Вся строка
      mda_left = (mda.partition(" " + punctuation_pattent))[0]
      mda_right = (mda.partition(" " + punctuation_pattent))[2]
      if mda_right != "" and mda_right.strip() != "":
        if mda_right.strip()[0] in ("ёйцукенгшщзхъфывапролджэячсмитьбю"):
          mda_right = " " + mda_right.strip()
        else:
          mda_right = mda_right.strip()
      if mda_left != "":
        mda_left = mda_left.strip() + " "
        mda_left = mda_left.capitalize()
        queue = punctuation_pattent
      else:
        queue = punctuation_pattent.strip().capitalize()
      new_i = [our_real_dict[i][2], 
               [mda_left, queue, mda_right]]
      full.append(new_i)
    
    return full


# ЧАСТЬ ЧТО НАДО БУДЕТ ЗАПУСКАТЬ
#request = str(input('Введите запрос: '))
#print(make_beautiful_print(wordowski_search(making_whole_pattern(request)[0])))

