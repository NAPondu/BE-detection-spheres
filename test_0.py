# -*- coding: utf-8 -*-
"""
Test_0
"""



import numpy as np
import time as time


# For line of command
import sys

from PIL import Image, ImageOps, ImageFilter


#Should be given as argument
LIGHTEST_COLOR_INTENSITY = 255

list_groups = []
list_pixel = []

#Should be given as argument
IMAGE_NAME = "im_0.jpg"

#Should be determined from IMAGE_NAME or given as argument
MASK_NAME = "im_0_mk.jpg"

#Information that isn't to be given to the users, only for the developper
GET_TIME = True

#Should be given as argument
REPORT = True

#Should be given as argument
DETAILLED_REPORT = True


if GET_TIME:
    print("Beginning calculus")
    print("TIME = ", time.asctime(time.gmtime()))
image=Image.open(MASK_NAME)
ld=image.load()

for i in range(0,image.width):
    for j in range(0, image.height):
        if image.getpixel((i,j))>180:
            list_pixel.append((i,j))
            ld.__setitem__((i,j),255)
        else:
            ld.__setitem__((i,j),0)

for i in range(1,image.width-1):
    for j in range(1,image.height-1):
        pixel = image.getpixel((i,j))
        if image.getpixel((i,j+1))==pixel:
            continue
        if image.getpixel((i,j-1))==pixel:
            continue
        if image.getpixel((i+1,j))==pixel:
            continue
        if image.getpixel((i-1,j))==pixel:
            continue
        if pixel==255:
            ld.__setitem__((i,j),0)
        else:
            ld.__setitem__((i,j),255)
        
image.save("TreatedMask.png")
image.close()
image=Image.open(MASK_NAME)
            
if GET_TIME:
    print("Done binarizing")
    print("TIME = ", time.asctime(time.gmtime()))

list_pixel_sorted = sorted(list_pixel)



for i in range(0,len(list_pixel)):
    found_neighbour = False
    value = -1
    for j in range(0,len(list_groups)):
        if (list_pixel[i][0] -1, list_pixel[i][1]) in list_groups[j]:
            if not found_neighbour:
                list_groups[j].append(list_pixel[i])
                found_neighbour = True
                value = j
            else:
                if value !=j:
                    list_groups[value].extend(list_groups[j])
                    del(list_groups[j])
                    j-=1
        if (list_pixel[i][0], list_pixel[i][1] -1) in list_groups[j]:
            if not found_neighbour:
                list_groups[j].append(list_pixel[i])
                found_neighbour = True
                value = j
            else:
                if value != j:
                    list_groups[value].extend(list_groups[j])
                    del(list_groups[j])
                    j-=1
    if value == -1:
        list_groups.append([list_pixel[i]])
       

if GET_TIME:
    print("Done generating groups")
    print("TIME = ", time.asctime(time.gmtime()))

border = []

brd = Image.new("RGB",image.size)
ld_brd = brd.load()

for i in range(0,len(list_groups)):
    border.append([])
    for j in range(0,len(list_groups[i])):
        minimum = 255
        cur_width = list_groups[i][j][0]
        cur_height = list_groups[i][j][1]
        top = (cur_width==0)
        bottom = (cur_width==image.width)
        left = (cur_height==0)
        right = (cur_height==image.height)
        if left: 
            if top:
                minimum = min(image.getpixel((cur_width+1, cur_height)),
                              image.getpixel((cur_width, cur_height+1)))
            elif bottom:
                minimum = min(image.getpixel((cur_width+1, cur_height)),
                              image.getpixel((cur_width, cur_height-1)))
            else:
                minimum = min(image.getpixel((cur_width+1, cur_height)),
                              image.getpixel((cur_width, cur_height-1)),
                              image.getpixel((cur_width, cur_height+1)))
        elif right:
            if top:
                minimum = min(image.getpixel((cur_width-1, cur_height)),
                              image.getpixel((cur_width, cur_height+1)))
            elif bottom:
                minimum = min(image.getpixel((cur_width-1, cur_height)),
                              image.getpixel((cur_width, cur_height-1)))
            else:
                minimum = min(image.getpixel((cur_width-1, cur_height)),
                              image.getpixel((cur_width, cur_height-1)),
                              image.getpixel((cur_width, cur_height+1)))
        
        elif top:
            minimum = min(image.getpixel((cur_width-1, cur_height)),
                          image.getpixel((cur_width+1, cur_height)),
                          image.getpixel((cur_width, cur_height+1)))
        elif bottom:
            minimum = min(image.getpixel((cur_width-1, cur_height)),
                          image.getpixel((cur_width+1, cur_height)),
                          image.getpixel((cur_width, cur_height-1)))
        else:
            minimum = min(image.getpixel((cur_width-1, cur_height)),
                          image.getpixel((cur_width+1, cur_height)),
                          image.getpixel((cur_width, cur_height-1)),
                          image.getpixel((cur_width, cur_height+1)))
        if minimum < 200:
            border[i].append((cur_width,cur_height))

