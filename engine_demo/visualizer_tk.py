import tkinter as tk
import math

class EngineVisualizerTk:
    def __init__(self, root, engine, x=20, y=20, size=300, min_temp=20, max_temp=120):
        self.engine = engine
        self.x = x
        self.y = y
        self.size = size
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.canvas = tk.Canvas(root, width=size+40, height=size+80, bg='white')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

    def draw(self, highlight=False):
        self.canvas.delete('all')
        cx = self.size//2 + 20
        cy = self.size//2 + 40
        r = self.size//2
        # Draw gauge background
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='#eee', outline='blue' if highlight else 'black', width=3 if highlight else 1)
        # Draw power arc (270 deg)
        self._draw_arc(cx, cy, r-20, 135, 405, width=20, color='#fff')
        # Draw power needle
        angle = 135 + 270 * self.engine.power
        self._draw_needle(cx, cy, r-40, angle, color='red', width=5)
        # Draw temperature arc
        temp_pct = (self.engine.temp - self.min_temp) / (self.max_temp - self.min_temp)
        temp_pct = max(0, min(1, temp_pct))
        temp_angle = 135 + 270 * temp_pct
        self._draw_arc(cx, cy, r, 135, temp_angle, width=10, color='orange')
        # Draw labels
        self.canvas.create_text(cx, cy+30, text=f"{self.engine.name}", font=('Arial', 16, 'bold'))
        self.canvas.create_text(cx, cy-20, text=f"Power: {int(self.engine.power*100)}%", font=('Arial', 12))
        self.canvas.create_text(cx, cy+60, text=f"Temp: {self.engine.temp:.1f}°C", font=('Arial', 12))

    def _draw_arc(self, cx, cy, r, start_deg, end_deg, width=10, color='orange'):
        # Tkinter's create_arc uses angles in degrees, starting at 0 (east) and increasing counterclockwise
        extent = end_deg - start_deg
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start_deg, extent=extent, style=tk.ARC, outline=color, width=width)

    def _draw_needle(self, cx, cy, length, angle_deg, color='red', width=3):
        angle_rad = math.radians(angle_deg)
        x = cx + length * math.cos(angle_rad)
        y = cy + length * math.sin(angle_rad)
        self.canvas.create_line(cx, cy, x, y, fill=color, width=width)
