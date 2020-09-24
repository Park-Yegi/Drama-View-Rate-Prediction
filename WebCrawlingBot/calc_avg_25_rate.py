import csv

kbs_mini = open('../kbs_mini.csv', 'r', encoding='utf-8')
# each_ep = open('../kbs_each_ep.csv','r',encoding='utf-8')

mini_rdr = csv.reader(kbs_mini)
# ep_rdr = csv.reader(each_ep)

for line in mini_rdr:

    try:
        rate_list = []
        drama_name = line[0]
        num_eps = int(line[5])
        num_25 = int(num_eps/4)
    
        each_ep = open('../kbs_each_ep.csv','r',encoding='utf-8')
        ep_rdr = csv.reader(each_ep)
        for ep in ep_rdr:

            if ep[0] == drama_name:
                rate_list.append(float(ep[2]))

        # print(rate_list)
        first_rate = rate_list[-1]
        avg_rate = sum(rate_list)/num_eps
        rate_25 = sum(rate_list[:num_25])/num_25

        print(drama_name, first_rate,',',avg_rate,',',rate_25)

        if num_eps != len(rate_list):
            print("다름!!!!")
    except Exception as e:
        print(e)