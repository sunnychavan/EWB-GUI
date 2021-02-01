import math
import numpy as np


def get_rot_mx(angle):
    '''
    Input:
        angle -- angle of CCW rotation in degrees
    Output:
        A 3x3 numpy array representing 2D rotations in homogeneous coordinates.
    '''
    angle = angle*(math.pi/180)
    rot_mx = np.array([[math.cos(angle), (-1)*math.sin(angle), 0],
                       [math.sin(angle), math.cos(angle), 0],
                       [0, 0, 1]])

    return rot_mx


def get_trans_mx(trans_vec):
    '''
    Input:
        trans_vec -- Translation vector represented by an 1D numpy array with 2
        elements
    Output:
        A 3x3 numpy array representing 2D translation.
    '''
    assert trans_vec.ndim == 1
    assert trans_vec.shape[0] == 2

    trans_mx = np.eye(3)
    trans_mx[:2, 2] = trans_vec

    return trans_mx


def get_scale_mx(s_x, s_y):
    '''
    Input:
        s_x -- Scaling along the x axis
        s_y -- Scaling along the y axis
    Output:
        A 3x3 numpy array representing 2D scaling.
    '''
    scale_mx = np.eye(3)

    for i, s in enumerate([s_x, s_y]):
        scale_mx[i, i] = s

    return scale_mx
