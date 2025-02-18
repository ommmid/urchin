from urchin import URDF
import numpy as np
from pathlib import Path

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
valk = URDF.load(valk_path, lazy_load_meshes=True)


# valk.show()


valk.animate(cfg_trajectory={
    'rightElbowPitch' : [-np.pi / 4, np.pi / 4],
    'rightKneePitch' : [-np.pi / 4, np.pi / 4],
    
})
