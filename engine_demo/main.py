import tkinter as tk
from engine import Engine
from visualizer_tk import EngineVisualizerTk

# Simulation parameters
outside_temp = 25.0
engines = [
    Engine(name=f"Engine {i+1}", power=0.0, temp=30.0, heat_gen_coeff=8.0, heat_rej_coeff=0.05) for i in range(1)
]


dt = 0.1  # seconds per frame
base_power_rate = 0.1  # power per second at full key press rate
def get_power_step():
    return base_power_rate * dt

current_engine_idx = 0

root = tk.Tk()
root.title("Engine Temperature Visualizer")

visualizers = [EngineVisualizerTk(root, engine, x=40+i*340, y=40, size=400) for i, engine in enumerate(engines)]

def update():
    for engine in engines:
        engine.update(outside_temp, dt=dt)
    for i, vis in enumerate(visualizers):
        vis.draw(highlight=(i==current_engine_idx))
    root.after(int(dt*1000), update)

def on_key(event):
    global current_engine_idx
    power_step = get_power_step()
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
