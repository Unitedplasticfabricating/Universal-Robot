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
        matrix = [1, 0, 0, 0, cos(a), -1 * sin(a), 0, sin(a), cos(a)]
        return matrix
    end
    if axis == "y" or axis == "Y":
        matrix = [cos(a), 0, sin(a), 0, 1, 0, -1*sin(a), 0, cos(a)]
        return matrix
    end
    if axis == "z" or axis == "Z":
        matrix = [cos(a), -1*sin(a), 0, sin(a), cos(a), 0, 0, 0, 1]
        return matrix
    end
end



matrix1 = [4,0,5,0,3,0,2,0,1]
matrix2 = [0,0,-1,0,1,0,1,0,0]


headingangle = 225 * pi / 180.0
ha = headingangle

matrix3 = [math.cos(ha), -1 * math.sin(ha), 0, math.sin(ha), math.cos(ha), 0, 0, 0, 1]
matrix4 = [0, 0, 1, 0, 1, 0, -1, 0, 0]
matrix5 = multiply_matrix(matrix3, matrix4)
print(convert_matrix_to_axang(matrix5))