import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

grid_size = 20
x = np.linspace(-1, 1, grid_size)
y = np.linspace(-1, 1, grid_size)
X, Y = np.meshgrid(x, y)
vertices = np.vstack([X.flatten(), Y.flatten(), np.zeros(X.size)]).T

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

colors = np.zeros((vertices.shape[0], 3))  # RGB

red    = np.array([1, 0, 0])
green  = np.array([0, 1, 0])
blue   = np.array([0, 0, 1])
yellow = np.array([1, 1, 0])

for i, (x, y, _) in enumerate(vertices):
    if x >= 0 and y >= 0:
        colors[i] = red
    elif x < 0 and y >= 0:
        colors[i] = green
    elif x < 0 and y < 0:
        colors[i] = blue
    else:
        colors[i] = yellow

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

mesh_faces = [vertices[triangle] for triangle in triangles]

face_colors = [colors[triangle].mean(axis=0) for triangle in triangles]

poly_collection = Poly3DCollection(mesh_faces, facecolors=face_colors, edgecolors='k', linewidths=0.5)
ax.add_collection3d(poly_collection)

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-0.1, 0.1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Square Mesh Divided into Four Colored Quadrants')

plt.show()

