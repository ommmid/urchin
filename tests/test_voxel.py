import numpy as np
from urchin import URDF
import trimesh

robot = URDF.load("data/ur5/ur5.urdf")
robot_initial_pose = {'shoulder_pan_joint': 0.1}

points = np.random.rand(5,3)
points = np.vstack((points, np.array([0,0,0]).reshape(1,3)))

cloud = trimesh.points.PointCloud(points)

voxel_mesh = robot.create_voxel(points, 0.1)

robot.show_trimesh(robot_initial_pose , [cloud, voxel_mesh])
