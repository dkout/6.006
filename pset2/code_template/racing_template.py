"""Main solution file for F1 Kart Racing."""

import heapq
import pdb

def compare(a, b):
    """
    Return True if a is smaller than b, or False, otherwise.

    Arguments:
        a (Fraction): The first fraction.
        b (Fraction): The second fraction.

    Return:
        bool: A boolean that is True if a < b, or False, otherwise.
    """
    if a.num*b.den<a.den*b.num:
        return True
    else:
        return False


class Fraction(object):
    """Class for fractions."""

    def __init__(self, num, den):
        """Construct a new fraction."""
        self.num = num
        self.den = den

    def __lt__(self, other):
        """Return True if self < other, or False otherwise."""
        return compare(self, other)

    def __str__(self):
        """Return textual representation of the fraction."""
        return str(self.num) + "/" + str(self.den)


def losetime(p_s, v_s, p_f, v_f, L):
    """
    Return the moment in time when (p_f, v_f) is going to take over (p_s, v_s).

    Arguments:
        p_s (int): The starting position of the slower kart.
        v_s (int): The velocity of the slower kart.
        p_f (int): The starting position of the faster kart.
        v_f (int): The velocity of the faster kart.
        L (int): The length of the track.

    Preconditions:
        (1) 0 <= p_s, p_f < L;
        (2) v_s < v_f
        (3) p_f != p_s

    Return:
        Fraction: The time when the faster kart (p_f, v_f) is going to take
            over the slower kart (p_s, v_s).
    """
    if p_s>p_f:
        return Fraction(p_s-p_f,v_f-v_s)
    else:
        return Fraction (L-p_f+p_s, v_f-v_s)

    return losetime

def remove(i, ahead, behind):
    """
    Update the (ahead, behind) data structure by removing competitor i.

    Note that this method does not return anything.

    Arguments:
        i (int): The id of the competitor.
        ahead (dict): A dictionary where the competitor ahead of competitor j
            is given by ahead[j].
        behind (dict): A dictionary where the competitor behind competitor j
            is given by behind[j].

    Preconditions:
        (1) i is present in both dictionaries.
        (2) for every competitor i present in either ahead or behind, we have
            i = ahead[behind[i]], as well as i = behind[ahead[i]]

    Return: Nothing.
    """
    if i not in ahead:
        del ahead[behind[i]]
    if i not in behind:
        del behind[ahead[i]]
    if i in behind and i in ahead:
        ahead[behind[i]]=ahead[i]
        behind[ahead[i]]=behind[i]
        del ahead[i]
        del behind[i]



def rank(N, L, velocity, position):
    """
    Compute the rank (as defined in the problem statement) of competitor 0.

    Arguments:
        N (int): The number of competitors.
        L (int): The length of the track.
        velocity (list[int]): The velocities of all competitors, where the
            velocity of competitor i (0 <= i < N) is given by velocity[i].
        position (list[int]): The starting positions of all competitors, where
            the starting position of competitor i (0 <= i < N) is given by
            position[i].

    Preconditions:
        (1) len(velocity) = len(position) = N
        (2) all elements of velocity are distinct, and non-negative
        (3) all elements of position are distinct, and non-negative

    Return: The rank of competitor 0, which is a number between 1 and N,
        inclusive.
    """

    #print ("\n\n\n position: ", position)
    #print ("velocity: ", velocity)
    #print("N, L = ", N, L)
    positions=dict() #maps position to contestant number
    ahead=dict()
    behind=dict()

    for j in range(len(position)):
        positions[position[j]]=j

    position_og=position[:]

    position.sort()
    for i in range(len(position)):
        j=positions[position[i]]
        if i==0:
            behind[j]=positions[position[-1]]
            ahead[j]=positions[position[i+1]]
        elif i==len(position)-1:
            ahead[j]=positions[position[0]]
            behind[j]=positions[position[i-1]]
        else:
            ahead[j]=positions[position[i+1]]
            behind[j]=positions[position[i-1]]

    #print ("position dictionary: ", positions)
    #print ("ahead = ", ahead)

    passtimes=[]
    heapq.heapify(passtimes)
    for i in ahead:
        if velocity[i]>velocity[ahead[i]]:
            heapq.heappush(passtimes, ((losetime(position_og[ahead[i]],velocity[ahead[i]],position_og[i], velocity[i], L), ahead[i], i)))

    passes=0
    ignore_events=set()

    prevLossTime=None
    while True:
        #pdb.set_trace()
        loss=heapq.heappop(passtimes)
        if loss[2] not in ignore_events and loss[1] not in ignore_events:
            #print(loss[2], " passes ", loss[1], " at time: ", loss[0].num, "/", loss[0].den)
            remove(loss[1], ahead, behind)
            ignore_events.add(loss[1])
            if loss[1]==0:
                #print ("Bowser rank is: ", N-passes, '\n\n\n')
                return N-passes
                #print("passtimes = ", passtimes)

            if loss[0] != prevLossTime:
                passes+=1

            if len(passtimes)==0:
                #print ("Bowser rank is: ", N-passes, '\n\n\n')
                return N-passes



            if velocity[loss[2]]>velocity[ahead[loss[2]]]:
                passtimes.append((losetime(position_og[ahead[loss[2]]],velocity[ahead[loss[2]]],position_og[loss[2]], velocity[loss[2]], L), ahead[loss[2]], loss[2]))


            prevLossTime=loss[0]
