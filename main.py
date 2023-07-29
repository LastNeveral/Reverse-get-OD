import pandas as pd
import numpy as np
from scipy import stats

class Reverse_OD():
    def __init__(self,mu,num_station, get_in, get_out):
        self.num_station = num_station
        self.O_list = list(range(1,num_station))
        self.D_list = list(range(2,num_station+1))
        self.get_in = [0]+get_in
        self.get_out = [0]+get_out
        self.Dataframe = pd.DataFrame(np.zeros((num_station-1,num_station-1)), index= self.O_list, columns = self.D_list)
        self.poisson_frame =[0]+[stats.poisson.pmf(i,mu) for i in range(1,num_station)]

    def calculation(self):
        Y = self.get_in.copy()
        for j in range(2, self.num_station+1):
            list1 = [Y[k] * self.poisson_frame[j - k] for k in range(1, j)]
            syp = sum(list1)
            if self.get_out[j] == 1:
                nn = list1.index(max(list1))+1
                i = nn
                self.Dataframe.loc[i, j] = 1
                Y[i] = Y[i] - 1
            else:
                for i in range(1, j):
                    ff = round((self.get_out[j] * Y[i] * self.poisson_frame[j - i]) / syp)
                    if ff < Y[i]:
                        self.Dataframe.loc[i, j] = ff
                        Y[i] = Y[i] - ff
                    else:
                        self.Dataframe.loc[i, j] = Y[i]
                        Y[i] = 0
        return

if __name__ =="__main__":
    maxN = 16
    get_in = [36,25,30,38,10,3,4,6,4,10,2,11,7,5,1,0]
    get_out = [0,1,2,1,3,5,7,5,16,8,4,23,27,42,16,32]
    mu = 6 # this is a question,because you need plenty of local data to ensure it is right.
    Reverse_OD1 = Reverse_OD(mu, maxN, get_in, get_out)
    Reverse_OD1.calculation()
    print(Reverse_OD1.Dataframe)