# -*- coding: utf-8 -*-
"""
Created on Wed May 25 14:52:29 2022

@author: Moi
"""

# -*- coding: utf-8 -*-



import numpy as np
import time as time
import sys

from PIL import Image, ImageOps, ImageFilter


LIGHTEST_COLOR_INTENSITY = 255

list_groups = []
list_pixel = []

print("BEGINNING CALCULUS")
print("TIME = ", time.asctime(time.gmtime()))
image=Image.open("im_514_mk.jpg")
print(image.size)
for i in range(0,image.width):
    for j in range(0, image.height):
        if image.getpixel((i,j))>200:
            list_pixel.append((i,j))
            ###find_neighbour(i,j,list_groups)
            
print("DONE LINEARISING")
print("TIME = ", time.asctime(time.gmtime()))

list_pixel_sorted = sorted(list_pixel)

#print(list_pixel_sorted)


#list_pixel = [(0,1),(0,2),(0,3),(1,1),(1,2),(1,4)]

for i in range(0,len(list_pixel)):
    found_neighbour = False
    value = -1
    #print("CUR PIXEL"+str(list_pixel[i]))
    for j in range(0,len(list_groups)):
        #print(len(list_groups))
        #print(j)
        #print(list_groups[j])
        #print(((0,1)in list_groups[j]))
        #print(((list_pixel[i][0] -1, list_pixel[i][1])in list_groups[j]))
        if (list_pixel[i][0] -1, list_pixel[i][1]) in list_groups[j]:
            #print("here0")
            if not found_neighbour:
                #print("found0")
                list_groups[j].append(list_pixel[i])
                found_neighbour = True
                value = j
            else:
                if value !=j:
                    #print("foundElse0")
                    list_groups[value].extend(list_groups[j])
                    #print("b")
                    #print(list_groups)
                    del(list_groups[j])
                    #print(list_groups)
                    #print("e")
                    j-=1

        #print("222222222222222222")
        #print(((0,1)in list_groups[j]))
        #print(((list_pixel[i][0], list_pixel[i][1] -1)in list_groups[j]))

        if (list_pixel[i][0], list_pixel[i][1] -1) in list_groups[j]:
            #print("here1")
            if not found_neighbour:
                #print("found1")
                list_groups[j].append(list_pixel[i])
                found_neighbour = True
                value = j
            else:
                if value != j:
                    #print("foundelse1")
                    list_groups[value].extend(list_groups[j])
                    #print("b")
                    #print(list_groups)
                    del(list_groups[j])
                    #print(list_groups)
                    #print("e")
                    j-=1
    #print(list_groups)
    if value == -1:
        #print("add")
        list_groups.append([list_pixel[i]])
        
print("DONE GENERATING GROUPS")
print("TIME = ", time.asctime(time.gmtime()))

border = []


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


print("DONE CALCULATING BORDERS")
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
    #print(i)
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
            
            
                
        
    ###toDel = toDel[:-1]
    toDel.reverse()
    for j in range(0, len(toDel)):
        del(i[toDel[j]])
    ###debug purpose:
    ###break
      
print("DONE ELIMINATING SIDE EFFECTS OF BORDERS")
print("TIME = ", time.asctime(time.gmtime()))
    
#print(border)
#print(len(border[0]))


img_new = Image.new('RGB',image.size)
ld = img_new.load()


for i in range(0,len(list_groups)):
    for j in range(0,len(list_groups[i])):
        ld.__setitem__(list_groups[i][j],(255,255,255))


for j in border:
    for i in j:
        ld.__setitem__(i,(0,255,0))

img_new.show()

########### SPECULARITY
########## Input
###########All groups in list_groups (list of list of tuples)
###########All borders in border (list of list of tuples)

########### Output
############ All specularity points in spec_points (list of tuples)
spec_points = []
true_image=Image.open("im_514.jpg")
true_grayscale = ImageOps.grayscale(true_image)
r,g,b = true_image.split()
list_loss = []

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
    spec_points.append(current_position)