for i in range(0,len(border)):
    for j in range(0,len(border[i])):
        ld_brd.__setitem__((border[i][j]),(255,255,255))
brd.save("Wrong_borders.png")

if GET_TIME:
    print("Done calculating borders")
    print("TIME = ", time.asctime(time.gmtime()))


"""
for i in range(1, image.width - 2):
    for j in range(1, image.height - 2):
        minimal = image.getpixel((i-1,j))
        minimal = min(image.getpixel((i,j-1)),minimal)
        minimal = min(image.getpixel((i,j+1)),minimal)
        minimal = min(image.getpixel((i+1,j)),minimal)
        if(minimal < 100):
            border.append((i,j))
"""

for i in border:
    toDel = []
    
    for j in range(0,len(i)):
        minimum = 255
        cur_width = i[j][0]
        cur_height = i[j][1]
        top = (cur_width==0)
        bottom = (cur_width==image.width)
        left = (cur_height==0)
        right = (cur_height==image.height)
        
        if left:
            if top and (not (cur_width+1,cur_height+1)in i):
                toDel.append(j)
            elif bottom and (not (cur_width-1,cur_height+1)in i):
                toDel.append(j)
            elif (not (cur_width+1,cur_height+1)in i) and (
                    not (cur_width-1,cur_height+1)in i):
                toDel.append(j)
        elif right:
            if top and (not (cur_width+1,cur_height+1)in i):
                toDel.append(j)
            elif bottom and (not (cur_width-1,cur_height+1)in i):
                toDel.append(j)
            elif (not (cur_width+1,cur_height+1)in i) and (
                    not (cur_width-1,cur_height+1)in i):
                toDel.append(j)
        elif (top
              and not (cur_width-1,cur_height+1)in i
              and not (cur_width+1,cur_height+1)in i
              ):
            toDel.append(j)
        elif (bottom
              and not(cur_width-1,cur_height-1)in i
              and not(cur_width+1,cur_height-1)in i              
              ):
            toDel.append(j)
            
            
                
        
    
    toDel.reverse()
    for j in range(0, len(toDel)):
        del(i[toDel[j]])
   
      
    
if GET_TIME:
    print("Done erasing side effects from borders")
    print("TIME = ", time.asctime(time.gmtime()))
    



img_new = Image.new('RGB',image.size)
ld = img_new.load()


for i in range(0,len(list_groups)):
    for j in range(0,len(list_groups[i])):
        ld.__setitem__(list_groups[i][j],(0,0,0))


for j in border:
    for i in j:
        ld.__setitem__(i,(0,255,0))
        ld_brd.__setitem__(i,(0,255,0))

img_new.show()
img_new.save("Border_treated.png")
brd.save("Treated_borders_2.png")

########### Finding the lightest point
########## Input
########### All groups in list_groups (list of list of tuples)
########### All borders in border (list of list of tuples)

########### Output
############ All lightest points in light_points (list of tuples)
light_points = []
true_image=Image.open(IMAGE_NAME)

true_grayscale = ImageOps.grayscale(true_image)
r,g,b = true_image.split()
list_loss = []


#grs = true_grayscale.filter(ImageFilter.GaussianBlur(radius = 3))


