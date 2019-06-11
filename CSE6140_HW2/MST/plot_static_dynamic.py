import matplotlib.pyplot as plt
#node = [16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536]
edge = [64,128,259,530,1054,2183,4411,9875,29779,106361,372670,1770677,7926934]
#static = [1.0991,2.4633,5.8968,11.6398,26.609,59.406,142.754,306.767,756.387,2032.95,5199.08,23512.62]
#dynamic = [351,478,439.77,577.525,783.0817,1005.625,2799.8,2921.607,10761.21,13283.477, 30859.16, 53942.33]

static = [0.499,0.50067,1.00,2.5017,6.0198,10.524,26.51,46.53,152.11,433.389,1215.99,5534.684,31747]
dynamic = [49,55.55,66.60,108.6478,151.609,217.713,565.8705,639.97,2389.811,3792.199,7936.84,12482,12680]
dyna_avg = []
for i in range(len(dynamic)):
    dyna_avg.append(dynamic[i]/1000)

#static
plt.plot(edge,static)
plt.xlabel('the number of edge')
plt.ylabel('running time for static')
plt.grid()
plt.show()

#dynamic
plt.plot(edge,dynamic)
plt.xlabel('the number of edge')
plt.ylabel('total running time for dynamic')
plt.grid()
plt.show()

#avg_dynamic
plt.plot(edge,dyna_avg)
plt.xlabel('the number of edge')
plt.ylabel('average running time for dynamic')
plt.grid()
plt.show()
