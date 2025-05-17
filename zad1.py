import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(10, 8))
plt.subplots_adjust(top=0.9)
fig.suptitle('Custom 3D Mesh Animation', fontsize=16)
ax = fig.add_subplot(111, projection='3d')

vertices = np.array([
    [0, 0, 0],    
    [1, 0, 0],    
    [1, 1, 0],    
    [0, 1, 0],    
    [0.5, 0.5, 1]  
])

face_colors = [
    'red',      
    'green',    
    'blue',    
    'yellow',   
    'magenta', 
    'cyan'     
]

view_elev = 30
view_azim = 45

def on_rotate(event):
    global view_elev, view_azim
    if hasattr(ax, 'elev') and ax.elev is not None:
        view_elev = ax.elev
    if hasattr(ax, 'azim') and ax.azim is not None:
        view_azim = ax.azim

fig.canvas.mpl_connect('motion_notify_event', on_rotate)

def update(frame):
    global view_elev, view_azim
    
    current_elev = view_elev
    current_azim = view_azim
    
    ax.clear()
    
    animated_vertices = vertices.copy()
    factor = np.sin(frame * 0.1) * 0.5 + 1  
    animated_vertices[4, 2] = vertices[4, 2] * factor  
    
    faces = [
        [animated_vertices[0], animated_vertices[1], animated_vertices[4]],
        [animated_vertices[1], animated_vertices[2], animated_vertices[4]],
        [animated_vertices[2], animated_vertices[3], animated_vertices[4]],
        [animated_vertices[3], animated_vertices[0], animated_vertices[4]],
        [animated_vertices[0], animated_vertices[2], animated_vertices[1]],
        [animated_vertices[0], animated_vertices[3], animated_vertices[2]]
    ]
    
    poly = Poly3DCollection(faces, alpha = 0.8)
    poly.set_facecolor(face_colors)
    poly.set_edgecolor('black')
    
    ax.add_collection3d(poly)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.view_init(elev=current_elev, azim=current_azim)
    return poly,

ani = FuncAnimation(fig, update, frames=60, interval=100, blit=False)
plt.show()
