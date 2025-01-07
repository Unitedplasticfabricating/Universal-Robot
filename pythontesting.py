import math
pi = 3.14159265358979
# this function takes two rotation matrices, and multiplies them together, returning one matrix. 
# all matrices are in the form of a list.
# all matrix values have constant values (no variables)
def multiply_matrix(matrix1, matrix2):
    # retrieve values
    a11 = matrix1[0]
    a12 = matrix1[1]
    a13 = matrix1[2]
    a21 = matrix1[3]
    a22 = matrix1[4]
    a23 = matrix1[5]
    a31 = matrix1[6]
    a32 = matrix1[7]
    a33 = matrix1[8]
    b11 = matrix2[0]
    b12 = matrix2[1]
    b13 = matrix2[2]
    b21 = matrix2[3]
    b22 = matrix2[4]
    b23 = matrix2[5]
    b31 = matrix2[6]
    b32 = matrix2[7]
    b33 = matrix2[8]
    #calculate c values
    c11 = a11*b11 + a12*b21 + a13*b31
    c12 = a11*b12 + a12*b22 + a13*b32
    c13 = a11*b13 + a12*b23 + a13*b33
    c21 = a21*b11 + a22*b21 + a23*b31
    c22 = a21*b12 + a22*b22 + a23*b32
    c23 = a21*b13 + a22*b23 + a23*b33
    c31 = a31*b11 + a32*b21 + a33*b31
    c32 = a31*b12 + a32*b22 + a33*b32
    c33 = a31*b13 + a32*b23 + a33*b33
    # return resulting matrix
    ret = [c11, c12, c13, c21, c22, c23, c31, c32, c33]
    return ret

# this function converts a matrix to axis angle representations
# this matrix is usually a resulting matrix (result of matrix multiplication) in normal use, given as a list
# returns a list of [rx,ry,rz]
def convert_matrix_to_axang(matrix1):
    # retrieve values
    a11 = matrix1[0]
    a12 = matrix1[1]
    a13 = matrix1[2]
    a21 = matrix1[3]
    a22 = matrix1[4]
    a23 = matrix1[5]
    a31 = matrix1[6]
    a32 = matrix1[7]
    a33 = matrix1[8]
    
    # First Half: find the angle    
    # find the trace
    # using the formula: trace = a11 + a22 + a33
    trace = a11 + a22 + a33
    # find the angle using the formula: trace(matrix) = 1 + 2 cos(angle)
    angle = math.acos((trace - 1.0)/2.0)
    
    # Second Half: calculate the rotation axis
    axisxraw = a32 - a23
    axisyraw = a13 - a31
    axiszraw = a21 - a12
    # normalize axis
    magnitude = math.sqrt(axisxraw*axisxraw + axisyraw*axisyraw + axiszraw*axiszraw)
    axisxunit = axisxraw / magnitude
    axisyunit = axisyraw / magnitude
    axiszunit = axiszraw / magnitude
    
    # combine axis and angle into rxryrz representation
    rxout = axisxunit * angle
    ryout = axisyunit * angle
    rzout = axiszunit * angle
    return [rxout, ryout, rzout]
    
# this function takes a rotation and calculates the corresponding rotation matrix
# input is (axis, direction, angle in radians)
# example is ("x", 1, pi/6) = a 30 degree turn around the x axis in the positive direction (right hand rule)
# returns a matrix (a list of 9 values)
def get_rotation_matrix_from_description(axis, direction, angle):
    # get the angle
    a = angle * direction
    # get the axis
    if axis == "x" or axis == "X":
        matrix = [1, 0, 0, 0, math.cos(a), -1 * math.sin(a), 0, math.sin(a), math.cos(a)]
        return matrix
    
    if axis == "y" or axis == "Y":
        matrix = [math.cos(a), 0, math.sin(a), 0, 1, 0, -1*math.sin(a), 0, math.cos(a)]
        return matrix
    
    if axis == "z" or axis == "Z":
        matrix = [math.cos(a), -1*math.sin(a), 0, math.sin(a), math.cos(a), 0, 0, 0, 1]
        return matrix

def main_calculate_right_extended(p11, p12, p21, p22, p3, p13, p23, chamferover, tcp_pose_top):
    struct1 = analyze_touchpoints_only(p11, p12, p21, p22, p3)
    list1 = analyze_vertical_touchpoints(p11, p12, p13, p21, p22, p23, p3)
    struct2 = calculate_DOtA_points_right_extended(struct1, list1, chamferover, tcp_pose_top)
    #validity = check_validity_right(struct1, struct2)
    return struct2

