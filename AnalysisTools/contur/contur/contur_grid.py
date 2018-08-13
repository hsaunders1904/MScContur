#!/usr/bin/env python

import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D


class ConturGrid:

    def __init__(self, map_file_path, grid_size, parameters=None):

        with open(map_file_path, 'rb') as f:
            self.depots = pickle.load(f)

        self.grid_size = grid_size
        if parameters is None:
            self.parameters = sorted([p for p in self.depots[0].params])
        else:
            self.parameters = parameters

        # Read parameter values from .map file to a dictionary
        self.params = {}
        self.conf_lvls = []
        for depot in self.depots:
            for param in self.parameters:
                try:
                    self.params[param].append(depot.params[param])
                # We expect to fail with KeyError first time for each param
                except KeyError:
                    try:
                        self.params[param] = [depot.params[param]]
                    # If we get key error again parameter not in map file
                    except KeyError:
                        print("No parameter '%s'!" % param)
                        print("Present parameters are:")
                        print(' '.join(self._get_parameters()))
                        sys.exit()
            self.conf_lvls.append(depot.conturPoint.CLs)

        self.parameter_vals = [self.params[param] for param in self.parameters]
        self.grid = self._generate_grid()

    def __str__(self):
        return str(self.grid)

    def __repr__(self):
        return "ConturGrid object: " + str(self._get_parameters())

    def _generate_grid(self):
        """Interpolate between points in the grid"""
        self.parameter_space = []
        for vals in self.parameter_vals:
            param_range = np.linspace(min(vals), max(vals), self.grid_size)
            self.parameter_space.append(param_range)
        mesh_points = tuple(np.meshgrid(*self.parameter_space))
        grid = griddata(tuple(self.parameter_vals), self.conf_lvls,
                        mesh_points)
        return grid

    def _get_parameters(self):
        """Get parameter names from conturDepot object"""
        present_parameters = []
        for param in self.depots[0].params:
            present_parameters.append(param)
        return present_parameters

    def plot_imshow(self, slice_idx, x_label=None, y_label=None, z_label=None,
                    title=None, plot_points=False, output_path='heatmap.png',
                    dont_save=False):
        """Generate heat map of slice of grid"""
        if x_label is None:
            x_label = self.parameters[0]
        if y_label is None:
            y_label = self.parameters[1]
        if len(self.parameters) > 2:
            if z_label is None and title is None:
                title = '%s=%.4f' % (self.parameters[2],
                                     self.parameter_space[-1][slice_idx])
            elif title:
                title += '\n%s=%.4f' % (self.parameters[2],
                                        self.parameter_space[-1][slice_idx])

        axis_limits = (min(self.parameter_vals[0]),
                       max(self.parameter_vals[0]),
                       min(self.parameter_vals[1]),
                       max(self.parameter_vals[1]))

        if len(self.grid.shape) == 2:
            grid_slice = self.grid
        else:
            grid_slice = self.grid[:, :, slice_idx]

        plt.figure()
        plt.imshow(grid_slice, origin='lower', aspect='auto',
                   vmin=min(self.conf_lvls), vmax=1, extent=axis_limits,
                   cmap=plt.get_cmap('magma'))

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        x_axis_pad = 0.02 * (axis_limits[1] - axis_limits[0])
        y_axis_pad = 0.02 * (axis_limits[3] - axis_limits[2])
        plt.xlim([axis_limits[0] - x_axis_pad, axis_limits[1] + x_axis_pad])
        plt.ylim([axis_limits[2] - y_axis_pad, axis_limits[3] + y_axis_pad])
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Confidence Level', rotation=270)
        cbar.ax.get_yaxis().labelpad = 15

        if plot_points is True:
            plt.plot(self.parameter_vals[0], self.parameter_vals[1], 'o')
            for i in range(len(self.parameter_vals[0])):
                plt.text(self.parameter_vals[0][i], self.parameter_vals[1][i],
                         '%04i' % i, fontsize=6)
        if dont_save is False:
            plt.savefig(output_path)

    def plot_3d_scatter(self, x_label=None, y_label=None, z_label=None,
                        title=None, dont_save=False,
                        output_path='3d_plot.png'):
        """Plot a 3D scatter graph"""
        if x_label is None:
            x_label = self.parameters[0]
        if y_label is None:
            y_label = self.parameters[1]
        if z_label is None:
            z_label = self.parameters[2]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.parameter_vals[0], self.parameter_vals[1],
                   self.parameter_vals[2], c='r', marker='^')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        if title:
            plt.title(title)

        if dont_save is False:
            plt.savefig(output_path)

    def plot_2d_scatter(self, x_label=None, y_label=None, title=None,
                        dont_save=False, output_path='2d_plot.png'):
        """Plot 2D scatter graph"""
        if x_label is None:
            x_label = self.parameters[0]
        if y_label is None:
            y_label = self.parameters[1]

        plt.plot(self.parameter_vals[0], self.parameter_vals[1], 'o')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if title:
            plt.title(title)

        if dont_save is False:
            plt.savefig(output_path)
