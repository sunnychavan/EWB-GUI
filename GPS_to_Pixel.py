import math
import numpy as np
import PIL
from matplotlib import pyplot as plt
from PIL import Image
import os
import transformations


def GPS_to_pixel_callibrated(H, W, bl, tr, gps):
    """Returns the pixel location/indices on the image that corresponds to the
    gps coordinates passed. Uses two coordinate calculation (requires coordinates to be
    'transformed'.
        Arguments:
            H -- height of aerial image
            W -- width of aerial image
            bl -- gps coordinates corresponding to the bottom left corner of the image
            tr -- gps coordinates corresponding to the top right corner of the image
            gps -- gps coordinate that we wish to find the pixel indices for.
        Output:
            The i,j indices for the specific pixel with the given gps coordindates
    """
    bl_x, bl_y = bl
    tr_x, tr_y = tr
    gps_x, gps_y = gps

    if gps_x > tr_x or gps_x < bl_x or gps_y < bl_y or gps_y > tr_y:
        print("GPS coordinate provided does not lie within the image given")
    else:
        return (findIndex1(H, gps_y, tr_y, bl_y), findIndex2(W, gps_x, tr_x, bl_x))


def findIndex2(W, gps, tr, bl):
    """Uses simple ratio math to determine the x index correspondent to
        the given gps coordinates based on the image width"""
    gps_width = max(tr, bl) - min(tr, bl)
    if gps_width == 0:
        return (int)(tr)
    location = gps - min(tr, bl)
    ratio = location/gps_width
    position = ratio*W
    return (int)(position)


def findIndex1(H, gps, tr, bl):
    """Uses simple ratio math to determine the y index correspondent to
        the given gps coordinates based on the image height"""
    gps_width = max(tr, bl) - min(tr, bl)
    if gps_width == 0:
        return (int)(tr)
    location = gps - min(tr, bl)
    ratio = location/gps_width
    position = ratio*H
    return (int)(H - position)


def read_image(image_path):
    """Reads an image as a numpy array given the path/directory as an arugment."""
    x = np.array(Image.open(image_path), dtype='uint8')
    shape = x.shape
    H = shape[0]
    W = shape[1]
    image = np.zeros((H, W, 3), dtype='uint8')
    if x.ndim == 3:
        image = x[:, :, 0:3]
    else:
        for i in range(H):
            for j in range(W):
                image[i, j, 0] = x[i, j]
                image[i, j, 1] = x[i, j]
                image[i, j, 2] = x[i, j]
    return image


def get_orientation(tl, bl):
    """Returns the CW angle between 'world' Frame of reference
        and the image's frame of reference."""
    p1 = np.array([tl[0], tl[1]])
    p3 = np.array([bl[0], bl[1]])
    direction = p1 - p3
    unit_dir = direction/np.linalg.norm(direction)
    x1, y1 = 0.0, 1.0
    x2, y2 = unit_dir[0], unit_dir[1]
    dot = x1*x2 + y1*y2
    det = x1*y2 - x2*y1
    return (-1)*math.atan2(det, dot)*(180/math.pi)


def get_transformation_matrix(tl, bl, tr, theta):
    """Returns transformation matrix that translates center to (0,0)
        and rotates image CCW by orientation theta. Then scales to
        be unit square centered at (0,0)"""
    # Calculates the center gps coordinates of the image/rectangle
    center_x = (bl[0] + tr[0])/2
    center_y = (bl[1] + tr[1])/2
    # Calculates the width and height in gps coordinates of the image/rectangle
    len_x = math.sqrt(math.pow(tl[0] - tr[0], 2) + math.pow(tl[1] - tr[1], 2))
    len_y = math.sqrt(math.pow(tl[0] - bl[0], 2) + math.pow(tl[1] - bl[1], 2))
    # Translation, Rotation, Scale matrix calculations
    trans_vec = np.array([-center_x, -center_y])
    trans_mx = transformations.get_trans_mx(trans_vec)
    rot_mx = transformations.get_rot_mx(theta)
    scale_mx = transformations.get_scale_mx(1/len_x, 1/len_y)
    return np.matmul(scale_mx, np.matmul(rot_mx, trans_mx))


def transform_point(matrix, coordinates):
    """Transforms individual points in 2D space to match that of the 'world's'
        frame of reference"""
    x, y = coordinates
    # Homogeneous representation of vec(x,y)
    vec = np.array([x, y, 1])
    vec_new = np.dot(matrix, vec)
    x_new, y_new = vec_new[0], vec_new[1]
    return (x_new, y_new)


def get_four_corners():
    """In general, would get this from csv file but just using
        arbitrary coordinates for testing purposes."""
    tl = (1, 0)
    tr = (0, 1)
    br = (4, 5)
    bl = (5, 4)
    return (tl, tr, bl, br)


