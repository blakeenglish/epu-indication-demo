import tkinter as tk
from engine import Engine
from visualizer_tk import EngineVisualizerTk

# Simulation parameters
outside_temp = 25.0
engines = [
    Engine(name=f"Engine {i+1}", power=0.5, temp=40.0, heat_gen_coeff=5.0, heat_rej_coeff=1) for i in range(2)
]

power_step = 0.05
current_engine_idx = 0

root = tk.Tk()
root.title("Engine Temperature Visualizer")

visualizers = [EngineVisualizerTk(root, engine, x=20+i*340, y=20, size=300) for i, engine in enumerate(engines)]

def update():
    for engine in engines:
        engine.update(outside_temp, dt=0.1)
    for i, vis in enumerate(visualizers):
        vis.draw(highlight=(i==current_engine_idx))
    root.after(100, update)

def on_key(event):
    global current_engine_idx
    if event.keysym == 'Up':
        engines[current_engine_idx].set_power(engines[current_engine_idx].power + power_step)
    elif event.keysym == 'Down':
        engines[current_engine_idx].set_power(engines[current_engine_idx].power - power_step)
    elif event.keysym == 'Right':
        current_engine_idx = (current_engine_idx + 1) % len(engines)
    elif event.keysym == 'Left':
        current_engine_idx = (current_engine_idx - 1) % len(engines)

root.bind('<Key>', on_key)
update()
root.mainloop()
