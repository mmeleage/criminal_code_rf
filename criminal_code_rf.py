import os
import matplotlib.pyplot as plt
import difflib

def main():
    directory = 'C:/Users/mmeleage/criminal_code_rf'
    filenames = os.listdir(directory)
    txt_filenames = sort_filenames_by_year(choose_txt_filenames(filenames))
    article_nums = get_article_nums(txt_filenames[-1])
    matr_of_texts = [[''] * len(txt_filenames) for i in range(len(article_nums))]
    matr_of_texts = get_matr_of_texts(txt_filenames, article_nums,\
                                      matr_of_texts)
    matr_of_statuses = [[''] * len(matr_of_texts[0]) \
                        for i in range(len(matr_of_texts))]
    matr_of_statuses = get_matr_of_statuses(matr_of_texts, matr_of_statuses)
    years = get_years_from_filenames(txt_filenames)
    print('      ', end = '')
    #for i in range(1, len(years)):
    #for i in range(1, 33):
    for i in range(33, len(years)):
        print(years[i], '', end = '')
    print()
    #for i in range(len(matr_of_statuses)):
    #for i in range(36):
    for i in range(36, len(matr_of_statuses)):
        print(article_nums[i], end = '')
        #for j in range(1, len(matr_of_statuses[i])):
        #for j in range(1, 33):
        for j in range(33, len(matr_of_statuses[i])):
            if j == 1:
                if matr_of_statuses[i][j] != '=':
                    print('  ', matr_of_statuses[i][j], end = '')
                else:
                    print('  ', ' ', end = '')
            else:
                if matr_of_statuses[i][j] != '=': 
                    print('   ', matr_of_statuses[i][j], end = '')
                else:
                    print('   ', ' ', end = '')
        print()
    unique_years = get_unique_years(years)
    arr_count_added, arr_count_deleted, arr_count_changed = \
                     total_count_by_years(matr_of_statuses)
    total_graph_by_years(unique_years, years,
                         arr_count_added, arr_count_deleted, arr_count_changed)

def choose_txt_filenames(filenames):
    new_filenames = []
    for filename in filenames:
        if filename.split('.')[1] == 'txt':
            new_filenames.append(filename)
    return new_filenames

def sort_filenames_by_year(txt_filenames):
    for i in range(1, len(txt_filenames) - 1):
        for j in range(1, len(txt_filenames) - i):
            year_1 = txt_filenames[j].split('.')[0].split('-')[-1]
            year_2 = txt_filenames[j + 1].split('.')[0].split('-')[-1]
            if year_1 > year_2:
                txt_filenames[j], txt_filenames[j + 1] =\
                                  txt_filenames[j + 1], txt_filenames[j]
            elif year_1 == year_2:
                month_1 = txt_filenames[j].split('.')[0].split('-')[1]
                month_2 = txt_filenames[j + 1].split('.')[0].split('-')[1]
                if month_1 > month_2:
                    txt_filenames[j], txt_filenames[j + 1] =\
                                  txt_filenames[j + 1], txt_filenames[j]
                elif month_1 == month_2:
                    day_1 = txt_filenames[j].split('.')[0].split('-')[2]
                    day_2 = txt_filenames[j + 1].split('.')[0].split('-')[2]
                    if day_1 > day_2:
                        txt_filenames[j], txt_filenames[j + 1] =\
                                  txt_filenames[j + 1], txt_filenames[j]
    return txt_filenames

def get_texts_from_file(filename):
    file = open(filename, 'r')
    texts = []
    text = ''
    for line in file:
        if line != '\n':
            text = text + line
        else:
             texts.append(text)
             text = ''
    texts.append(text)
    return texts

def get_article_nums(filename):
    texts = get_texts_from_file(filename)
    article_nums = []
    for i in range(len(texts)):
        article_nums.append(texts[i][7:12])
    return article_nums

