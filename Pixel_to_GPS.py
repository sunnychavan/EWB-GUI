import numpy as np
from PIL import Image


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


def pixel_to_GPS(image, H, W, tl, tr, bl):
    """
    pixel_to_GPS allows us to convert from pixel coordinates to GPS coordinates 
    of every pixel in the image with only the GPS coordinates of the top left pixel,
    top right pixel, and bottom left pixel.


    INPUTS:
        image : image that we will convert pixel coordinate to GPS coordinate
        H: height of the image
        W: width of the image
        tl: GPS coordinate of the top left corner of the image
        tr: GPS coordinate of the top right corner of the image
        bl: GPS coordinate of the bottom left corner of the image

    OUTPUTS:
        GPS_coords: 2D Array representing the GPS coordinate at a certain pixel
            Example: GPS_coords[0][0] will return the GPS coordinate of the top left pixel



    """
    GPS_coords = np.zeros((H, W), dtype='f,f')
    GPS_coords[0][0] = tl
    GPS_coords[0][W-1] = tr
    GPS_coords[H-1][0] = bl
    GPS_coords = fill_array(GPS_coords, H, W, tl, tr, bl)
    return GPS_coords


def fill_array(GPS_coords, H, W, tl, tr, bl):
    """
    HELPER METHOD for pixel_to_GPS.

    """
    bl_x, bl_y = bl
    tr_x, tr_y = tr
    tl_x, tl_y = tl

    slope1x = (float)(tr_x - tl_x) / W  # How much to increment x by for line 1

    # How much to incrememnt y by for line 2
    slope2y = (float)(bl_y - tl_y) / H

    if (tr_x - tl_x == 0):
        slope1 = 0.0
    else:
        slope1 = (float)(tr_y-tl_y) / (tr_x - tl_x)  # Slope of Line 1
    if (bl_y - tl_y == 0):
        slope2 = 0.0
    else:
        slope2 = (float)(bl_x-tl_x) / (bl_y-tl_y)  # Slope of Line 2

    for i in range(W-1):  # Fill in the top and bottom edges
        x_scaled = slope1x*i
        GPS_coords[0][i] = (x_scaled, x_scaled*slope1)
        GPS_coords[H-1][i] = (bl_x + x_scaled, bl_y + (x_scaled*slope1))

    for j in range(H-1):  # Fill in the left and right edges
        y_scaled = slope2y*j
        GPS_coords[j][0] = (y_scaled*slope2, y_scaled)
        GPS_coords[j][W-1] = (tr_x + (y_scaled*slope2), tr_y + y_scaled)

    for z in range(H-1):  # Fill in everything in between
        x, y = GPS_coords[z][0]
        for i in range(W-1):
            x_scaled = slope1x*i
            GPS_coords[z][i] = (x + x_scaled, y + (x_scaled*slope1))

    return GPS_coords


if __name__ == "__main__":

    img = read_image("resources/images/test.png")
    W, H, _ = img.shape
    gps = pixel_to_GPS(img, H, W, (0.0, 0.0), (W, 0.0), (0.0, H))
    print(gps[5][0])
