from urchin import URDF
import numpy as np
from pathlib import Path
import trimesh
import itertools

def calcSteps(lower_baound, upper_bound, step_size):
    num_steps = int((upper_bound - lower_baound)/step_size)
    return np.linspace(lower_baound, upper_bound, num_steps)



# p = "/home/oheidari/PersonaIsaacLab/external/valkyrie/src/main/resources/models/val_description/urdf/package://val_description/model/meshes/pelvis/pelvis.dae"

# indx = p.find("package://")
# rel_to_pkg = p[indx+10:]
# print('rel_to_pkg: ', rel_to_pkg)

# pkg_name = p[indx+10:].split('/')[0]
# print('package name: ', pkg_name)
# pkg_name_len = len(pkg_name)

# indx = p.find(pkg_name)
# parent = p[:indx]
# print(parent + rel_to_pkg)

robot = URDF.load("tests/data/ur5/ur5.urdf")

# robot.show(cfg={
#     'shoulder_lift_joint': -2.0,
#     'shoulder_lift_joint': -2.0,
# })

# robot.animate(cfg_trajectory={
#     'shoulder_pan_joint' : [-np.pi / 4, np.pi / 4],
#     'shoulder_lift_joint' : [0.0, -np.pi / 2.0],
#     'elbow_joint' : [0.0, np.pi / 2.0]
# })


valk_path = "/home/oheidari/PersonaIsaacLab/external/valkyrie/src/main/resources/models/val_description/urdf/valkyrie_sim.urdf"
# valk = URDF.load(valk_path)
valk = URDF.load(valk_path, lazy_load_meshes=False)


# valk.show({
#         'rightElbowPitch' : -np.pi / 4,
#     'rightKneePitch' :  np.pi / 4,
# }
# )


# valk.animate(cfg_trajectory={
#     'rightElbowPitch' : [-np.pi / 4, np.pi / 4],
#     'rightKneePitch' : [-np.pi / 4, np.pi / 4],
    
# })


ee = 'rightPalm'


# chain of joints
joints = [  "rightShoulderPitch", 
            "rightShoulderRoll",
            "rightShoulderYaw",
            "rightElbowPitch",
            "rightForearmYaw",
            "rightWristRoll",
            "rightWristPitch"]


num_steps = 6
cfg = {}

j_steps = []
for j in joints:
    j_steps.append( np.linspace(valk.joint_map[j].limit.lower, valk.joint_map[j].limit.upper, num_steps) )


joints_combs = list(itertools.product(*j_steps))
vals = np.array(joints_combs)
print(vals.shape)

for x, j in enumerate(joints):
    cfg[j] = vals[:,x]

cfg["torsoPitch"] = 1.0*np.ones_like(vals[:,0])
# cfg["rightKneePitch"] = -1.0*np.ones_like(vals[:,0])
# cfg["leftKneePitch"] = -1.0*np.ones_like(vals[:,0])

print('inja 1')

ee_fk = valk.link_fk_batch(cfg, link=ee)
points = ee_fk[:,:3,3]

cloud = trimesh.points.PointCloud(points)
print('inja 3')
# scene = trimesh.Scene([cloud_original])
# scene.show()

# valk.show()


valk.show_trimesh({"torsoPitch": 1.0}, cloud)
# valk.show_trimesh({"torsoPitch": 1.0, "rightKneePitch": -1.0, "leftKneePitch": -1.0}, cloud)