def get_matr_of_texts(txt_filenames, article_nums, matr_of_texts):
    for i in range(len(txt_filenames)):
        file = open(txt_filenames[i], 'r')
        text = ''
        for line in file:
            if line != '\n':
                text = text + line
            else:
                cut_article_num = text[7:12]
                matr_of_texts[article_nums.index(cut_article_num)][i] = text
                text = ''

        cut_article_num = text[7:12]
        matr_of_texts[article_nums.index(cut_article_num)][i] = text
        file.close()
    return matr_of_texts

def get_matr_of_statuses(matr_of_texts, matr_of_statuses):
    for i in range(len(matr_of_texts)):
        flag = False
        for j in range(1, len(matr_of_texts[i])):
            if matr_of_texts[i][j] != matr_of_texts[i][j - 1]:
                if flag == False:
                    if matr_of_texts[i][j - 1] == '':
                        matr_of_statuses[i][j] = '+'
                    elif matr_of_texts[i][j][12:25] == 'Утратила силу':
                        matr_of_statuses[i][j] = '-'
                        flag = True
                    else:
                        matr_of_statuses[i][j] = '~'
            else:
                matr_of_statuses[i][j] = '='
    return matr_of_statuses

def get_years_from_filenames(txt_filenames):
    years = []
    for i in range(len(txt_filenames)):
        years.append(txt_filenames[i].split('.')[0].split('-')[-1])
    return years

def get_unique_years(years):
    unique_years = []
    temp = ''
    for i in range(1, len(years)):
        if years[i] != temp:
            unique_years.append(years[i])
            temp = years[i]
    return unique_years

def arr_count_by_unique_years(unique_years, years, arr_count_added,
                              arr_count_deleted, arr_count_changed):
    added_by_unique_years = [0] * len(unique_years)
    deleted_by_unique_years = [0] * len(unique_years)
    changed_by_unique_years = [0] * len(unique_years)
    for i in range(len(years) - 1):
        added_by_unique_years[unique_years.index(years[1:][i])] += \
        arr_count_added[i]
        deleted_by_unique_years[unique_years.index(years[1:][i])] += \
        arr_count_deleted[i]
        changed_by_unique_years[unique_years.index(years[1:][i])] += \
        arr_count_changed[i]
    return added_by_unique_years, deleted_by_unique_years,\
           changed_by_unique_years

def count_article_changes_by_years(num, article_nums, years, unique_years,
                                   matr_of_statuses):
    index = article_nums.index(num)
    count_changes = [0] * len(unique_years)
    for j in range(1, len(matr_of_statuses[0]) - 1):
        if matr_of_statuses[index][j] == '~':
            count_changes[unique_years.index(years[j])] += 1
    return count_changes

def total_count_by_years(matr_of_statuses):
    arr_count_added = []
    arr_count_deleted = []
    arr_count_changed = []
    for j in range(1, len(matr_of_statuses[0])):
        count_added = count_deleted = count_changed = 0
        for i in range(len(matr_of_statuses)):
            if matr_of_statuses[i][j] == '+':
                count_added += 1
            elif matr_of_statuses[i][j] == '-':
                count_deleted += 1
            elif matr_of_statuses[i][j] == '~':
                count_changed += 1
        arr_count_added.append(count_added)
        arr_count_deleted.append(count_deleted)
        arr_count_changed.append(count_changed)
    return arr_count_added, arr_count_deleted, arr_count_changed

def total_graph_by_years(unique_years, years, arr_count_added,\
                         arr_count_deleted, arr_count_changed):
    x = unique_years
    y_added, y_deleted, y_changed = arr_count_by_unique_years(unique_years,\
    years, arr_count_added,
                              arr_count_deleted, arr_count_changed)
    line_added, line_deleted, line_changed = \
                plt.plot(x, y_added, 'b-', x, y_deleted, 'r-', x, y_changed,
                         'g-')
    plt.axis(['1998', '2019', -5, 70])
    plt.title('Количество добавленных, утративших силу и измененных статей \
        по годам')
    plt.xlabel('Год')
    plt.ylabel('Количество')
    plt.legend((line_added, line_deleted, line_changed),
           ('Добавленные', 'Утратившие силу', 'Измененные'))
    plt.grid()
    plt.show()
    #plt.savefig('criminal_code_rf.png', format = 'png')

main()