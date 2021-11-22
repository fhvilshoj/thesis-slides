import numpy as np

svg_points = np.array([
    [530,    86],
    [106,    213]
])

real_points = np.array([
    # Params, accuracy
    [829,     97.6],
    [60 ,     84.6]
]) 

x1, x2 = svg_points[:,0]
y1, y2 = real_points[:,0]
x_a = (y2 - y1) / (x2 - x1)
x_b = y1 - x_a * x1

x_to_x = lambda x: x_a * x + x_b

x1, x2 = svg_points[:,1]
y1, y2 = real_points[:,1]
y_a = (y2 - y1) / (x2 - x1)
y_b = y1 - y_a * x1

y_to_y = lambda y: y_a * y + y_b

with open( 'param_data.csv', 'r') as f:
    # to_plot = [l.strip().split(',') for l in f if l]
    to_plot = [l.strip().split(',') for l in f if len(l) > 0]
    to_plot = [(int(x), int(y)) for x, y  in to_plot]

to_plot = np.array([(x_to_x(x), y_to_y(y)) for x, y in to_plot])
# to_plot = to_plot[np.argsort(to_plot[:,0])]

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(*to_plot.T)
ax.set_xscale('log')

ax.set_title("ImageNet Top-5 accuracy") 
ax.set_xlabel('#Paramteres')
ax.set_ylabel('Top-5 accuracy')

fig.tight_layout()
fig.savefig('param-chart.svg', bbox_inches='tight')


