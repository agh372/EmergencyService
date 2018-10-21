import time
import random
import threading


def draw_nodes(grid, canvas, xd, yd, xd_start, yd_start, node_diameter, edge_distance):
    rects = []
    traffic_lights = []
    for i in range(grid.N):
        row_rects = []
        row_lights = []
        for j in range(grid.N):
            rect = canvas.create_rectangle(xd, yd, xd + node_diameter, yd + node_diameter, fill='red')
            row_rects.append(rect)
            row_lights.append(draw_traffic_lights(grid, i, j, canvas, rect, node_diameter))
            xd += edge_distance
        yd += edge_distance
        xd = xd_start
        rects.append(row_rects)
        traffic_lights.append(row_lights)

    return rects, traffic_lights


def draw_edge(grid, src, dest, canvas, rects, edges, edge_thickness, edge_texts, text_buffer):
    if grid.adjacency[src][dest] is not None:
        src_i = int(src/grid.N)
        src_j = src% grid.N
        dest_i = int(dest/ grid.N)
        dest_j = dest% grid.N

        src_rect = rects[src_i][src_j]
        dest_rect = rects[dest_i][dest_j]

        src_coords = canvas.coords(src_rect)
        dest_coords = canvas.coords(dest_rect)

        if src >= dest:
            if src_i == dest_i:
                edge_texts[src][dest] = canvas.create_text(src_coords[0] - text_buffer, src_coords[1] - text_buffer,
                                                           fill="white", text=str(grid.adjacency[src][dest].weight))
                edges[src][dest] = canvas.create_rectangle(src_coords[0], src_coords[1],
                                                       dest_coords[2], dest_coords[1] + edge_thickness, fill='white')
            elif src_j == dest_j:
                edge_texts[src][dest] = canvas.create_text(src_coords[2] + text_buffer, src_coords[1] - text_buffer,
                                                           fill="white", text=str(grid.adjacency[src][dest].weight))
                edges[src][dest] = canvas.create_rectangle(src_coords[2] - edge_thickness, src_coords[1],
                                                       dest_coords[2], dest_coords[3], fill='white')

        elif src < dest:
            if src_i == dest_i:
                edge_texts[src][dest] = canvas.create_text(src_coords[2] + text_buffer, src_coords[3] + text_buffer,
                                                           fill="white", text=str(grid.adjacency[src][dest].weight))
                edges[src][dest] = canvas.create_rectangle(src_coords[2], src_coords[3] - edge_thickness,
                                                           dest_coords[0], dest_coords[3], fill='white')
            elif src_j == dest_j:
                edge_texts[src][dest] = canvas.create_text(src_coords[0] - text_buffer, src_coords[3] + text_buffer,
                                                           fill="white", text=str(grid.adjacency[src][dest].weight))
                edges[src][dest] = canvas.create_rectangle(src_coords[0], src_coords[3],
                                                       dest_coords[0] + edge_thickness, dest_coords[1], fill='white')



def draw_traffic_lights(grid, node_i, node_j, canvas, rect, node_diameter):
    rect_coords = canvas.coords(rect)
    lights = []
    for i in range(4):
        fillcolor = "red"
        if grid.nodes[node_i][node_j].lights[i] == 0:
            fillcolor = "red"
        else:
            fillcolor = "green"
        if i == 0:
            lights.append(canvas.create_rectangle(rect_coords[0], rect_coords[1],
                                                  rect_coords[0] + node_diameter/2, rect_coords[1] + node_diameter/2, fill=fillcolor))
        elif i == 1:
            lights.append(canvas.create_rectangle(rect_coords[0] + node_diameter/2, rect_coords[1],
                                                  rect_coords[2], rect_coords[1] + node_diameter/2, fill=fillcolor))
        elif i == 2:
            lights.append(canvas.create_rectangle(rect_coords[0] + node_diameter/2, rect_coords[1] + node_diameter/2,
                                                  rect_coords[2], rect_coords[3], fill=fillcolor))
        elif i == 3:
            lights.append(canvas.create_rectangle(rect_coords[0], rect_coords[1] + node_diameter/2,
                                                  rect_coords[0] + node_diameter/2, rect_coords[3], fill=fillcolor))
    return lights


def traffic_light_green(grid, node_i, node_j, light_no, gui, canvas, blob, rects, traffic_lights, threshold, sleeptime):
    grid.nodes[node_i][node_j].lights = [0, 0, 0, 0]
    grid.nodes[node_i][node_j].lights[light_no] = 1
    for i in range(4):
        if grid.nodes[node_i][node_j].lights[i] == 0:
            fillcolor = "red"
        else:
            fillcolor = "green"
        canvas.itemconfig(traffic_lights[node_i][node_j][i], fill=fillcolor)
        gui.update()