"""

Following lines only take the highest value on the picture
Not precise enough


for i in list_groups:
    for j in i:
        ld.__setitem__(j,(255,255,255))


for i in range(0,len(list_groups)):
    lightest_value_in_grp = 0
    current_position = (0,0)
    for j in range(0,len(list_groups[i])):
        check_value = list_groups[i][j]
        #pixel = grs.getpixel(check_value)
        pixel = max(true_image.getpixel(check_value))
        if pixel>lightest_value_in_grp:
            lightest_value_in_grp = pixel
            current_position = check_value
    list_loss.append(lightest_value_in_grp)
    light_points.append(current_position)


for i in range(0,len(light_points)):
    ld.__setitem__((light_points[i][0],light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0]+1,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+1),(255,0,0))
    ld.__setitem__((light_points[i][0]-1,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-1),(255,0,0))
    ld.__setitem__((light_points[i][0]+2,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+2),(255,0,0))
    ld.__setitem__((light_points[i][0]-2,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-2),(255,0,0))
    ld.__setitem__((light_points[i][0]+3,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+3),(255,0,0))
    ld.__setitem__((light_points[i][0]-3,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-3),(255,0,0))
    
    ld.__setitem__((light_points[i][0]+4,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+4),(255,0,0))
    ld.__setitem__((light_points[i][0]-4,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-4),(255,0,0))

img_new.save("Light_1.png")
"""

grs = true_grayscale.filter(ImageFilter.GaussianBlur(radius = 3))
for i in range(0,len(list_groups)):
    lightest_value_in_grp = 0
    current_position = (0,0)
    for j in range(0,len(list_groups[i])):
        check_value = list_groups[i][j]
        pixel = grs.getpixel(check_value)
        if pixel>lightest_value_in_grp:
            lightest_value_in_grp = pixel
            current_position = check_value
    list_loss.append(lightest_value_in_grp)
    light_points.append(current_position)


for i in range(0,len(light_points)):
    ld.__setitem__((light_points[i][0],light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0]+1,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+1),(255,0,0))
    ld.__setitem__((light_points[i][0]-1,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-1),(255,0,0))
    ld.__setitem__((light_points[i][0]+2,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+2),(255,0,0))
    ld.__setitem__((light_points[i][0]-2,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-2),(255,0,0))
    ld.__setitem__((light_points[i][0]+3,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+3),(255,0,0))
    ld.__setitem__((light_points[i][0]-3,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-3),(255,0,0))
    
    ld.__setitem__((light_points[i][0]+4,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]+4),(255,0,0))
    ld.__setitem__((light_points[i][0]-4,light_points[i][1]),(255,0,0))
    ld.__setitem__((light_points[i][0],light_points[i][1]-4),(255,0,0))

img_new.save("Light_2.png")
img_new.show()

if GET_TIME:
    print("Donce calculating lightest points")
    print("TIME = ", time.asctime(time.gmtime()))





########## Circle fitting equation calculus
########## Input
########### All groups in list_groups (list of list of tuples)
########### All borders in border (list of list of tuples)


########## Output
########## eq => One circle equation with (x_center, y_center, ray)
########## circles_eq list of circle_equations
########## circle_borders list of list of borders (through the equation)
########## disk_points (list of list of tuples)
################ => Parkour + calculus for each point and ray smaller or not
###########Objective
list_circle = []
list_circle_eq = []
theta = np.linspace(0, 2*np.pi, 360)
for cur_border in border:
    x_list = []
    y_list = []
    
    for i in range(0,len(cur_border)):
        x_list.append(cur_border[i][0])
        y_list.append(cur_border[i][1])
    
    
    
    
    # coordinates of the barycenter
    x_m = np.mean(x_list)
    y_m = np.mean(y_list)

    # calculation of the reduced coordinates
    u = x_list - x_m
    v = y_list - y_m

    # linear system defining the center in reduced coordinates (uc, vc):
    #    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
    #    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
    Suv  = sum(u*v)
    Suu  = sum(u**2)
    Svv  = sum(v**2)
    Suuv = sum(u**2 * v)
    Suvv = sum(u * v**2)
    Suuu = sum(u**3)
    Svvv = sum(v**3)

    # Solving the linear system
    A = np.array([ [ Suu, Suv ], [Suv, Svv]])
    B = np.array([ Suuu + Suvv, Svvv + Suuv ])/2.0
    uc, vc = np.linalg.solve(A, B)

    xc_1 = x_m + uc
    yc_1 = y_m + vc

    # Calculation of all distances from the center (xc_1, yc_1)
    Ri_1      = np.sqrt((x_list-xc_1)**2 + (y_list-yc_1)**2)
    R_1       = np.mean(Ri_1)
    residu_1  = sum((Ri_1-R_1)**2)
    residu2_1 = sum((Ri_1**2-R_1**2)**2)

    circle = []

    x_value = 0
    y_value = 0
    for i in range(0,len(theta)):
        x_value = round(xc_1)+round(R_1 * np.cos(theta[i]))
        y_value = round(yc_1)+round(R_1 * np.sin(theta[i]))
        if(x_value>=0 and x_value<img_new.width and y_value>=0 and y_value<img_new.height):
           circle.append((x_value, y_value))
    list_circle.append(circle)
    list_circle_eq.append((xc_1,yc_1,R_1))

