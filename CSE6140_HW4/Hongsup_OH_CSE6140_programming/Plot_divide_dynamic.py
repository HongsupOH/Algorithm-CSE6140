import numpy as np
import matplotlib.pyplot as plt

#the number of k
k = [10,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
#Divide and Conquer
dc = [0.168,43.55,68.7,103.64,132,159,200,224,269.1,275.8,328]
#Dynamic Programming
dp = [0.048,10.554,18.889,29.50,32.329,36.6,38.2,46.3,52.4,54.6,71]

#Plot Graph
plt.plot(k,dc,label = 'Divide and Conquer')
plt.plot(k,dp,label = 'Dynamic Programming')
plt.legend()
plt.xlabel('The number of k',fontsize = 20)
plt.ylabel('Time (millisecons)',fontsize = 20)
plt.title('Divide and Conquer VS Dynamic Programming',fontsize = 20)
plt.grid()
plt.show()


