# ФКЗ-6-ФКЗ-21_03_2014.rtf ,ФКЗ-5-ФКЗ-28_06_2004.rtf, ФКЗ-5-ФКЗ-21_07_2007.rtf
# https://petr-panda.ru/sravnvit-teksty/ - проверить пропажу данных
import re
# объединяет/группирует всю метаинформацию (вход: лист, выход: лист ( на все метаданные в <...>) и количесво объединений
def Unite(list):
    d = 0
    for i in range(len(list)):
        if i+1 >= len(list):
            break
        if ('<' not in list[i]) & ('>' not in list[i+1]):
            list[i] = list[i]+list[i+1]
            list.pop(i+1)
            d = d+1
    return list, d
# Переводит текст в лист, содержащий только текст обрабатываемый в дальнейшем
def Convert_Text_To_List_Of_Sentence(text):
    text_out = []
    # количество изменений в метаданных
    d = 1
    #Убирает английский язык, &nbsp;,</span>
    text = re.sub(r'[0-9]+</span>|[a-zA-Z]+|&[a-z]{4};', ' ', text)
    text = ''.join(text)
    # находит метаинформацию, предложения
    text = re.findall(r'<.*?>|[а-яА-Я :#№;,"\'\.?!()\-0-9]+', text)
    # объединяет гркппу метаинформации
    while (d > 0):
        text, d = Unite(text)
    text = [item for item in text if (item not in ' ') & (item not in '  ')]
    # Если между метаинформациями текст, то заносит в выходной текст его
    for i in range(len(text)):
        if i+2 >= len(text):
            break
        if ('<' in text[i]) & ('>' not in text[i+1]) & ('<' in text[i+2]):
            text_out.append(text[i+1]+'\n')
    return text_out
# Нумерует абзацы ( или специальные предложения, что были стилистически подчеркнуты) (Вход: Лист, Выход:Лист)
def Num_Sentence(list):
    text_out = []
    num = 0
    i=-1
    #  в том случае, если весь текст содержится в 1 элементе исходного списка
    if (len(list)<3):
        list1 = []
        # Так как на сайте все отступы соблюдены за счет пробела, то группа пробелов переводится в спец знак /del
        for i in range(len(list)):
            list1.append(re.sub(r'     [ ]+', ' /del ', list[i]))
        list1 = ''.join(list1).split('\n')
        list1 = ''.join(list1)
        list = re.findall(r'<.*?>|[а-яА-Я :#;№,"\'\.?!()\-0-9]+', list1)
    bracketed = False
    # Случай, если последние символы- пробелы
    for j in range(len(list)):
        list[j]=list[j].rstrip()

    while(i < len(list)):
        i = i + 1
        if(i+1) >= len(list):
            break
        #     Объединение значений в скобках ( )
        if ( '(' in list[i]):
            j = i
            bracketed = True
            if ( ')' in list[i]):
                bracketed = False
            if bracketed:
                i = i + 1
                while( ')' not in list[i]):
                    list[j] = list[j] + list[i]
                    list.pop(i)
                list[j] = list[j] + list[i]
                list.pop(i)
                bracketed = False
                i=j
                list[i]=re.sub(r'\n','', list[i])
                list[i-1]=list[i-1]+list[i]
                list.pop(i)
                i=i-1
                num = num - 1
                text_out.pop()
        #         Предложение заканчиается числом, присвоение дальнейших элементов
        if(re.findall(r'[0-9]$', list[i]) != []):
            while (re.findall(r'[0-9]$', list[i]) != []):
                list[i] = re.sub(r'\n', '', list[i])
                list[i] = list[i] + list[i+1]
                list.pop(i+1)
        # Предыдущее Предложение заканчиается буквой или запятой, присвоение элементов к тому элементу
        if (i-1>0)&( re.findall(r'[а-я]$|[, ]$', list[i-1]) != []):
            while ( re.findall(r'[а-я]$|[, ]$', list[i-1]) != []):
                list[i - 1] = list[i - 1] + list[i]
                list.pop(i)
            text_out.pop()
            i=i-1
            num = num - 1
        # Предложение содержит заглавную букву или входит в перечисление
        if(re.findall(r'[А-Я]', list[i]) != []) | (re.findall(r'[0-9]+\)|[0-9]+\.', list[i]) != []):
            num = num+1
    #         text_out.append(list[i] + '\n')
            text_out.append(str(num) + ')   ' + list[i] + '\n')
    # for j in range(len(text_out)):
    #     text_out[j] = re.findall(r'([0-9]+\.)?[а-яА-Я :#;№,"\'?!()\-0-9]+\.|\(.*?\)|([0-9]+\))?[а-яА-Я :#;№,"\'?!()\-0-9]+\.', text_out[j])
    # text_out = ''.join(text_out)
    #
    # for j in range(len(text_out)):
    #     text_out[j]=str(j+1) + ')   ' + text_out[j] + '\n'

    return text_out

name = input('Введите расположение и название файла с расширением .rtf (если файл в 1 месте с исполняющим файлом, то можно только название): ')
text = open(name).read().split('\n')
text = ' '.join(text)

f_out = open('out_1.txt', 'w')

# работа с данными из body
delete_index = text.rfind('<body')
text = text[delete_index:]
delete_index = text.rfind('</body>')
text = text[:delete_index]

test = Convert_Text_To_List_Of_Sentence(text)
text_out = ''.join(test)
# text = re.sub(r'<.*?>|&[a-z]{4}|;|[a-zA-Z]+', '', text) ver 1
print(text_out)

f_out.write(text_out)
f_out.close()
f_out = open('out_2.txt', 'w')
test = Num_Sentence(test)
text_out = ''.join(test)
f_out.write(text_out)
f_out.close()