for i in range(0,len(list_circle)):
    ld.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0]+1,list_circle_eq[i][1]),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]+1),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0]-1,list_circle_eq[i][1]),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]-1),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]+2),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0]+2,list_circle_eq[i][1]),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0]-2,list_circle_eq[i][1]),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]-2),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]),(0,150,255))
    ld.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]),(0,150,255))
    for j in range(0,len(list_circle[i])):
        ld.__setitem__(list_circle[i][j],(255,255,255))

img_new.show()
img_new.save("Cercles_cas_limite.png")

if GET_TIME:
    print("Done calculating least square circle equation")
    print("TIME = ", time.asctime(time.gmtime()))

########## Circle fitting equation calculus
########## Input
###########All groups in list_groups (list of list of tuples)
###########All borders in border (list of list of tuples)
########## eq => One circle equation with (x_center, y_center, ray)
########## circles_eq list of circle_equations
########## circle_borders list of list of borders (through the equation)

########## Output
########## disk_points (list of list of tuples)
################ => Parkour + calcul pour chaque point ray + petit ou pas
###########Objective

def list_of_empty_lists(list_to_fill, number_of_list):
    if number_of_list <=0:
        return list_to_fill
    list_to_fill.append([])
    return list_of_empty_lists(list_to_fill, number_of_list-1)


def point_is_in_circle(x,y,tuple_3):
    return ((x-tuple_3[0])**2 + (y-tuple_3[1])**2)<=(tuple_3[2])**2

disk_points = list_of_empty_lists([],len(list_circle_eq))

for i in range(0,img_new.width):
    for j in range(0,img_new.height):
        for k in range(0,len(list_circle_eq)):
            if point_is_in_circle(i,j,list_circle_eq[k]):
                disk_points[k].append((i,j))
                break

"""
### If you want to color the disks, uncomment the few following lines
for i in disk_points:
    for j in i:
        ld.__setitem__(j,(255,0,0))
img_new.save("colored_disks_from_disks.png")
"""


if GET_TIME:
    print("Done coloring disks")
    print("TIME = ", time.asctime(time.gmtime()))

########## Circle fitting equation calculus
########## Input
###########All groups in list_groups (list of list of tuples)
###########All borders in border (list of list of tuples)
########## eq => One circle equation with (x_center, y_center, ray)
########## circles_eq list of circle_equations
########## circle_borders list of list of borders (through the equation)


########## Output
########## Coordonnées (x,y,z) du point avec comme origine le centre de la spere

list_of_3d_vectors = []

loss_x = []
loss_y = []

for i in range(0,len(list_circle_eq)):
    eq = list_circle_eq[i]
    light = light_points[i]
    x_p = round(light[0]) - round(eq[0])
    y_p = round(light[1]) - round(eq[1])
    hypotenuse_2d_pow2 = x_p**2 + y_p**2
    z_p = round(np.sqrt((eq[2])**2 - hypotenuse_2d_pow2))
    loss_x.append(x_p)
    loss_y.append(y_p)
    
    
    vector = (-x_p,-y_p,-z_p)
    list_of_3d_vectors.append(vector)
    
    
if GET_TIME:
    print("Done Calculating z-coordinate of lightest point")    
    print("TIME = ", time.asctime(time.gmtime()))
list_of_delta_points = []


#Finding highest the highest deltas on the border
### Meaning finding the point were there is the highest gap
### So as to find the best shadowed area to get


