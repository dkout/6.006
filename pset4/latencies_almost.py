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
    A = [[[L(y,x) for x in range(N)] for y in range(N)] for z in range(N+1)]
#    print("\n\n N=",N, "\n")
    # for z in range(N):
    #     for x in range(N):
    #         for y in range(N):
    #             A[z][x][y]=L(x,y)

    for z in range(1,N+1):
        #print(z)
        #print(A, "\n\n")
        for x in range(N):
            for y in range(N):
                if A[z-1][x][y]>A[z-1][x][z-1]+A[z-1][z-1][y]:
                    A[z][x][y]=A[z-1][x][z-1]+A[z-1][z-1][y]
                else:
                    A[z][x][y]=A[z-1][x][y]
    ans=A[-1][:][:]
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
    A = [[[L(y,x) for x in range(N)] for y in range(N)] for z in range(N+1)]
    B = [[[float("inf") for x in range(N)] for y in range(N)] for z in range(N+1)]

#    print("\n\n N=",N, "\n")
    #for z in range(N+1):
    #    for x in range(N):
    #        for y in range(N):
    #            A[z][x][y]=L(x,y)

#    print ("Weights = ", A, "\n\n")
    for z in range(1,N+1):
#        print(z)
        for x in range(N):
            for y in range(N):
                if A[z-1][x][y]>A[z-1][x][z-1]+A[z-1][z-1][y]:
                    A[z][x][y]=A[z-1][x][z-1]+A[z-1][z-1][y]
                    B[z][x][y]=min(A[z-1][x][y],B[z-1][x][z-1]+A[z-1][z-1][y],A[z-1][x][z-1]+B[z-1][z-1][y])
                if A[z-1][x][y]==A[z-1][x][z-1]+A[z-1][z-1][y]:
                    if z-1!=x and z-1!=y:
                        A[z][x][y]=A[z-1][x][y]
                        B[z][x][y]=A[z-1][x][y]
                    elif x==z-1 or y==z-1:
                        A[z][x][y]=A[z-1][x][y]
                        B[z][x][y]=min(A[z][x][y]+B[z-1][x][x], A[z][x][y]+B[z-1][y][y], B[z-1][x][y]) #old path +loop
                if A[z-1][x][y]<A[z-1][x][z-1]+A[z-1][z-1][y]:
                    if B[z-1][x][y]>A[z-1][x][z-1]+A[z-1][z-1][y]:
                        B[z][x][y]=A[z-1][x][z-1]+A[z-1][z-1][y]
                        A[z][x][y]=A[z-1][x][y]
                    else:
                        A[z][x][y]=A[z-1][x][y]
                        B[z][x][y]=B[z-1][x][y]

    for x in range (N):
        for y in range(N):
            for z in range(N):
                B[-1][x][y]=min(B[-1][x][y], A[-1][x][z] + B[-1][z][z] + A[-1][z][y]) #checking if loop leads to second shortest path

#    print("A = ", A[z], "\n", "B = ", B, "\n\n")

    ans = B[-1][:][:]
#    print ("Return: B=", ans)
    return ans
