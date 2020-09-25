###### ALL FEATURES                             -> VECTOR ######
# start_date 'yyyy-mm-dd'                       -> pandas Datetime
# day "월,화"/"수,목"/금/"금,토"/"토,일"/일(6종류)    -> one hot encoding
# time 'hh:mm:00'                               -> float (hh + (mm/60))
## 10:10/20:55/21:15/21:30/21:40/21:50/21:55/22:00/22:15/22:45/23:00 11종류 밖에 없는데 categorical data로 해서 one hot encoding할까?
# num_eps(number of episodes) int               -> int
# prev(선행드라마)                                 -> 후반기 25% 시청률, 결측치는 k nearest neighbor 이용
# kbs (1 or 2)                                  -> one hot encoding

# news_keyword 0~9                              -> 방영 전 네이버 연예뉴스를 dataset으로 word2vec을 통해 드라마 제목과 코사인유사도가 높은 단어 10개의 벡터
# pd (min=1, max=3) 
# 해당 드라마가 방영되기 이전까지의 이력을 이용하여 과거에 연출했던 드라마 중 최고 시청률이 20% 이상(지상파 외 채널 2% 이상)인 드라마의 수를 기록
# writer (min=1, max=3) 
# 해당 드라마가 방영되기 이전까지의 이력을 이용하여 과거에 연출했던 드라마 중 최고 시청률이 20% 이상(지상파 외 채널 2% 이상)인 드라마의 수를 기록
# actor1,2,3,4,5 (min=2, max=5)
    # 5가지의 기준을 두었다. 
    # 첫 번째와 두 번째 기준은 각각 해당 드라마 이전에 출연한 방송(드라마 및 예능과 같은 TV 브라운관에서의 방송활동)과 영화의 수이다. 
    # 세 번째 기준은 수상 경력으로, 각종 시상식을 비롯하여 각 방송사에서 매년 주최하는 연말 시상식에서 수상한 상의 개수를 점수
    # 화하였다. 이 때 대상, 최우수·우수 연기상, 그 외의 상에 대하여 각각 3, 2, 1로 가중치를 주었다. 
    # 네 번째 기준은 역대 한국 드라마 시청률 100위 안에 드는 드라마에 주연으로 출연한 횟수이다.
    # 다섯 번째 기준은 해당 드라마의 주연배우 수이며 앞선 4가지 변수는 모두 주연배우의 수로 나눈 평균 점수를 사용
    # 드라마 출연 배우 , 프로듀서 , 작가의 해당 작품 전 5 년간으로 제한을 두어 평균 시청률을 변수화




###### MORE FEATURES? ######
# 네이버에서 제공하는 인터넷 기사를 기준으로 드라마 방영 전 날부터 3개월 이전까지, 방영한 날부터 1주일 이후까지의 기사 개수
# 드라마 검색량 (네이버 트렌드)
# 경쟁작의 시청률
# 원작이 있는 경우 1, 없는 경우 0을 나타내는 원작 유무 변수를 고려


#### 보정
# 연출자, 작가 변수 사이에서는 명확한 선형관계가 나타ㄴ나지 않아 GMM(Gaussian Mixture Model)을 이용하여 군집분석을 수행
# 드라마의 편성시간대를 나타내는 방송요일과 방송시간 모두 평균 시청률을 기준으로 하여 비슷한 값을 나타내는 범주들은 동일 범주로 묶었다

### 초반시청률 예측의 중요 변수: 방송시간, 방송사, 이전작의 평균 시청률, 방영 전 드라마 검색량
                        # 선행드라마 후반기 25% 시청률, 방송사, 방송요일, 방송시간, 프로듀서, 배우, 부작수
# 이 중 나한테 없는 데이터: 이전작의 평균 시청률/선행드라마 후반기 25% 시청률, 방영 전 드라마 검색량


import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

pd.set_option('display.max_rows', 160)
pd.set_option('display.max_columns', 20)

def embedding(file_path):
    kbs_mini = pd.read_csv(file_path, encoding='utf-8')
    del kbs_mini['end_date']
    del kbs_mini['pd']
    del kbs_mini['writer']
    del kbs_mini['actor1']
    del kbs_mini['actor2']
    del kbs_mini['actor3']
    del kbs_mini['actor4']
    del kbs_mini['actor5']
    del kbs_mini['avg_rate']
    del kbs_mini['rate_25']
    del kbs_mini['prev']

    start_timestamp = pd.to_datetime(kbs_mini['start_date'], format='%Y-%m-%d').astype(int) / 10**11
    kbs_mini['start_date'] = start_timestamp

    time_to_datetime = pd.to_datetime(kbs_mini['time'], format='%H:%M:%S')
    kbs_mini['time'] = time_to_datetime.dt.hour + (time_to_datetime.dt.minute/60)

    day_one_enc = pd.get_dummies(kbs_mini, columns=['day'])
    kbs_mini = day_one_enc

    # # print(kbs_mini['kbs'])
    kbs_mini = pd.get_dummies(kbs_mini, columns=['kbs'])

    del kbs_mini['title']
    
    # column_names = kbs_mini.columns.values.tolist()
    imp_mean = IterativeImputer(missing_values=np.nan, skip_complete=True, random_state=0)
    imputed_prev_25 = imp_mean.fit_transform(kbs_mini.to_numpy())[:, 4]
    kbs_mini['prev_25_imputed'] = imputed_prev_25
    # kbs_mini = pd.DataFrame(imp_mean.fit_transform(kbs_mini.to_numpy()), columns=column_names)
    del kbs_mini['prev_25']

    # print(kbs_mini.loc[:,['prev_25','prev_25_imputed']])
    return kbs_mini
    # print(kbs_mini)

# embedding('../kbs_mini.csv')