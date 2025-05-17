import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors

grid_size = 30  
x = np.linspace(-3, 3, grid_size)
y = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x, y)

Z = 0.5 * np.sin(X) * np.cos(Y) + 0.2 * np.sin(3*X) + 0.3 * np.cos(2*Y)

vertices = np.vstack([X.flatten(), Y.flatten(), Z.flatten()]).T

triangles = []
for i in range(grid_size-1):
    for j in range(grid_size-1):
        p1 = i * grid_size + j
        p2 = i * grid_size + j + 1
        p3 = (i + 1) * grid_size + j + 1
        p4 = (i + 1) * grid_size + j
        
        triangles.append([p1, p2, p3])  
        triangles.append([p1, p3, p4])  

triangles = np.array(triangles)

z_min, z_max = Z.min(), Z.max()
z_normalized = (Z.flatten() - z_min) / (z_max - z_min)

fig = plt.figure(figsize=(12, 10))
plt.subplots_adjust(top=0.9)
fig.suptitle('Custom Terrain with Height-Based Coloring', fontsize=16)
ax = fig.add_subplot(111, projection='3d')

mesh = []
face_colors = []
cmap = plt.cm.terrain 

for triangle in triangles:
    triangle_vertices = vertices[triangle]
    mesh.append(triangle_vertices)
    
    avg_z = np.mean(Z.flatten()[triangle])
    color_val = (avg_z - z_min) / (z_max - z_min)
    face_colors.append(cmap(color_val))

terrain = Poly3DCollection(mesh, alpha=1.0)
terrain.set_facecolors(face_colors)
ax.add_collection3d(terrain)

ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())
ax.set_zlim(Z.min(), Z.max())
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Elevation (Z)')

norm = colors.Normalize(vmin=z_min, vmax=z_max)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax, shrink=0.5, aspect=5, label='Elevation')

view_elev = 30
view_azim = 45

def on_rotate(event):
    global view_elev, view_azim
    if hasattr(ax, 'elev') and ax.elev is not None:
        view_elev = ax.elev
    if hasattr(ax, 'azim') and ax.azim is not None:
        view_azim = ax.azim

fig.canvas.mpl_connect('motion_notify_event', on_rotate)

plt.show()
