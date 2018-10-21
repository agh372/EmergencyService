from trafficDraw import *
from CityGrid import *
import tkinter as tk

N = 10
edge_distance = 70
node_diameter = 30
xd_start = 30
yd_start = 30
edge_thickness = 7
blob_diameter = 10

path1 = [0, 1, 2, 12, 13, 23]
path2 = [20, 10, 11, 12, 13, 3]

colors = ['SlateBlue1', 'SlateBlue2', 'SlateBlue3',
          'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4']

c_h = N*edge_distance + 2*yd_start + node_diameter
c_w = N*edge_distance + 2*xd_start + node_diameter

gui = tk.Tk()
gui.geometry(str(c_w)+"x"+str(c_h))
canvas = tk.Canvas(gui, width=c_w, height=c_h, background="black")
canvas.pack()
gui.title("City Grid")

xd = xd_start
yd = yd_start

edges = [[None for j in range(N*N)]for i in range(N*N)]
edge_texts = [[None for j in range(N*N)]for i in range(N*N)]
text_buffer = 10
text_font = "Times 10"
grid = Grid(N)
grid.create_graph()
grid.shortest_path(0, 5)

rects, traffic_lights = draw_nodes(grid, canvas, xd, yd, xd_start, yd_start, node_diameter, edge_distance)

for i in range(N*N):
    for j in range(N*N):
        draw_edge(grid, i, j, canvas, rects, edges, edge_thickness, edge_texts, text_buffer)
gui.update()

simulate_movement(grid, gui, canvas, node_diameter, blob_diameter, rects, traffic_lights, path1, colors, 10)
simulate_movement(grid, gui, canvas, node_diameter, blob_diameter, rects, traffic_lights, path2, colors, 10)

gui.mainloop()