true_img = Image.open(IMAGE_NAME)
for i in range(0,len(border)):
    cur_border = border [i]
    max_1 = 0
    delta_1 = None
    for j in range(0,len(cur_border)):
        left=True
        right=True
        top=True
        bottom=True
        pixel = cur_border[j]
        grp = list_groups[i]
        pixel_value = max(true_img.getpixel(pixel))
        if((pixel[0],pixel[1]+1) not in cur_border and (pixel[0],pixel[1]+1) in grp):
            bottom = False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0],pixel[1]+1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0],pixel[1]+1))
                
        if((pixel[0],pixel[1]-1) not in cur_border and (pixel[0],pixel[1]-1) in grp):
            top=False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0],pixel[1]-1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0],pixel[1]-1))
            
        if((pixel[0]+1,pixel[1]) not in cur_border and (pixel[0]+1,pixel[1]) in grp):
            right=False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]+1,pixel[1]))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]+1,pixel[1]))
        if((pixel[0]-1,pixel[1]) not in cur_border and (pixel[0]-1,pixel[1]) in grp):
            left=False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]-1,pixel[1]))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]-1,pixel[1]))
                
        if(left and top and (pixel[0]-1,pixel[1]-1) not in cur_border and (pixel[0]-1,pixel[1]-1) in grp):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]-1,pixel[1]-1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]-1,pixel[1]-1))
                
        if(left and bottom and (pixel[0]-1,pixel[1]+1) not in cur_border and (pixel[0]-1,pixel[1]+1) in grp):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]-1,pixel[1]+1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]-1,pixel[1]+1))
            
        if(right and top and (pixel[0]+1,pixel[1]-1) not in cur_border and (pixel[0]+1,pixel[1]-1) in grp):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]+1,pixel[1]-1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]+1,pixel[1]-1))
    
        if(right and bottom and (pixel[0]+1,pixel[1]+1) not in cur_border and (pixel[0]+1,pixel[1]+1) in  grp):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]+1,pixel[1]+1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]+1,pixel[1]+1))
    x_c = light_points[i][0]
    y_c = light_points[i][1]
    val_1 = (x_c-delta_1[0][0])**2+(y_c-delta_1[0][1])**2
    val_2 = (x_c-delta_1[1][0])**2+(y_c-delta_1[1][1])**2
    
    if val_1>val_2 :
        list_of_delta_points.append(delta_1[1])
    else:
        list_of_delta_points.append(delta_1[0])

list_of_height = []

if GET_TIME:
    print("Done Calculating deltas")
    print("TIME = ", time.asctime(time.gmtime()))
    
    


image_delta = true_image.copy()
ld_delta = image_delta.load()
for i in range(0,len(list_of_delta_points)):
    ld_delta.__setitem__((list_of_delta_points[i][0],list_of_delta_points[i][1]),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0]+1,list_of_delta_points[i][1]),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0],list_of_delta_points[i][1]+1),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0],list_of_delta_points[i][1]-1),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0]-1,list_of_delta_points[i][1]),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0]+2,list_of_delta_points[i][1]),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0],list_of_delta_points[i][1]+2),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0],list_of_delta_points[i][1]-2),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0]-2,list_of_delta_points[i][1]),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0],list_of_delta_points[i][1]+3),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0]+3,list_of_delta_points[i][1]),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0]-3,list_of_delta_points[i][1]),(0,225,255))
    ld_delta.__setitem__((list_of_delta_points[i][0],list_of_delta_points[i][1]-3),(0,225,255))
    

image_delta.show()
image_delta.save("delta.png")



image_for_shadow = Image.new("RGB",image.size)
ld_shadow = image_for_shadow.load()
list_of_delta_value = []
for i in range(0,len(list_of_delta_points)):
    list_of_delta_value.append(max(true_image.getpixel((i,j))))

for i in range (0,len(list_groups)):
    for j in range(0,len(list_groups[i])):
        if max(true_image.getpixel(list_groups[i][j]))<list_of_delta_value[i]:
            ld_shadow.__setitem__((list_groups[i][j]),(255,0,255))
        else:
            ld_shadow.__setitem__((list_groups[i][j]),(0,0,150))