def GPS_to_pixel(image, gps):
    """Finds the pixel location of the gps coordinates on the image.
        Arguments:
            Image -- the aerial image used (taken parrallel to the Earth) and
                this is before image's frame of reference is callibrated to match
                that of the 'world'.
            gps -- Gps coordinates that we wish to convert to pixel location.
        Output:
            Pixel indices corresponding to gps coordinates.
    """
    H, W = image.shape[:2]

    # Usually this would be read from csv file
    tl, tr, bl, br = get_four_corners()

    angle = get_orientation(tl, bl)
    print(angle)
    mat = get_transformation_matrix(tl, bl, tr, angle)
    bl_cal = transform_point(mat, bl)
    tr_cal = transform_point(mat, tr)
    gps_cal = transform_point(mat, gps)
    print(bl_cal, tr_cal, gps_cal)

    pixel_indices = GPS_to_pixel_callibrated(H, W, bl_cal, tr_cal, gps_cal)
    return pixel_indices


def assure_type_before_saving(image):
    if image.dtype == 'float64':
        image = np.uint8(image*255)
    return image


def write_image(image, out_path):
    """Writes a numpy array as an image file.

    Args:
      image: Numpy array containing image to write
      out_path: Path for the output image
    """
    image = assure_type_before_saving(image)
    Image.fromarray(image).save(out_path)


def pinpoint_pixel(image, pixel):
    x, y = pixel
    image[x-2:x+3, y-2:y+3, 0] = 255
    image[x-2:x+3, y-2:y+3, 1] = 0
    image[x-2:x+3, y-2:y+3, 2] = 0


def pixel_to_GPS(image, H, W, tl, tr, bl):
    GPS_coords = np.zeros((H, W))
    GPS_coords[0][0] = tl
    GPS_coords[0][W-1] = tr
    GPS_coords[H-1][0] = bl
    fill_array(GPS_coords,H,W,tl,tr,bl)
    return GPS_coords


def fill_array(GPS_coords, H, W, tl, tr, bl):
    bl_x, bl_y = bl
    tr_x, tr_y = tr
    tl_x, tl_y = tl

    slope1x = (tr_x - tl_x) / W  # How much to increment x by for line 1
    slope2y = (bl_y - tl_y) / H  # How much to incrememnt y by for line 2

    slope1 = (tr_y-tl_y) / (tr_x - tl_x)  # Slope of Line 1
    slope2 = (bl_x-tl_x) / (bl_y-tl_y)  # Slope of Line 2

    for i in range(W-1):
        x_scaled = slope1x*i
        GPS_coords[0][i] = (x_scaled, x_scaled*slope1)
        GPS_coords[H-1][i] = (bl_x + x_scaled , bl_y+ (x_scaled*slope1) )   

    for j in range(H-1):
        y_scaled = slope2y*j
        GPS_coords[j][0] = (y_scaled*slope2, y_scaled)
        GPS_coords[j][W-1] = (tr_x + (y_scaled*slope2), tr_y + yscaled)


    for(z in range(H-1)):
        x,y = GPS_coords[z][0]
        for i in range(W-1):
        x_scaled = slope1x*i
        GPS_coords[z][i] = (x+ x_scaled, y+ (x_scaled*slope1) )

    return gps_coords



"""
def pixel_GPS_coordinates(image, H, W, bl, tr):
    Returns the pixel coordinate matrix and the corresponding GPS coordinate matrix


    
    GPS_coords = np.zeros((H, W))
    GPS_coords[0][H-1] = bl
    GPS_coords[W-1][0] = tr
    bl_x, bl_y = bl
    tr_x, tr_y = tr

    x_scale = (tr_x - bl_x) / W
    y_scale = (br_y - tr_x) / H
    x = 0
    y = H-1

    for i in range (W):
        bl_x += x_scale
        for j in range H:
            bl_y -= y_scale
            GPS_coords[x][y] = (bl_x, bl_y)
            y += 1
        x += 1

    return
"""


im = read_image("field.png")
print(im)
# Test cases
print(im.shape[:2])
print("Near top left corner:")
pixel = GPS_to_pixel(im, (1, 0.2))
print(pixel)

print("Near bottom left corner:")
pixel = GPS_to_pixel(im, (4.8, 4))
print(pixel)

print("Near top right corner:")
pixel = GPS_to_pixel(im, (0.2, 1))
print(pixel)

print("Near bottom right corner:")
pixel = GPS_to_pixel(im, (4, 4.8))
print(pixel)

print("Middle of the image:")
pixel = GPS_to_pixel(im, (2.5, 2.5))
print(pixel)

print("Outside the image:")
pixel = GPS_to_pixel(im, (0.5, 0.2))
print(pixel)