for i in range(0,len(spec_points)):
    ld.__setitem__((spec_points[i][0],spec_points[i][1]),(100,100,100))
    ld.__setitem__((spec_points[i][0]+1,spec_points[i][1]),(100,100,100))
    ld.__setitem__((spec_points[i][0],spec_points[i][1]+1),(100,100,100))
    ld.__setitem__((spec_points[i][0]-1,spec_points[i][1]),(100,100,100))
    ld.__setitem__((spec_points[i][0],spec_points[i][1]-1),(100,100,100))
    ld.__setitem__((spec_points[i][0]+2,spec_points[i][1]),(100,100,100))
    ld.__setitem__((spec_points[i][0],spec_points[i][1]+2),(100,100,100))
    ld.__setitem__((spec_points[i][0]-2,spec_points[i][1]),(100,100,100))
    ld.__setitem__((spec_points[i][0],spec_points[i][1]-2),(100,100,100))
    ld.__setitem__((spec_points[i][0]+3,spec_points[i][1]),(100,100,100))
    ld.__setitem__((spec_points[i][0],spec_points[i][1]+3),(100,100,100))
    ld.__setitem__((spec_points[i][0]-3,spec_points[i][1]),(100,100,100))
    ld.__setitem__((spec_points[i][0],spec_points[i][1]-3),(100,100,100))



print("DONE CALCULATING SPECULARITY")
print("TIME = ", time.asctime(time.gmtime()))



true_image.close()
#true_grayscale.close()


print("CLOSED IMAGE")


########## Circle fitting equation calculus
########## Input
###########All groups in list_groups (list of list of tuples)
###########All borders in border (list of list of tuples)


########## Output
########## eq => One circle equation with (x_center, y_center, ray)
########## circles_eq list of circle_equations
########## circle_borders list of list of borders (through the equation)
########## disk_points (list of list of tuples)
################ => Parkour + calcul pour chaque point ray + petit ou pas
###########Objective
list_circle = []
list_circle_eq = []
theta = np.linspace(0, 2*np.pi, 360)
for cur_border in border:
    x_list = []
    y_list = []
    #trp_group = group.T
    for i in range(0,len(cur_border)):
        x_list.append(cur_border[i][0])
        y_list.append(cur_border[i][1])
    # == METHOD 1 ==
    method_1 = 'algebraic'
    
    
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
    for j in range(0,len(list_circle[i])):
        ld.__setitem__(list_circle[i][j],(0,0,255))

print("DONE CALCULATING LEAST SQUARE CIRCLE EQUATION")
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
for i in disk_points:
    for j in i:
        ld.__setitem__(j,(255,0,0))
