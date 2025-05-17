import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
import time

fig = plt.figure(figsize=(10, 8))
plt.subplots_adjust(top=0.9)  
fig.suptitle('Animated Breathing Surface', fontsize=16)
ax = fig.add_subplot(111, projection='3d')

grid_size = 20
x = np.linspace(-1, 1, grid_size)
y = np.linspace(-1, 1, grid_size)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X) 

vertices = np.vstack([X.flatten(), Y.flatten(), Z.flatten()]).T

triangles = []
for i in range(grid_size - 1):
    for j in range(grid_size - 1):
        p1 = i * grid_size + j
        p2 = i * grid_size + j + 1
        p3 = (i + 1) * grid_size + j + 1
        p4 = (i + 1) * grid_size + j
        triangles.append([p1, p2, p3])
        triangles.append([p1, p3, p4])
triangles = np.array(triangles)

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
    
    t = frame / 10.0
    amplitude = 0.3
    freq1, freq2 = 2.0, 3.0
    
    Z = amplitude * np.sin(freq1 * X + t) * np.cos(freq2 * Y + t)
    
    vertices_new = np.vstack([X.flatten(), Y.flatten(), Z.flatten()]).T
    
    z_min, z_max = Z.min(), Z.max()
    z_normalized = (Z - z_min) / (z_max - z_min + 1e-8)
    
    colors = np.zeros((vertices_new.shape[0], 3))
    for i in range(len(vertices_new)):
        z_value = vertices_new[i, 2]
        norm_z = (z_value - z_min) / (z_max - z_min + 1e-8)
        
        colors[i] = [norm_z, 0, 1-norm_z]
    
    ax.clear()
    
    mesh_faces = [vertices_new[triangle] for triangle in triangles]
    
    face_colors = []
    for triangle in triangles:
        face_colors.append(colors[triangle].mean(axis=0))
    
    poly_collection = Poly3DCollection(mesh_faces, facecolors=face_colors, edgecolors='k', linewidths=0.2)
    ax.add_collection3d(poly_collection)
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-amplitude, amplitude)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.view_init(elev=current_elev, azim=current_azim)
    
    ax.set_title(f"Frame: {frame} | Wave parameters: A={amplitude:.2f}, f1={freq1:.1f}, f2={freq2:.1f}")

    return poly_collection,

ani = FuncAnimation(fig, update, frames=100, interval=50)

plt.show()
