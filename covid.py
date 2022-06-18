import requests

class CovidMap:
    # 建構式
    def __init__(self,city:str):
        self.city = city
        self.url = 'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5002&limited={}'.format(self.city)
        self.dist = None
        self.data = None
    def set_city(self,city:str):
        self.city = city
        self.data = self.get_all_data()
    def get_all_data(self):
        r = requests.get(self.url)
        self.data = r.json()
        return self.data

    def get_url(self):
        return self.url

    def get_all_dist_data(self):
        for i in range(1,12):
            print(self.data[i])
    
    def get_dist_data(self,dist:str):
        dist_num = 0
        #從第二筆資料(第一個行政區)開始
        i=2
        #計算縣市行政區數量
        while(True):
            temp = self.data[1]['a04']
            if temp == self.data[i]['a04']:
                dist_num = i-2
                break
            i+=1
        #透過上面算出的行政區數量撈出指定的行政區數據
        for i in range(dist_num):
            if self.data[i]['a04']==dist:
                return self.data[i]
        