for i in range(0,len(list_circle)):
    ld_shadow.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0]+1,list_circle_eq[i][1]),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]+1),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0]-1,list_circle_eq[i][1]),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]-1),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]+2),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0]+2,list_circle_eq[i][1]),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0]-2,list_circle_eq[i][1]),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]-2),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0]+3,list_circle_eq[i][1]),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]+3),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0]-3,list_circle_eq[i][1]),(255,255,255))
    ld_shadow.__setitem__((list_circle_eq[i][0],list_circle_eq[i][1]-3),(255,255,255))
    ld_shadow.__setitem__((light_points[i][0],light_points[i][1]),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0]+1,light_points[i][1]),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0],light_points[i][1]+1),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0]-1,light_points[i][1]),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0],light_points[i][1]-1),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0]+2,light_points[i][1]),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0],light_points[i][1]+2),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0]-2,light_points[i][1]),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0],light_points[i][1]-2),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0]+3,light_points[i][1]),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0],light_points[i][1]+3),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0]-3,light_points[i][1]),(255,215,0))
    ld_shadow.__setitem__((light_points[i][0],light_points[i][1]-3),(255,215,0))


image_for_shadow.show()        
image_for_shadow.save("shadow.png")



midpoints_x=[]
midpoints_y=[]
midpoints_z=[]
for i in range(0,len(list_of_delta_points)):
    light_x = light_points[i][0]
    light_y = light_points[i][1]
    light_z = -list_of_3d_vectors[i][2]
    midpoint_x = (light_x+list_of_delta_points[i][0])/2
    midpoint_y = (light_y+list_of_delta_points[i][1])/2
    midpoint_z = light_z/2
    midpoints_x.append(midpoint_x)
    midpoints_y.append(midpoint_y)
    midpoints_z.append(midpoint_z)
    
    
    dist_from_midway = np.sqrt(2*((midpoint_x-light_x)**2+(midpoint_y-light_y)**2+(midpoint_z)**2))
    list_of_height.append(dist_from_midway)
    
    
    
if GET_TIME:
    print("Done Calculating height")
    print("TIME = ", time.asctime(time.gmtime()))


list_of_areas = []
list_of_area_true = []
list_of_shadow = []
list_of_shadow_true = []
sphere_true_ray = 1
for i in range(0,len(list_of_height)):
    area = 2*np.pi*list_of_height[i]*list_circle_eq[i][2]
    list_of_areas.append(area)
    list_of_area_true.append((sphere_true_ray**2)*np.pi*2*list_of_height[i])



    whole_sphere = 4*np.pi*(list_circle_eq[i][2])**2
    shadow = (whole_sphere-area)
    list_of_shadow_true.append(4*np.pi*(sphere_true_ray)**2-list_of_area_true[i])
    list_of_shadow.append(shadow)


if GET_TIME:
    print("Done Calculating area and shadow")
    print("TIME = ", time.asctime(time.gmtime()))



xm = np.mean(loss_x)
ym = np.mean(loss_y)
xs = 0
ys = 0
for i in range(0,len(loss_x)):
    xs = xs + (loss_x[i]-xm)**2
    ys = ys + (loss_y[i]-ym)**2

xs = np.sqrt(xs)
ys = np.sqrt(ys)



number_of_found_spheres = len(list_groups)

list_circle_ray = []
list_of_x_values = []
list_of_y_values = []
list_of_z_values = []
for i in range(0,number_of_found_spheres):
    list_circle_ray.append(list_circle_eq[i][2])
    list_of_x_values.append(list_of_3d_vectors[i][0])
    list_of_y_values.append(list_of_3d_vectors[i][1])
    list_of_z_values.append(list_of_3d_vectors[i][2])