def simulate_movement(grid, gui, canvas, node_diameter, blob_diameter, rects, traffic_lights, path, colors, threshold):
    start_src = path[0]
    start_src_i = int(start_src / grid.N)
    start_src_j = start_src % grid.N
    start_src_coords = canvas.coords(rects[start_src_i][start_src_j])

    # Initiating blob in the center of the source node

    colorcode = random.randint(0, len(colors)-1)

    blob = canvas.create_oval(int(start_src_coords[0] + node_diameter/2 - blob_diameter/2),
                              int(start_src_coords[1] + node_diameter/2 - blob_diameter/2),
                              int(start_src_coords[2] - node_diameter/2 + blob_diameter/2),
                              int(start_src_coords[3] - node_diameter/2 + blob_diameter/2),
                              fill=colors[colorcode])
    gui.update()
    for i in range(len(path) - 1):
        src = path[i]
        dest = path[i+1]

        src_i = int(src/ grid.N)
        src_j = src% grid.N
        dest_i = int(dest/ grid.N)
        dest_j = dest% grid.N

        src_rect = rects[src_i][src_j]
        dest_rect = rects[dest_i][dest_j]

        src_coords = canvas.coords(src_rect)
        dest_coords = canvas.coords(dest_rect)

        sleeptime = grid.adjacency[src][dest].weight/100

        if src < dest:
            if src_i == dest_i:
                blob_coords = canvas.coords(blob)

                if blob_coords[0] > src_coords[2] - blob_diameter:
                    while blob_coords[0] > src_coords[2] - blob_diameter:
                        canvas.move(blob,-1,0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[0] < src_coords[2] - blob_diameter:
                        canvas.move(blob,1,0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)

                if blob_coords[1] > src_coords[3] - blob_diameter:
                    while blob_coords[1] > src_coords[3] - blob_diameter:
                        canvas.move(blob,0,-1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[1] < src_coords[3] - blob_diameter:
                        canvas.move(blob,0,1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)

                canvas.coords(blob, src_coords[2] - blob_diameter, src_coords[3] - blob_diameter,
                              src_coords[2], src_coords[3])
                gui.update()
                while blob_coords[0] < dest_coords[0]:
                    if dest_coords[0] - blob_coords[0] <= threshold:
                        traffic_light_green(grid, dest_i, dest_j, 3, gui, canvas, blob, rects, traffic_lights,
                                                                 threshold, sleeptime)
                    canvas.move(blob,1,0)
                    gui.update()
                    blob_coords = canvas.coords(blob)
                    time.sleep(sleeptime)

            elif src_j == dest_j:
                blob_coords = canvas.coords(blob)

                if blob_coords[0] > src_coords[0]:
                    while blob_coords[0] > src_coords[0]:
                        canvas.move(blob, -1, 0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[0] < src_coords[0]:
                        canvas.move(blob, 1, 0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)

                if blob_coords[1] > src_coords[3]:
                    while blob_coords[1] > src_coords[3]:
                        canvas.move(blob, 0, -1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[1] < src_coords[3]:
                        canvas.move(blob, 0, 1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                canvas.coords(blob, src_coords[0], src_coords[3],
                              src_coords[0] + blob_diameter, src_coords[3] + blob_diameter)
                gui.update()
                while blob_coords[1] < dest_coords[1]:
                    if dest_coords[1] - blob_coords[1] <= threshold:
                        traffic_light_green(grid, dest_i, dest_j, 0, gui, canvas, blob, rects, traffic_lights,
                                                                 threshold, sleeptime)
                    canvas.move(blob,0,1)
                    gui.update()
                    blob_coords = canvas.coords(blob)
                    time.sleep(sleeptime)

        elif src >= dest:
            if src_i == dest_i:
                blob_coords = canvas.coords(blob)

                if blob_coords[0] > src_coords[0]:
                    while blob_coords[0] > src_coords[0]:
                        canvas.move(blob, -1, 0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[0] < src_coords[0]:
                        canvas.move(blob, 1, 0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)

                if blob_coords[1] > src_coords[1]:
                    while blob_coords[1] > src_coords[1]:
                        canvas.move(blob, 0, -1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[1] < src_coords[1]:
                        canvas.move(blob, 0, 1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                canvas.coords(blob, src_coords[0], src_coords[1],
                              src_coords[0] - blob_diameter, src_coords[1] + blob_diameter)
                blob_coords = canvas.coords(blob)
                gui.update()
                while blob_coords[2] > dest_coords[2]:
                    if blob_coords[2] - dest_coords[2] <= threshold:
                        traffic_light_green(grid, dest_i, dest_j, 2, gui, canvas, blob, rects, traffic_lights,
                                                                 threshold, sleeptime)
                    canvas.move(blob,-1,0)
                    gui.update()
                    blob_coords = canvas.coords(blob)
                    time.sleep(sleeptime)

            elif src_j == dest_j:
                blob_coords = canvas.coords(blob)

                if blob_coords[0] > src_coords[2] - blob_diameter:
                    while blob_coords[0] > src_coords[2] - blob_diameter:
                        canvas.move(blob, -1, 0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[0] < src_coords[2] - blob_diameter:
                        canvas.move(blob, 1, 0)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)

                if blob_coords[1] > src_coords[1]:
                    while blob_coords[1] > src_coords[1]:
                        canvas.move(blob, 0, -1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                else:
                    while blob_coords[1] < src_coords[1]:
                        canvas.move(blob, 0, 1)
                        time.sleep(sleeptime)
                        blob_coords = canvas.coords(blob)
                canvas.coords(blob, src_coords[2] - blob_diameter, src_coords[1],
                              src_coords[2], src_coords[1] + blob_diameter)
                blob_coords = canvas.coords(blob)
                gui.update()
                while blob_coords[3] > dest_coords[3]:
                    if blob_coords[3] - dest_coords[3] <= threshold:
                        traffic_light_green(grid, dest_i, dest_j, 2, gui, canvas, blob, rects, traffic_lights,
                                                                 threshold, sleeptime)
                    canvas.move(blob,0,-1)
                    gui.update()
                    blob_coords = canvas.coords(blob)
                    time.sleep(sleeptime)

            gui.update()
        i += 1
