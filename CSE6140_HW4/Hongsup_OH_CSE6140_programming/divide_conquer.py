#Divide and Conquer
import os
import time
from os import listdir
from os.path import isfile, join
import sys
import glob

#Divide and Conqeur algorithm
class divide_conquer(object):
    def __init__(self):
        self.day_arr = []
        self.data_files = []

    #def load_file_data(self,input_path):
    #    self.data_files = [f for f in listdir(input_path) if '.txt' in f and isfile(join(input_path, f))]

    def load_file_data(self):
        for element in glob.glob('*.txt'):
            self.data_files.append(element)
    
    def load_day_data(self,file_name):
        """
        file_name = "10.txt"
        """
        with open(file_name) as f:
            content = [line.strip('\n') for line in f.readlines()]
            temp = content[0].split(',')
            no_of_days, no_of_instances = int(temp[0]), int(temp[1])

            for i in range(1,no_of_instances+1,1):
                temp_days = content[i].split(',')
                days = [float(rate) for rate in temp_days]
                self.day_arr.append(days)
                 
    def maxCrossingSum(self,arr,l,m,h) :
        # Include elements on left of mid. 
        s_l = 0
        left_sum = float('-inf')
        for i in range(m,l-1,-1) :
            s_l = s_l + arr[i]
            if (s_l > left_sum): 
                left_sum = s_l
                start_ind =i
        # Include elements on right of mid 
        s_r = 0; right_sum = float('-inf')
        for i in range(m + 1, h + 1) :
            s_r = s_r + arr[i] 
            if (s_r > right_sum) : 
                right_sum = s_r
                end_ind = i
        # Return sum of elements on left and right of mid
        return left_sum + right_sum, start_ind+1, end_ind+1

    def max_sub_array(self,arr,l,h):
        if l == h:
            return arr[h], l,h
        m = (l+h)//2
        left_sum,left_start,left_end = self.max_sub_array(arr,l,m)
        right_sum,right_start,right_end = self.max_sub_array(arr,m+1,h)
        overlapping_sum, cross_start, cross_end = self.maxCrossingSum(arr,l,m,h)

        i,j,max_sum = 0,0,0

        if left_sum > right_sum:
            i = left_start
            j = left_end
            max_sum = left_sum
        else:
            i = right_start
            j = right_end
            max_sum = right_sum

        if overlapping_sum > max_sum:
            i = cross_start
            j = cross_end
            max_sum = overlapping_sum
        return max_sum,i,j

    def save_output(self,file_name,data):
        file_name = 'output_divide_conquer/HongsupOH_output_dc' + file_name
        with open(file_name,'w') as f:
            for i in range(len(data)):
                f.write(data[i])

                if i < len(data)-1:
                    f.write('\n')

    def run_dc(self):
        #path = os.path.join(os.path.dirname(__file__), 'data/')
        self.load_file_data()

        avg_arr = []
        for file in self.data_files:
            print("Loading data for file",file, "....")
            self.load_day_data(file)
            print("Finished loading data for file",file,"....")
            output = []

            print()
            print("Running DC Algorithm for file",file,"....")
            for day in self.day_arr:
                start_time = time.time() * 1000
                val,i,j = self.max_sub_array(day,0,len(day)-1)
                exec_time = (time.time() * 1000) - start_time
                val = "%.2f" % val
                exec_time = "%.2f" % exec_time

                out_str = val + ',' + str(i+1) + ',' + str(j+1) + ',' + exec_time
                output.append(out_str)

            print("Finished running DC Algorithm for file",file,"....")
            print()

            self.save_output(file,output)
            self.day_arr = []

if __name__ == '__main__':
    dc = divide_conquer()
    dc.run_dc()