def analyze_touchpoints_only(p11, p12, p21, p22, p3):
  # FIND THE INTERSECTION
  # comment get the z
  zcoord=p3[2]

  # get the raw points from the first line
  l1p1x=p11[0]
  l1p1y=p11[1]
  l1p2x=p12[0]
  l1p2y=p12[1]

  # equate the first line in 2d space
  ml1 = (l1p2y-l1p1y) / (l1p2x-l1p1x)

  # b = y - mx
  bl1 = l1p1y - ml1 * l1p1x

  # get the raw points from the second line
  l2p1x=p21[0]
  l2p1y=p21[1]
  l2p2x=p22[0]
  l2p2y=p22[1]

  # equate the second line in 2d space
  ml2 = (l2p2y-l2p1y) / (l2p2x-l2p1x)

  # b = y - mx
  bl2 = l2p1y - ml2 * l2p1x


  # find the intersection of the two lines
  # m1x+b1 = m2x+b2
  # m1x - m2x = b2 - b1
  # x = (b2-b1) / (m1-m2)
  xintersect = (bl2-bl1) / (ml1-ml2)
  yintersect = ml1 * xintersect + bl1
  
  pointintersect = [xintersect,yintersect,zcoord,0,0,0]
  
  #FIND THE VECTORS
  #define a vector from the intersection to the second point on the first line
  l1delxfull = l1p2x - xintersect
  l1delyfull = l1p2y - yintersect

  l1delmag = math.sqrt(l1delxfull*l1delxfull + l1delyfull*l1delyfull)

  l1delxunit = l1delxfull / l1delmag
  l1delyunit = l1delyfull / l1delmag
  
  #define a vector from the intersection to the second point on the second line
  l2delxfull = l2p2x - xintersect
  l2delyfull = l2p2y - yintersect

  l2delmag = math.sqrt(l2delxfull*l2delxfull + l2delyfull*l2delyfull)

  l2delxunit = l2delxfull / l2delmag
  l2delyunit = l2delyfull / l2delmag
  
  #FIND HEADINGS
  #for each heading, find the angle of the line with respect to the pos x axis. then add/subtract 90 degrees because you want to be perpendicular to that
  headingvector1 = convert_uv_to_heading(l1delxunit, l1delyunit)
  headingvector2 = convert_uv_to_heading(l2delxunit, l2delyunit)
  # find halfway heading
  heading2 = (headingvector1 + headingvector2)/2
  # find headings that the robot should face while traveling, perpendicular to the vectors of the sides of the box
  heading1 = headingvector1 + pi/2
  heading3 = headingvector2 - pi/2
  
  #RETURN STRUCT
  ret = (pointintersect, heading1, heading2, heading3, l1delxunit, l1delyunit, l2delxunit, l2delyunit)
  return ret
  
def analyze_vertical_touchpoints(p11, p12, p13, p21, p22, p23, p3):
    # first, find the equations of the planes from the 6 points
    plane1 = findplane(p11, p12, p13)
    plane2 = findplane(p21, p22, p23)
    # Find the Direction Vector of the Line: The direction vector d of the line of intersection can be found by taking the cross product of the normal vectors of each plane (a, b, and c)
    nx = plane1[1]*plane2[2] - plane1[2]*plane2[1]
    ny = plane1[2]*plane2[0] - plane1[0]*plane2[2]
    nz = plane1[0]*plane2[1] - plane1[1]*plane2[0]
    # normalize the vector so the z length is 1
    multiplier = 1 / nz
    nx = nx * multiplier
    ny = ny * multiplier
    nz = nz * multiplier # should become equal to 1
    ret = [nx, ny]
    return ret


# given 3 points, this finds the plane and its equation
# rereturns ax + by + cz + d = 0 in a list of [a, b, c, d]
def findplane(p11, p12, p13):
    # extract coordinates
    x1 = p11[0]
    y1 = p11[1]
    z1 = p11[2]
    x2 = p12[0]
    y2 = p12[1]
    z2 = p12[2]
    x3 = p13[0]
    y3 = p13[1]
    z3 = p13[2]
    # create vectors from the points
    v1x = x2-x1
    v1y = y2-y1
    v1z = z2-z1
    v2x = x3-x1
    v2y = y3-y1
    v2z = z3-z1
    #calculate the normal vector using the cross product
    nx = v1y*v2z - v1z*v2y # i component
    ny = v1z*v2x - v1x*v2z # j component
    nz = v1x*v2y - v1y*v2x # k component
    # calculate d in the plane equation
    d = -1 * (nx*x1 + ny*y1 + nz*z1)
    ret = [nx, ny, nz, d]
    return ret
    
