import csv

actor_link = open('../actor_link.csv', 'r', encoding='utf-8')
all_drama = open('../all_drama.csv', 'r', encoding='utf-8')
link_rdr = csv.reader(actor_link)
all_drama_rdr = csv.reader(all_drama)

actor_name_link = []
all_name = []
for line in link_rdr:
    actor_name_link.append(line[0].strip())

for line in all_drama_rdr:
    title = line[0]
    ac1 = line[17]
    ac2 = line[18]
    ac3 = line[19]
    ac4 = line[20]

    ac_list = [ac1, ac2, ac3, ac4]

    for ac in ac_list:
        if ac != '':
            if ac not in actor_name_link:
                print(title, ac)