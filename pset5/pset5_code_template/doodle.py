###################################
##########  PROBLEM 5-4 ###########
###################################

def double_kill(ghost1, ghost2):
    """
    Compute the shortest move sequence which will make both ghosts disappear.

    Parameters
    ----------
    ghost1: []
        ordered list of moves which will make ghost1 disappear
    ghost2: []
        ordered list of moves which will make ghost2 disappear

    Returns
    -------
    seq : []
        move sequence of minimal length which will make both ghosts disappear
    """
    #dp=[[(None, (0,0), 0)]]
    #initialize lists
    seq=[]
    dp = []

    #make array
    for x in range(len(ghost1)+1):
        dp.append([])
        for y in range(len(ghost2)+1):
            dp[x].append(0)

    dp[0][0] = (None, (0,0), 0)
    for y in range(len(ghost2)):
        y+=1
        dp[0][y] = (ghost2[len(ghost2)-y], (0, -1), y)
    for x in range(len(ghost1)):
        x+=1
        dp[x][0] = (ghost1[len(ghost1)-x], (-1, 0), x)



    for x in range(len(ghost1)):
        x+=1
        for y in range(len(ghost2)):
            y+=1
            if ghost1[len(ghost1)-x] == ghost2[len(ghost2)-y]:
                dp[x][y] = (ghost1[len(ghost1)-x], (-1, -1), dp[x-1][y-1][2]+1)
            else:

                if dp[x-1][y][2]<dp[x][y-1][2]:
                    dp[x][y] = (ghost1[len(ghost1)-x], (-1, 0), dp[x-1][y][2]+1)
                else:
                    dp[x][y] = (ghost2[len(ghost2)-y], (0, -1), dp[x][y-1][2]+1)

    #print (dp)
    i=len(ghost1)
    j=len(ghost2)
    i_new=i
    j_new=j

    while dp[i][j][0] is not None:
        #print (i, j)
        #print(dp[i][j])
        seq.append(dp[i][j][0])
        i_new+=dp[i][j][1][0]
        j_new+=dp[i][j][1][1]
        i=i_new
        j=j_new
    #seq.reverse()
    return seq

# #
# PART B: Fill in the code for part b
#

def triple_kill(ghost1, ghost2, ghost3):
    """
    Compute the shortest move sequence which will make all three ghosts disappear.

    Parameters
    ----------
    ghost1: []
        ordered list of moves which will make ghost1 disappear
    ghost2: []
        ordered list of moves which will make ghost2 disappear
    ghost3: []
        ordered list of moves which will make ghost3 disappear

    Returns
    -------
    seq : []
        move sequence of minimal length which will make all three ghosts disappear
    """

    g1=len(ghost1)
    g2=len(ghost2)
    g3=len(ghost3)

    seq=list()

    #make dp array
    dp=[]
    for x in range(g1+1):
        dp.append([])
        for y in range(g2+1):
            dp[x].append([])
            for z in range(g3+1):
                dp[x][y].append(0)


    #initialize corner
    dp[0][0][0]=(None, (0,0,0), 0)
    #initialize edges
    for x in range(1, g1+1):
        dp[x][0][0]=(ghost1[g1-x], (-1,0,0), x)
    for y in range(1, g2+1):
        dp[0][y][0]=(ghost2[g2-y], (0,-1,0), y)
    for z in range(1, g3+1):
        dp[0][0][z]=(ghost3[g3-z], (0,0,-1), z)

