import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as colors

fig = plt.figure(figsize=(10, 8))
plt.subplots_adjust(top=0.9)
fig.suptitle('Central Peak with Radial Color Gradient', fontsize=16)
ax = fig.add_subplot(111, projection='3d')

grid_size = 30
x = np.linspace(-1, 1, grid_size)
y = np.linspace(-1, 1, grid_size)
X, Y = np.meshgrid(x, y)

R_squared = X**2 + Y**2  
Z = np.exp(-4 * R_squared)  

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

distances = np.sqrt(R_squared.flatten())
normalized_distances = distances / distances.max()

colors_array = np.zeros((vertices.shape[0], 3))
colors_array[:, 0] = 1 - normalized_distances**2  
colors_array[:, 1] = np.exp(-3 * normalized_distances) 
colors_array[:, 2] = normalized_distances  

mesh_faces = [vertices[triangle] for triangle in triangles]

face_colors = []
for triangle in triangles:
    face_colors.append(colors_array[triangle].mean(axis=0))

poly_collection = Poly3DCollection(mesh_faces, facecolors=face_colors, edgecolors='k', linewidths=0.2)
ax.add_collection3d(poly_collection)

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(0, 1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

view_elev = 30
view_azim = 45

def on_rotate(event):
    global view_elev, view_azim
    if hasattr(ax, 'elev') and ax.elev is not None:
        view_elev = ax.elev
    if hasattr(ax, 'azim') and ax.azim is not None:
        view_azim = ax.azim

fig.canvas.mpl_connect('motion_notify_event', on_rotate)
ax.view_init(elev=view_elev, azim=view_azim)

plt.show()
