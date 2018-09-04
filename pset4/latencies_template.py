###################################
##########  PROBLEM 4-4 ###########
###################################
#
# PART A: Fill in the code for part a
#
def latencies(N, L):
    """
    Compute the latencies between every pair of servers in the 6006LE network.
    The servers are numbered with IDs from 0...N-1.

    Parameters
    ----------
    N : int
        number of servers in the network
    L : function
        L(i,j), where i and j are server IDs, will output the latency for the router connection between i and j. Latency must be a positive float value, in the range [0, float('inf')]

    Returns
    -------
    A : [][] (list of lists)
        N by N matrix, where A[i][j] is the latency of the shortest walk from i to j.
    """
    # YOUR CODE HERE
    A = [[L(y,x) for x in range(N)] for y in range(N)]
#    print("\n\n N=",N, "\n")
    # for z in range(N):
    #     for x in range(N):
    #         for y in range(N):
    #             A[z][x][y]=L(x,y)

    for z in range(N):
        #print(z)
        #print(A, "\n\n")
        for x in range(N):
            for y in range(N):
                if A[x][y]>A[x][z]+A[z][y]:
                    A[x][y]=A[x][z]+A[z][y]
                else:
                    A[x][y]=A[x][y]
    ans=A[:][:]
#    print ("Return: A=", ans)
    return ans

#
# PART B: Fill in the code for part b
#
def conservative_latencies(N, L):
    """
    Compute the latencies between every pair of servers in the 6006LE network.
    The servers are numbered with IDs from 0...N-1.

    Parameters
    ----------
    N : int
        number of servers in the network
    L : function
            L(i,j), where i and j are server IDs, will output the latency for the router connection between i and j. Latency must be a positive float value, in the range [0, float('inf')]

    Returns
    -------
    B : [][] (list of lists)
        N by N matrix, where B[i][j] is the latency of the SECOND shortest walk from i to j.
    """
    # YOUR CODE HERE
    A = [[L(y,x) for x in range(N)] for y in range(N)]
    B = [[float("inf") for x in range(N)] for y in range(N)]

#    print("\n\n N=",N, "\n")
    #for z in range(N+1):
    #    for x in range(N):
    #        for y in range(N):
    #            A[z][x][y]=L(x,y)

#    print ("Weights = ", A, "\n\n")
#    print ("B = ", B, "\n\n")
    for z in range(N):
        for x in range(N):
            for y in range(N):
#                print (" z = ", z, " x = ", x, " y = ",y)
                if A[x][y]>A[x][z]+A[z][y]:
#                    print (A[x][y], " > ", A[x][z], " + ", A[z][y])
                    B[x][y]=min(A[x][y],B[x][z]+A[z][y],A[x][z]+B[z][y])
                    A[x][y]=A[x][z]+A[z][y]

#                    print ("B[x][y] = ",  B[x][y])
                elif A[x][y]==A[x][z]+A[z][y]:
#                    print (A[x][y], " = ", A[x][z], " + ", A[z][y])
                    if z!=x and z!=y:
                        B[x][y]=A[x][y]
#                        A[x][y]=A[x][y]

                    elif x==z or y==z:
#                        A[x][y]=A[x][y]
                        B[x][y]=min(A[x][y]+B[x][x], A[x][y]+B[y][y], B[x][y]) #old path +loop
#                    print ("B[x][y] = ",  B[x][y])
                elif A[x][y]<A[x][z]+A[z][y]:
#                    print (A[x][y], " < ", A[x][z], " + ", A[z][y])
                    if B[x][y]>A[x][z]+A[z][y]:
                        B[x][y]=A[x][z]+A[z][y]
                        #A[x][y]=A[x][y]
#                        print ("B[x][y] = ",  B[x][y])
                    # else:
                    #     A[x][y]=A[x][y]
                    #     B[x][y]=B[x][y]


#                print ("B = ", B, "\n\n")
    for x in range (N):
        for y in range(N):
            for z in range(N):
                #B[x][y]=min(B[x][y], A[x][z] + B[z][z] + A[z][y])
                if B[x][y] > (A[x][z] + B[z][z] + A[z][y]):
                    B[x][y]= A[x][z] + B[z][z] + A[z][y] #checking if loop leads to second shortest path

#    print("A = ", A[z], "\n", "B = ", B, "\n\n")

    ans = B[:][:]
#    print ("Return: B=", ans)
    return ans
