import trimesh
import numpy as np


class PC2Voxel:

    def create_voxel(self, points, voxel_size = 0.1):
        """ Converts a given point cloud to voxels

        Parameters
        ---------
        points : ndarray (n x 3)
            n is the number of points

        Returns
        -------
        Trimesh
        """

        # Step 1: Compute bounding box
        min_bound = np.min(points, axis=0)
        max_bound = np.max(points, axis=0)
        
        # Step 2: Determine voxel grid size
        grid_size = np.ceil((max_bound - min_bound) / voxel_size).astype(int)
        
        # Step 3: Map points to voxel indices
        voxel_indices = np.floor((points - min_bound) / voxel_size).astype(int)
        
        # Step 4: Remove duplicate voxels
        voxel_indices = np.unique(voxel_indices, axis=0)

        print(f"Voxel Grid Size: {grid_size}")
        print(f"Number of Occupied Voxels: {len(voxel_indices)}")

        # Create a 3D numpy array to represent a simple voxel grid
        voxel_data = np.zeros((grid_size[0], grid_size[1], grid_size[2]), dtype=bool)

        # Fill in some voxels to create a shape (e.g., a cube)
        voxel_data[voxel_indices[:,0], voxel_indices[:,1], voxel_indices[:,2]] = True

        # Create a VoxelGrid object
        voxel_grid = trimesh.voxel.VoxelGrid(encoding=voxel_data, transform=np.eye(4))

        scale = voxel_grid.scale
        print('scale: ', scale)

        # Print some properties of the VoxelGrid
        print("Voxel size (pitch):", voxel_grid.pitch)
        print("Voxel grid shape:", voxel_grid.encoding.shape)

        # Convert the voxel grid to a mesh for visualization
        mesh = voxel_grid.as_boxes()

        mesh.apply_scale(voxel_size)
        mesh.apply_translation(min_bound + 0.5*voxel_size)

        return mesh