if REPORT:
    f = open("report.txt","w")
    f.write("NUMBER OF SPHERES = ")
    f.write(str(len(list_groups)))
    f.write("\n")
    
    f.write("AVERAGE RAY (in pixels) = ")
    average_ray = np.mean(list_circle_ray)
    f.write(str(average_ray))
    f.write("\n")
    f.write("AVERAGE SIZE OF LIGHTENED AREA = ")
    if sphere_true_ray!=1:
        average_size_of_lightened_areas = np.mean(list_of_area_true)
    else:
        average_size_of_lightened_areas = np.mean(list_of_areas)
    f.write(str(average_size_of_lightened_areas))
    f.write("\n")
    f.write("AVERAGE SIZE OF SHADOWED AREA = ")
    if sphere_true_ray!=1:
        average_size_of_shadowed_area = np.mean(list_of_shadow_true)
    else:
        average_size_of_shadowed_area = np.mean(list_of_shadow)
    f.write(str(average_size_of_shadowed_area))
    f.write("\n")
    f.write("Percentage of lightened area = ")
    percent = average_size_of_lightened_areas/(average_size_of_shadowed_area+average_size_of_lightened_areas)*100
    f.write(str(percent)+" %")
    f.write("\n")
    f.write("AVERAGE RATIO OF LOST INTENSITY = ")
    average_loss = np.mean(list_loss)/len(list_groups)
    f.write(str(average_loss))
    f.write("\n")
    f.write("Percentage = ")
    f.write(str((average_loss/LIGHTEST_COLOR_INTENSITY)*100))
    f.write("\n")
    f.write("AVERAGE VECTOR ANGULUS COORDINATES:\n X coordinates : ")
    f.write(str(np.mean(list_of_x_values)))
    f.write("\n Y coordinates : ")
    f.write(str(np.mean(list_of_y_values)))
    f.write("\n Z coordinates : ")
    f.write(str(np.mean(list_of_y_values)))
    f.write("\n")
    f.write("AVERAGE DISPERSION (through square loss function) :\n")
    f.write("(If lower than 10 it should be a close enough accuracy)")
    f.write("\n X coordinate from lightest point :")
    f.write(str(xs))
    f.write("\n Y coordinate from lightest point  :")
    f.write(str(ys))
    f.close()

    
 




if DETAILLED_REPORT:
    f = open("detailled_report.txt","w")
    for i in range(0,len(list_groups)):
        f.write("Sphere number : "+str(i+1)+" \n\n")
        f.write("Ray (in pixel) : ")
        f.write(str(list_circle_eq[i][2])+" \n")
        f.write("Size of lightened area (in square pixel) : ")
        lightened_area = list_of_areas[i]
        f.write(str(lightened_area)+" \n")
        if sphere_true_ray !=1:
            f.write("Size of lightened area (in square size of ray's unit) : ")
            f.write(str(list_of_area_true[i])+" \n")
        shadowed_area = list_of_shadow[i]
        f.write("Size of shadowed area (in square pixel) : ")
        f.write(str(shadowed_area)+" \n")
        if sphere_true_ray !=1:
            f.write("Size of shadowed area (in square size of ray's unit') : ")
            f.write(str(list_of_shadow_true[i])+" \n")
        f.write("Percentage of lightened area : ")
        f.write(str((lightened_area*100)/(lightened_area+shadowed_area))+" % \n")
        f.write("Lost light intensity at lightest point :\n")
        f.write(" (in RGB intensity values compared to the original color) \n")
        f.write(str(-LIGHTEST_COLOR_INTENSITY-list_loss[i])+"\n")
        f.write("Ratio of light intensity lost : ")
        f.write(str((LIGHTEST_COLOR_INTENSITY - list_loss[i])/LIGHTEST_COLOR_INTENSITY)+"\n")
        f.write("Percentage : ")
        f.write(str(100*(LIGHTEST_COLOR_INTENSITY-list_loss[i])/LIGHTEST_COLOR_INTENSITY)+" %\n")
        f.write("Vector coordinates : \n")
        f.write("X coordinates :")
        f.write(str(list_of_3d_vectors[i][0])+" \n")
        f.write("Y coordinates :")
        f.write(str(list_of_3d_vectors[i][1])+" \n")
        f.write("Z coordinates :")
        f.write(str(list_of_3d_vectors[i][2])+" \n")
        f.write("Local loss for the lightest point :\n")
        f.write("X axis : ")
        f.write(str((loss_x[i]-np.mean(loss_x))**2))
        f.write("\nY axis : ")
        f.write(str((loss_x[i]-np.mean(loss_x))**2))
        f.write("\n____________________________\n")
        
    f.write("##############################")
    f.close()





img_new.save("Trace.png")
img_new.show()

if GET_TIME:
    print("End of treatment")
    print("TIME = ", time.asctime(time.gmtime()))
