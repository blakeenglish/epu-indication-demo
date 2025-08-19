import tkinter as tk
import math

class EngineVisualizerTk:
    def __init__(self, root, engine, x=20, y=20, size=300):
        self.engine = engine
        self.x = x
        self.y = y
        self.size = size
        self.min_temp = self.engine.temperature_lower_redline
        self.max_temp = self.engine.temperature_upper_redline
        self.padding = 160
        self.canvas = tk.Canvas(root, width=size+self.padding, height=size+self.padding, bg='black')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

    def draw(self, highlight=False):
        self.canvas.delete('all')
        cx = self.size//2 + self.padding//2
        cy = self.size//2 + self.padding//2
        r = self.size//2

        total_arc_angle = 270
        temperature_arc_starting_angle_in_degrees = 225
        power_arc_starting_angle_in_degrees = 225
        # Draw gauge background
        #self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='black', outline='white' if highlight else 'white', width=3 if highlight else 1)
        # Draw power arc (270 deg)
        self._draw_arc(cx, cy, r-20, power_arc_starting_angle_in_degrees, power_arc_starting_angle_in_degrees + total_arc_angle, width=20, color='gray25')

        # Draw marker for takeoff temperature limit
        takeoff_temp = getattr(self.engine, 'takeoff_temperature_limit', None)
        if takeoff_temp is not None:
            temp_frac = self.engine.takeoff_temperature_limit / (self.engine.temperature_upper_redline - self.engine.temperature_lower_redline)
            #temp_frac = max(0.0, min(1.0, temp_frac))
            self.draw_temperature_marker(cx, cy, r, temperature_arc_starting_angle_in_degrees, total_arc_angle, temp_frac, color='white', name='T_VTO')
            
        # Draw marker for inverter 60 power
        #power_60 = getattr(self.engine, 'power_for_steady_state_temperature_for_inverter_60', None)
        #if power_60 is not None:
            # Compute the power fraction for steady-state at inverter 60
        power_frac = self.engine.power_ratio_for_steady_state_temperature_for_inverter_60
        #power_frac = max(0.0, min(1.0, power_frac))
        self.draw_power_marker(cx, cy, r, power_arc_starting_angle_in_degrees, total_arc_angle, power_frac, color='white', name='P_SS60')

        power_frac = self.engine.power_ratio_for_i_60
        #power_frac = max(0.0, min(1.0, power_frac))
        self.draw_power_marker(cx, cy, r, power_arc_starting_angle_in_degrees, total_arc_angle, power_frac, color='white', name='P_I60', inner_radius_offset=-50)

        temp_frac = self.engine.temperature_inverter_60 / (self.engine.temperature_upper_redline - self.engine.temperature_lower_redline)
            #temp_frac = max(0.0, min(1.0, temp_frac))
        self.draw_temperature_marker(cx, cy, r, temperature_arc_starting_angle_in_degrees, total_arc_angle, temp_frac, color='white', name='T_I60')

        power_frac = self.engine.power_ratio_for_vto_30
        #power_frac = max(0.0, min(1.0, power_frac))
        self.draw_power_marker(cx, cy, r, power_arc_starting_angle_in_degrees, total_arc_angle, power_frac, color='white', name='P_VTO_30')
        
        power_frac = self.engine.power_ratio_for_steady_state_temperature_for_upper_redline
        #power_frac = max(0.0, min(1.0, power_frac))
        self.draw_power_marker(cx, cy, r, power_arc_starting_angle_in_degrees, total_arc_angle, power_frac, color='white', name='P_SSMax')

        temp_frac = self.engine.trend_temperature / (self.engine.temperature_upper_redline - self.engine.temperature_lower_redline)
            #temp_frac = max(0.0, min(1.0, temp_frac))
            
        trend_mark_color = 'green2'
        if self.engine.trend_temperature > self.max_temp * 0.95:
            trend_mark_color = 'red'
        elif self.engine.trend_temperature < self.engine.temperature_inverter_60:
            trend_mark_color = 'green2'
        else:
            trend_mark_color = 'yellow'

        self.draw_temperature_marker(cx, cy, r, temperature_arc_starting_angle_in_degrees, total_arc_angle, temp_frac, color=trend_mark_color, name='5s')
        
        self.draw_temperature_marker(cx, cy, r, temperature_arc_starting_angle_in_degrees, total_arc_angle, 1.0, color='red', name='')

        # Draw power needle
        angle = power_arc_starting_angle_in_degrees + total_arc_angle * self.engine.power
        self._draw_needle(cx, cy, r-40, angle, color='white', width=5)
        # Draw temperature arc
        temp_pct = (self.engine.temp - self.min_temp) / (self.max_temp - self.min_temp)
        temp_angle = temperature_arc_starting_angle_in_degrees + total_arc_angle * temp_pct
        if self.engine.temp > self.max_temp * 0.95:
            arc_color = 'red'
            self.draw_arrow(cx, cy, r*0.75, 45, 'red', -45, 40, 16)
        elif self.engine.temp < self.engine.temperature_inverter_60:
            arc_color = 'green2'
        else:
            arc_color = 'yellow'
            #self.draw_arrow(self, cx, cy, 30, 90, 'orange', 0, 20, 8)
            self.draw_arrow(cx, cy, r*0.75, 65, 'yellow', -(90-65+5), 40, 16)
            self.draw_arrow(cx, cy, r*0.75, 45, 'yellow', -(90-45+5), 40, 16)
            self.draw_arrow(cx, cy, r*0.75, 25, 'yellow', -(90-25+5), 40, 16)

        self._draw_arc(cx, cy, r, temperature_arc_starting_angle_in_degrees, temp_angle, width=10, color=arc_color)
        # Draw labels
        self.canvas.create_text(cx, cy+100, text=f"{self.engine.name}", font=('Arial', 16, 'bold'), fill='white')
        self.canvas.create_text(cx, cy+70, text=f"Avg Power: {int(self.engine.power*100)}%", font=('Arial', 12), fill='white')
        self.canvas.create_text(cx, cy+130, text=f"Max Temp: {self.engine.temp:.1f}%", font=('Arial', 12), fill='white')
        #self.canvas.create_text(cx, cy+80, text=f"Power 60: {self.engine.power_ratio_for_steady_state_temperature_for_inverter_60:.1f}%", font=('Arial', 12), fill='white')

    def draw_power_marker(self, cx, cy, r, arc_start_deg, arc_total_angle, power_frac, color='blue', name=None, inner_radius_offset = -32):
        """
        Draw a perpendicular marker line on the power arc at the given power fraction (0-1).
        Optionally label it with 'name'.
        """
        angle = arc_start_deg + arc_total_angle * power_frac
        angle_rad = math.radians(angle-90)
        inner = r + inner_radius_offset
        outer = r-8
        x0 = cx + inner * math.cos(angle_rad)
        y0 = cy + inner * math.sin(angle_rad)
        x1 = cx + outer * math.cos(angle_rad)
        y1 = cy + outer * math.sin(angle_rad)
        self.canvas.create_line(x0, y0, x1, y1, fill=color, width=3)
        if name:
            # Place label closer to the arc center
            label_x = cx + (inner - 30) * math.cos(angle_rad)
            label_y = cy + (inner - 30) * math.sin(angle_rad)
            self.canvas.create_text(label_x, label_y, text=name, fill=color, font=('Arial', 10, 'bold'))
        
    def draw_temperature_marker(self, cx, cy, r, arc_start_deg, arc_total_angle, temp_frac, color='purple', name=None):
        """
        Draw a perpendicular marker line on the temperature arc at the given temperature fraction (0-1).
        This marker is radially farther from the center than the power marker.
        Optionally label it with 'name'.
        """
        angle = arc_start_deg + arc_total_angle * temp_frac
        angle_rad = math.radians(angle-90)
        inner = r + 8
        outer = r + 32
        x0 = cx + inner * math.cos(angle_rad)
        y0 = cy + inner * math.sin(angle_rad)
        x1 = cx + outer * math.cos(angle_rad)
        y1 = cy + outer * math.sin(angle_rad)
        self.canvas.create_line(x0, y0, x1, y1, fill=color, width=3)
        if name:
            label_x = cx + (outer+10) * math.cos(angle_rad)
            label_y = cy + (outer+10) * math.sin(angle_rad)
            self.canvas.create_text(label_x, label_y, text=name, fill=color, font=('Arial', 10, 'bold'))
        
    def _draw_arc(self, cx, cy, r, start_deg, end_deg, width=10, color='orange'):
        # Redefine 0 deg as up, increasing clockwise, 90 deg is right
        # Tkinter's 0 deg is east (right), increasing counterclockwise
        def to_tk_angle(deg):
            return ((360 - (deg-90))) % 360

        tk_start = to_tk_angle(start_deg)
        tk_end = to_tk_angle(end_deg)
        # Calculate extent for clockwise arc
        extent = (tk_end - tk_start) % 360
        if extent > 0:
            extent = extent - 360  # Make negative for clockwise

        self.canvas.create_arc(
            cx - r, cy - r, cx + r, cy + r,
            start=tk_start,
            extent=extent,
            style=tk.ARC,
            outline=color,
            width=width
        )

    def _draw_needle(self, cx, cy, length, angle_deg, color='red', width=3):
        angle_rad = math.radians(angle_deg-90)
        x = cx + length * math.cos(angle_rad)
        y = cy + length * math.sin(angle_rad)
        self.canvas.create_line(cx, cy, x, y, fill=color, width=width)

    def draw_arrow(self, cx, cy, base_radius, base_angle_deg, arrow_color, arrow_angle_deg, length, width):
        """
        Draw a small arrow on the gauge.
        cx, cy: center of gauge
        base_radius: distance from center to base of arrow
        base_angle_deg: angle (degrees, 0=up, increases clockwise) for base location
        arrow_color: color of the arrow
        arrow_angle_deg: orientation of the arrow (degrees, 0=up, increases clockwise)
        length: length of the arrow
        width: width of the arrow head
        """
        # Compute base point
        base_angle_rad = math.radians(base_angle_deg - 90)
        bx = cx + base_radius * math.cos(base_angle_rad)
        by = cy + base_radius * math.sin(base_angle_rad)
        # Arrow direction
        arrow_angle_rad = math.radians(arrow_angle_deg - 90)
        # Tip of arrow
        tx = bx + length * math.cos(arrow_angle_rad)
        ty = by + length * math.sin(arrow_angle_rad)
        # Arrowhead points
        left_angle = arrow_angle_rad + math.radians(150)
        right_angle = arrow_angle_rad - math.radians(150)
        lx = tx + width * math.cos(left_angle)
        ly = ty + width * math.sin(left_angle)
        rx = tx + width * math.cos(right_angle)
        ry = ty + width * math.sin(right_angle)
        # Draw main line
        self.canvas.create_line(bx, by, tx, ty, fill=arrow_color, width=3)
        # Draw arrowhead
        self.canvas.create_polygon([tx, ty, lx, ly, rx, ry], fill=arrow_color)