"""
print("DONE COLORING DISKS")
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
    spec = spec_points[i]
    x_p = round(spec[0]) - round(eq[0])
    y_p = round(spec[1]) - round(eq[1])
    hypotenuse_2d_pow2 = x_p**2 + y_p**2
    z_p = round(np.sqrt((eq[2])**2 - hypotenuse_2d_pow2))
    loss_x.append(x_p)
    loss_y.append(y_p)
    """
    relative_intensity_mean = 
    relative_intensity_max = 
    relative_intensity_max = 
    """
    
    vector = (-x_p,-y_p,-z_p)
    list_of_3d_vectors.append(vector)
    
print("Done Calculating z-coordinate of spec point")    
print("TIME = ", time.asctime(time.gmtime()))
list_of_delta_points = []

"""
#Finding highest the two highest deltas on the border
for i in range(0,len(border)):
    cur_border = border [i]
    max_1 = 0
    max_2 = 0
    delta_1 = None
    delta_2 = None
    for j in range(0,len(cur_border)):
        left=True
        right=True
        top=True
        bottom=True
        pixel = cur_border[j]
        pixel_value = image.getpixel(pixel)
        if((pixel[0],pixel[1]+1) in cur_border):
            bottom = False
            local_delta = abs(pixel_value - image.getpixel((pixel[0],pixel[1]+1)))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0],pixel[1]+1))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0],pixel[1]+1))

        if((pixel[0],pixel[1]-1) in cur_border):
            top=False
            local_delta = abs(pixel_value - image.getpixel((pixel[0],pixel[1]-1)))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0],pixel[1]-1))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0],pixel[1]-1))

        if((pixel[0]+1,pixel[1]) in cur_border):
            right=False
            local_delta = abs(pixel_value - image.getpixel((pixel[0]+1,pixel[1])))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0]+1,pixel[1]))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0]+1,pixel[1]))
        
        if((pixel[0]-1,pixel[1]) in cur_border):
            left=False
            local_delta = abs(pixel_value - image.getpixel((pixel[0]-1,pixel[1])))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0]-1,pixel[1]))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0]-1,pixel[1]))
        if(left and top and (pixel[0]-1,pixel[1]-1) in cur_border):
            local_delta = abs(pixel_value - image.getpixel((pixel[0]-1,pixel[1]-1)))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0]-1,pixel[1]-1))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0]-1,pixel[1]-1))
        if(left and bottom and (pixel[0]-1,pixel[1]+1) in cur_border):
            local_delta = abs(pixel_value - image.getpixel((pixel[0]-1,pixel[1]+1)))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0]-1,pixel[1]+1))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0]-1,pixel[1]+1))
        if(right and top and (pixel[0]+1,pixel[1]-1) in cur_border):
            local_delta = abs(pixel_value - image.getpixel((pixel[0]+1,pixel[1]-1)))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0]+1,pixel[1]-1))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0]+1,pixel[1]-1))
        if(right and bottom and (pixel[0]+1,pixel[1]+1) in cur_border):
            local_delta = abs(pixel_value - image.getpixel((pixel[0]+1,pixel[1]+1)))
            if max_2<local_delta:
                if max_1<local_delta:
                    max_2 = max_1
                    delta_2 = delta_1
                    max_1 = local_delta
                    delta_1 = (pixel,(pixel[0]+1,pixel[1]+1))
                else:
                    max_2 = local_delta
                    delta_2 = (pixel,(pixel[0]+1,pixel[1]+1))
        
    list_of_delta_points.append((delta_1,delta_2))
"""

#Finding highest the highest deltas on the border
true_img = Image.open("im_514.jpg")
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
        pixel_value = max(true_img.getpixel(pixel))
        if((pixel[0],pixel[1]+1) in cur_border):
            bottom = False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0],pixel[1]+1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0],pixel[1]+1))
                
        if((pixel[0],pixel[1]-1) in cur_border):
            top=False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0],pixel[1]-1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0],pixel[1]-1))
            
        if((pixel[0]+1,pixel[1]) in cur_border):
            right=False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]+1,pixel[1]))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]+1,pixel[1]))
        if((pixel[0]-1,pixel[1]) in cur_border):
            left=False
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]-1,pixel[1]))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]-1,pixel[1]))
                
        if(left and top and (pixel[0]-1,pixel[1]-1) in cur_border):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]-1,pixel[1]-1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]-1,pixel[1]-1))
                
        if(left and bottom and (pixel[0]-1,pixel[1]+1) in cur_border):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]-1,pixel[1]+1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]-1,pixel[1]+1))
            
        if(right and top and (pixel[0]+1,pixel[1]-1) in cur_border):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]+1,pixel[1]-1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]+1,pixel[1]-1))
    
        if(right and bottom and (pixel[0]+1,pixel[1]+1) in cur_border):
            local_delta = abs(pixel_value - max(true_img.getpixel((pixel[0]+1,pixel[1]+1))))
            if max_1<local_delta:
                max_1 = local_delta
                delta_1 = (pixel,(pixel[0]+1,pixel[1]+1))
    x_c = spec_points[i][0]
    y_c = spec_points[i][1]
    val_1 = (x_c-delta_1[0][0])**2+(y_c-delta_1[0][1])**2
    val_2 = (x_c-delta_1[1][0])**2+(y_c-delta_1[1][1])**2
    
    if val_1>val_2 :
        list_of_delta_points.append(delta_1[1])
    else:
        list_of_delta_points.append(delta_1[0])

list_of_height = []

print("Done Calculating deltas")
print("TIME = ", time.asctime(time.gmtime()))
print(list_of_delta_points)
print(list_of_3d_vectors)

"""
for i in range(0,len(list_of_delta_points)):
    val_1 = (list_of_delta_points[i][0][0] - list_of_3d_vectors[i][0])**2 + (list_of_delta_points[i][0][1] - list_of_3d_vectors[i][0])**2
    val_2 = (list_of_delta_points[i][1][0] - list_of_3d_vectors[i][0])**2 + (list_of_delta_points[i][1][1] - list_of_3d_vectors[i][0])**2
    print(val_2-val_1)

    print(list_of_delta_points[i][0][0])
    print(list_of_delta_points[i][1][0])
    mid_point_x = (list_of_delta_points[i][0][0]+list_of_delta_points[i][1][0])/2
    mid_point_y = (list_of_delta_points[i][0][1]+list_of_delta_points[i][1][1])/2
    mid_point_z = 0
    height_value = np.sqrt((mid_point_x-list_of_3d_vectors[i][0])**2+(mid_point_y-list_of_3d_vectors[i][1])**2+(list_of_3d_vectors[i][2])**2)
    
    list_of_height.append(height_value)