def convert_uv_to_heading(uvx, uvy):
  baseang = math.atan(uvy/uvx)
  if uvx < 0:
    ang = baseang + pi
  elif uvy < 0:
    ang = baseang + pi * 2
  else:
    ang = baseang
  
  return ang
  
def calculate_DOtA_points_right_extended(struct1, listleans, chamferover, tcp_pose_top):
    # get the stuff from the struct
    pointintersect = struct1[0]
    heading1 = struct1[1]
    heading2 = struct1[2]
    heading3 = struct1[3]
    l1delxunit = struct1[4]
    l1delyunit = struct1[5]
    l2delxunit = struct1[6]
    l2delyunit = struct1[7]
    
    # FIND THE POINTS ON THE LINES OF THE FIRST TURN PATH
    # find locations 8 inches away from  intersect point
    # CONST
    # welddistance1 = 8 # vertical weld distance
    welddistance2 = 6 # first path second leg
    welddistance3 = 8 # second path second leg
    zup = .375
    # inches
    # wd1 = welddistance1 * 25.4 / 1000
    wd2 = welddistance2 * 25.4 / 1000
    wd3 = welddistance3 * 25.4 / 1000
    zup = zup * 25.4 / 1000
    chamferovermm =  chamferover * 25.4 / 1000
    
    # weld distance is the distance that it will weld. this will make it start at the z height that the user specified
    wd1 = tcp_pose_top[2] - pointintersect[2] - zup 
    
    x = pointintersect[0] + l1delxunit * chamferovermm
    y = pointintersect[1] + l1delyunit * chamferovermm
    z = pointintersect[2] + zup
    
    #apply actual rxryrz to points
    # convert the headings to rxryrz and insert those values into the relevant points
    rxryrz = convert_heading_to_axang_preheatdown(heading1)
    rx = rxryrz[0]
    ry = rxryrz[1]
    rz = rxryrz[2]
    
    point1 = [x + wd1*listleans[0], y + wd1*listleans[1], z + wd1, rx, ry, rz] # add in the listleans factor to follow the face of the box as we move up
    point2 = [x, y, z, rx, ry, rz]
    
    # convert the headings to rxryrz and insert those values into the relevant points
    rxryrz = convert_heading_to_axang_ccw(heading1)
    rx = rxryrz[0]
    ry = rxryrz[1]
    rz = rxryrz[2]
    
    point4 = [x, y, z, rx, ry, rz]
    x = x + l1delxunit * wd2
    y = y + l1delyunit * wd2
    point5 = [x, y, z, rx, ry, rz]
    
    # FIND THE POINTS ON THE LINES OF THE SECOND AROUND PATH
    roundoverdistance = 0.05
    rod = roundoverdistance * 25.4 / 1000
    
    # now we have the unit vector. extend the weld distance from the intersection
    x = pointintersect[0] + l1delxunit * chamferovermm
    y = pointintersect[1] + l1delyunit * chamferovermm
    # convert the headings to rxryrz and insert those values into the relevant points
    rxryrz = convert_heading_to_axang(heading1)
    rx = rxryrz[0]
    ry = rxryrz[1]
    rz = rxryrz[2]
    point_1 = [x, y, z, rx, ry, rz]

    x = pointintersect[0] + l1delxunit * rod
    y = pointintersect[1] + l1delyunit * rod
    point_2 = [x, y, z, rx, ry, rz]

    # convert the headings to rxryrz and insert those values into the relevant points
    rxryrz = convert_heading_to_axang(heading3)
    rx = rxryrz[0]
    ry = rxryrz[1]
    rz = rxryrz[2]
    
    x = pointintersect[0] + l2delxunit * rod
    y = pointintersect[1] + l2delyunit * rod
    point_4 = [x, y, z, rx, ry, rz]
    
    # extend the weld distance from the intersection
    valid1 = True
    # start with the seed
    x = pointintersect[0] + l2delxunit * wd3
    y = pointintersect[1] + l2delyunit * wd3
    point_5 = [x, y, z, rx, ry, rz]
    seed = [x, y, z, rx, ry, rz]
    valid1 = get_inverse_kin_has_solution(seed)
    # define the increment
    increment = 1.0 # inches
    increment = increment * 25.4 / 1000 # meters
    while valid1 == True:
        wd3 = wd3 + increment
        x = pointintersect[0] + l2delxunit * wd3
        y = pointintersect[1] + l2delyunit * wd3
        seed = [x, y, z, rx, ry, rz]
        valid1 = get_inverse_kin_has_solution(seed)
        print(seed)
    
    # move back 1 to get the highest valid wd3
    # move back 3 to get the third highest valid wd3
    wd3 = wd3 - (3.0 * increment)
    x = pointintersect[0] + l2delxunit * wd3
    y = pointintersect[1] + l2delyunit * wd3
    point_5 = [x, y, z, rx, ry, rz]
    print(point_5)
    #FIND POINT 3
    # by calling analyze_touchpoints()
    #atret = analyze_touchpoints(point_2, point_1, point_4, point_5, pointintersect)
    #point_3 = atret[5]
    
    
    #struct2 = struct(point1=point1, point2=point2, point4=point4, point5=point5, point_1=point_1, point_2=point_2, point_3=point_3, point_4=point_4, point_5=point_5)
    #return struct2
    
