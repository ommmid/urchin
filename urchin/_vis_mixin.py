
from copy import deepcopy
from typing import Sequence
import logging
import trimesh
import open3d as o3d
import numpy as np

# desc: separate the visualization stuff from the urdf.py file as it is getting really large. This is 
# a mixin, URDF class will inherit this but just to have access to its funciton. It is not really 
# a parent of URDF but just a way to seaparet some functionalities of URDF into another file

event_logger = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)

import glooey
import pyglet
import pathlib

import glooey
import numpy as np
import pyglet

import trimesh
import trimesh.viewer

class MyLabel(glooey.Label):
    custom_color = '#babdb6'
    custom_font_size = 10
    custom_alignment = 'center'

# If we want another kind of text, for example a bigger font for section
# titles, we just have to derive another class:

class MyTitle(glooey.Label):
    custom_color = '#eeeeec'
    custom_font_size = 12
    custom_alignment = 'center'
    custom_bold = True

# It's also common to style a widget with existing widgets or with new
# widgets made just for that purpose.  The button widget is a good example.
# You can give it a Foreground subclass (like MyLabel from above) to tell it
# how to style text, and Background subclasses to tell it how to style the
# different mouse rollover states:

class MyButton(glooey.Button):
    Foreground = MyLabel
    custom_alignment = 'fill'

    # More often you'd specify images for the different rollover states, but
    # we're just using colors here so you won't have to download any files
    # if you want to run this code.

    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#3465a4'

    class Down(glooey.Background):
        custom_color = '#729fcff'

    # Beyond just setting class variables in our widget subclasses, we can
    # also implement new functionality.  Here we just print a programmed
    # response when the button is clicked.

    def __init__(self, text, response, robot):
        super().__init__(text)
        self.response = response
        self.robot = robot

    def on_click(self):
        print(self.robot)

class Visualization():

    def run_app(self, scene):
        # create window with padding
        width, height = 480 * 3, 2*360
        
        config = pyglet.gl.Config(
                sample_buffers=1, samples=4, depth_size=24, double_buffer=True
            )
        window = window = pyglet.window.Window(config=config, width=width, height=height)

        gui = glooey.Gui(window)

        hbox = glooey.HBox()
        hbox.set_padding(5)

        # scene widget for changing camera location
        self.scene_widget1 = trimesh.viewer.SceneWidget(scene)
        self.scene_widget1._angles = [np.deg2rad(45), 0, 0]
        hbox.add(self.scene_widget1)

        button = MyButton("Blue.", "Right, off you go.")
        hbox.add(button)    

        gui.add(hbox)

        pyglet.app.run()



    def show(self, cfg=None, use_collision=False):
        """Visualize the URDF in a given configuration.

        Parameters
        ----------
        cfg : dict or (n), float
            A map from joints or joint names to configuration values for
            each joint, or a list containing a value for each actuated joint
            in sorted order from the base link.
            If not specified, all joints are assumed to be in their default
            configurations.
        use_collision : bool
            If True, the collision geometry is visualized instead of
            the visual geometry.
        """
        import pyribbit  # Save pyribbit import for here for CI

        if use_collision:
            fk = self.collision_trimesh_fk(cfg=cfg)
        else:
            fk = self.visual_trimesh_fk(cfg=cfg)

        scene = pyribbit.Scene()
        for tm in fk:
            pose = fk[tm]
            mesh = pyribbit.Mesh.from_trimesh(tm, smooth=False)
            scene.add(mesh, pose=pose)
        pyribbit.Viewer(scene, use_raymond_lighting=True)

    
    def show_trimesh(self, cfg=None, extra=None):
        '''extra: is the extra types to visualize, could be axis, point cloud ....'''
        fk = self.visual_trimesh_fk(cfg=cfg)
        meshes = []
        for tm in fk:
            pose = fk[tm]
            tm.apply_transform(pose)
            meshes.append(tm)
        meshes.extend(extra)

        axis = trimesh.creation.axis()

        scene = trimesh.Scene([axis, extra, meshes])
        scene.show()



    def show_widget(self, cfg=None, extra=None):
        '''extra: is the extra types to visualize, could be axis, point cloud ....'''

        def create_scene(cfg, extra):
            fk = self.visual_trimesh_fk(cfg=cfg)
            meshes = []
            for tm in fk:
                pose = fk[tm]
                tm.apply_transform(pose)
                meshes.append(tm)
            meshes.extend(extra)

            axis = trimesh.creation.axis()

            scene = trimesh.Scene([axis, extra, meshes])
            return scene

        scene = create_scene(cfg, extra)
        np.random.seed(0)
        self.run_app(scene)