"""
midpoints_x=[]
midpoints_y=[]
midpoints_z=[]
for i in range(0,len(list_of_delta_points)):
    spec_x = spec_points[i][0]
    spec_y = spec_points[i][1]
    spec_z = -list_of_3d_vectors[i][2]
    midpoint_x = (spec_x+list_of_delta_points[i][0])/2
    midpoint_y = (spec_y+list_of_delta_points[i][1])/2
    midpoint_z = spec_z/2
    midpoints_x.append(midpoint_x)
    midpoints_y.append(midpoint_y)
    midpoints_z.append(midpoint_z)
    
    
    dist_from_midway = np.sqrt(2*((midpoint_x-spec_x)**2+(midpoint_y-spec_y)**2+(midpoint_z)**2))
    list_of_height.append(dist_from_midway)
    
print("Done Calculating height")
print("TIME = ", time.asctime(time.gmtime()))


list_of_areas = []
list_of_area_true = []
list_of_shadow = []
list_of_shadow_true = []
sphere_true_ray = 1
for i in range(0,len(list_of_height)):
    area = 2*np.pi*list_of_height[i]*list_circle_eq[i][2]
    print(area)
    print((list_circle_eq[i][2]**2)*np.pi)
    area = area - (list_circle_eq[i][2]**2)*np.pi
    list_of_areas.append(area)
    list_of_area_true.append((sphere_true_ray**2)*np.pi)



    whole_sphere = 4*np.pi*(list_circle_eq[i][2])**2
    shadow = (whole_sphere-area)#round(whole_sphere - area)
    list_of_shadow_true.append(4*np.pi*(sphere_true_ray)**2-list_of_area_true[i])
    #list_of_areas.append(area)
    list_of_shadow.append(shadow)

print("Done Calculating area and shadow")
print("TIME = ", time.asctime(time.gmtime()))

print(list_of_shadow)

xm = np.mean(loss_x)
ym = np.mean(loss_y)
xs = 0
ys = 0
for i in range(0,len(loss_x)):
    xs = xs + (loss_x[i]-xm)**2
    ys = ys + (loss_y[i]-ym)**2

xs = np.sqrt(xs)
ys = np.sqrt(ys)

print(xs)
print(ys)

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

report=True
if(report == True):
    f = open("report.txt","w")
    f.write("NUMBER OF SPHERES = ")
    f.write(str(len(list_groups)))
    f.write("\n")
    #f.write("AVERAGE SIZE OF SPHERES = ")
    #average_sphere_ray = np.mean(list_circle_ray)
    #f.write(round((4*np.pi)*average_sphere_ray**2))
    #f.write("\n")
    
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
    average_size_of_lightened_areas/(average_size_of_shadowed_area+average_size_of_lightened_areas)*100
    f.write(" %")
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
    f.write("\n X coordinate from point of specularity :")
    f.write(str(xs))
    f.write("\n Y coordinate from point of specularity :")
    f.write(str(ys))
    f.close()

    
#average_shadow = np.mean(list_of_shadow)
#average_vector = np.mean(list_of_3d_vectors)
#average_light_intensity_loss = (LIGHTEST_COLOR_INTENSITY-np.mean(list_loss))/255
#average_percentage_of_loss = (np.mean(list_loss)-LIGHTEST_COLOR_INTENSITY)/255 /100

    



detailled_report = True
if detailled_report == True:
    f = open("detailled_report.txt","w")
    for i in range(0,len(list_groups)):
        f.write("Sphere number : "+str(i)+" \n\n")
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
        f.write("Lost light intensity at specularity point :\n")
        f.write(" (in RGB intensity values compared to the original color) \n")
        f.write(str(list_loss[i]))
        f.write("Ratio of light intensity lost : ")
        f.write(str((list_loss[i]-LIGHTEST_COLOR_INTENSITY)/LIGHTEST_COLOR_INTENSITY)+"\n")
        f.write("Percentage : ")
        f.write(str(100*(list_loss[i]-LIGHTEST_COLOR_INTENSITY)/LIGHTEST_COLOR_INTENSITY)+" %\n")
        f.write("Vector coordinates : \n")
        f.write("X coordinates :")
        f.write(str(list_of_3d_vectors[i][0])+" \n")
        f.write("Y coordinates :")
        f.write(str(list_of_3d_vectors[i][1])+" \n")
        f.write("Z coordinates :")
        f.write(str(list_of_3d_vectors[i][2])+" \n")
        f.write("Local loss for the specularity point :\n")
        f.write("X axis : ")
        f.write(str((loss_x[i]-np.mean(loss_x))**2))
        f.write("Y axis : ")
        f.write(str((loss_x[i]-np.mean(loss_x))**2))
        f.write("____________________________\n")
        
    f.write("##############################")
    f.close()


"""
img_new = Image.new('RGB',image.size)
ld = img_new.load()