def get_inverse_kin_has_solution(seed):
    if seed[0] > -1.5:
        return True
    return False
    
def convert_heading_to_axang_preheatdown(heading):
 axisxraw = -1*math.sin(heading) - 1
 axisyraw = math.cos(heading)
 axiszraw = -1*math.cos(heading)
 
 magnitude = math.sqrt(axisxraw*axisxraw + axisyraw*axisyraw + axiszraw*axiszraw)
 
 axisxunit = axisxraw / magnitude
 axisyunit = axisyraw / magnitude
 axiszunit = axiszraw / magnitude
 
 angle = math.acos( (math.sin(heading) - 1) / 2 )
 
 rxout = axisxunit * angle
 ryout = axisyunit * angle
 rzout = axiszunit * angle
 
 return [rxout, ryout, rzout]
 
def convert_heading_to_axang_ccw(heading):
 axisxraw = -1*math.sin(heading) 
 axisyraw = math.cos(heading) - 1
 axiszraw = -1*math.sin(heading) 
 
 magnitude = math.sqrt(axisxraw*axisxraw + axisyraw*axisyraw + axiszraw*axiszraw)
 
 axisxunit = axisxraw / magnitude
 axisyunit = axisyraw / magnitude
 axiszunit = axiszraw / magnitude
 
 angle = math.acos( (-1*math.cos(heading) - 1) / 2 )
 
 rxout = axisxunit * angle
 ryout = axisyunit * angle
 rzout = axiszunit * angle
 
 return [rxout, ryout, rzout]
 
def convert_heading_to_axang(heading):
 axisxraw = -1 * math.sin(heading)
 axisyraw = math.cos(heading) + 1
 axiszraw = math.sin(heading)

 magnitude = math.sqrt(axisxraw*axisxraw + axisyraw*axisyraw + axiszraw*axiszraw)

 axisxunit = axisxraw / magnitude
 axisyunit = axisyraw / magnitude
 axiszunit = axiszraw / magnitude

 angle = math.acos( (math.cos(heading) - 1) / 2 )

 rxout = axisxunit * angle
 ryout = axisyunit * angle
 rzout = axiszunit * angle
 
 return [rxout, ryout, rzout]
    

    

matrix1 = get_rotation_matrix_from_description("x", -1, 10 * pi/180)
matrix2 = get_rotation_matrix_from_description("z", 1, 25 * pi/180)
matrixfinal = multiply_matrix(matrix2, matrix1)
print(convert_matrix_to_axang(matrixfinal))



headingangle = 225 * pi / 180.0
ha = headingangle

matrix3 = [math.cos(ha), -1 * math.sin(ha), 0, math.sin(ha), math.cos(ha), 0, 0, 0, 1]
matrix4 = [0, 0, 1, 0, 1, 0, -1, 0, 0]
matrix5 = multiply_matrix(matrix3, matrix4)
print(convert_matrix_to_axang(matrix5))

# test out main calculate right
p11 = [-1.22721, .21026, .07259, 0, 0, 0]
p12 = [-1.31502, .33475, .07266, 0, 0, 0]
p13 = [-1.22720, .21025, .08259, 0, 0, 0]
p21 = [-1.24758, .07837, .07253, 0, 0, 0]
p22 = [-1.37227, -.00915, .07292, 0, 0, 0]
p23 = [-1.247581, .078371, .08253, 0, 0, 0]
p3 = [0, 0, .02, 0, 0, 0]
chamferover = .375
tcp_pose_top = [-1.247581, .078371, .08253, 0, 0, 0]
main_calculate_right_extended(p11, p12, p21, p22, p3, p13, p23, chamferover, tcp_pose_top)