###INITIALIZE PLANES
    #ghost 1,2
    #print ("ghosts 1 and 2")
    for x in range(1, g1+1):
        for y in range(1, g2+1):
            if ghost1[g1-x] == ghost2[g2-y]:
                dp[x][y][0] = (ghost1[g1-x], (-1, -1, 0), dp[x-1][y-1][0][2]+1)
            else:
                if dp[x-1][y][0][2] < dp[x][y-1][0][2]:
                    dp[x][y][0] = (ghost1[g1-x], (-1,0,0), dp[x-1][y][0][2]+1)
                else:
                    dp[x][y][0] = (ghost2[g2-y], (0, -1,0), dp[x][y-1][0][2]+1)


    #print (dp[x][y][0])


    #ghost 2,3


        #print ("ghosts 2 and 3")
        for y in range(1, g2+1):
            for z in range(1, g3+1):
                #print ((g2-y,g3-z))
                if ghost2[g2-y] == ghost3[g3-z]:
                    dp[0][y][z] = (ghost2[g2-y], (0, -1, -1), dp[0][y-1][z-1][2]+1)
                else:
                    if dp[0][y-1][z][2] < dp[0][y][z-1][2]:
                        dp[0][y][z] = (ghost2[g2-y], (0,-1,0), dp[0][y-1][z][2]+1)
                    else:
                        dp[0][y][z] = (ghost3[g3-z], (0, 0,-1), dp[0][y][z-1][2]+1)


        #print (dp[0][y][z])


    #ghost 1,3


        #print ("ghosts 3 and 1")
        for z in range(1, g3+1):
            for x in range(1, g1+1):
                if ghost1[g1-x] == ghost3[g3-z]:
                    dp[x][0][z] = (ghost1[g1-x], (-1, 0, -1), dp[x-1][0][z-1][2]+1)
                else:
                    if dp[x][0][z-1][2] < dp[x-1][0][z][2]:
                        dp[x][0][z] = (ghost3[g3-z], (0,0,-1), dp[x][0][z-1][2]+1)
                    else:
                        dp[x][0][z] = (ghost1[g1-x], (-1, 0,0), dp[x-1][0][z][2]+1)


        #print (dp[x][0][z])


    #ghost 1,2,3

    for x in range(1, g1+1):
        for y in range(1, g2+1):
            for z in range (1, g3+1):
                prevbest=min( dp[x-1][y][z][2],dp[x][y-1][z][2], dp[x][y][z-1][2])
                if ghost1[g1-x]==ghost2[g2-y]==ghost3[g3-z] and dp[x-1][y-1][z-1][2] <prevbest:
                    dp[x][y][z]=(ghost1[g1-x], (-1,-1,-1), dp[x-1][y-1][z-1][2]+1)
                    #print("all ghosts")
                elif ghost1[g1-x]==ghost2[g2-y] and dp[x-1][y-1][z][2] <prevbest:
                    dp[x][y][z]=(ghost1[g1-x], (-1, -1, 0), dp[x-1][y-1][z][2]+1)
                elif ghost2[g2-y]==ghost3[g3-z] and dp[x][y-1][z-1][2] <prevbest:
                    dp[x][y][z]=(ghost2[g2-y], (0, -1, -1), dp[x][y-1][z-1][2]+1)
                elif ghost1[g1-x]==ghost3[g3-z] and dp[x-1][y][z-1][2] <prevbest:
                    dp[x][y][z]=(ghost1[g1-x], (-1,0,-1), dp[x-1][y][z-1][2]+1)

                else:
                    if dp[x-1][y][z][2]<dp[x][y-1][z][2]:
                        dp[x][y][z]=(ghost1[g1-x], (-1, 0, 0), dp[x-1][y][z][2]+1)
                    elif dp[x][y-1][z][2]<dp[x][y][z-1][2]:
                        dp[x][y][z]=(ghost2[g2-y], (0, -1, 0), dp[x][y-1][z][2]+1)
                    else:

                        dp[x][y][z]=(ghost3[g3-z], (0,0,-1), dp[x][y][z-1][2]+1)


    x=g1
    y=g2
    z=g3
    x_new=x
    y_new=y
    z_new=z

    while dp[x][y][z][0] is not None:
        #print (i, j)
        #print(dp[i][j])
        seq.append(dp[x][y][z][0])
        x_new+=dp[x][y][z][1][0]
        y_new+=dp[x][y][z][1][1]
        z_new+=dp[x][y][z][1][2]
        x=x_new
        y=y_new
        z=z_new
    #seq.reverse()
    return seq