for i in range(0,len(list_groups)):
    for j in range(0,len(list_groups[i])):
        if i==0:
            ld.__setitem__(list_groups[i][j],(255,255,255))
        if i==1:
            ld.__setitem__(list_groups[i][j],(255,0,0))
        if i==2:
            ld.__setitem__(list_groups[i][j],(0,255,0))
        if i==3:
            ld.__setitem__(list_groups[i][j],(0,0,255))
        if i==4:
            ld.__setitem__(list_groups[i][j],(0,255,255))
        if i==5:
            ld.__setitem__(list_groups[i][j],(255,0,255))
        if i==6:
            ld.__setitem__(list_groups[i][j],(255,255,0))
        if i==7:
            ld.__setitem__(list_groups[i][j],(100,100,100))
        if i==8:
            ld.__setitem__(list_groups[i][j],(100,255,100))
        if i==9:
            ld.__setitem__(list_groups[i][j],(100,100,255))
        if i==10:
            ld.__setitem__(list_groups[i][j],(255,100,100))
        if i==11:
            ld.__setitem__(list_groups[i][j],(0,100,255))
        if i==12:
            ld.__setitem__(list_groups[i][j],(100,0,255))
        if i==13:
            ld.__setitem__(list_groups[i][j],(255,100,0))
        if i==14:
            ld.__setitem__(list_groups[i][j],(255,0,100))
        if i==15:
            ld.__setitem__(list_groups[i][j],(180,0,155))
        if i==16:
            ld.__setitem__(list_groups[i][j],(0,180,155))
        if i==17:
            ld.__setitem__(list_groups[i][j],(155,180,0))
"""
img_new.save("Trace.png")
img_new.show()
#img_new.save("border_calcul_correct.png")
#img_new.save("grp_color.png")
#print(list_groups)
#print(len(list_groups))
print("TIME = ", time.asctime(time.gmtime()))