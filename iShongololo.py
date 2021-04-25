#! /usr/bin/env python3
# ==================================================== >
# This is like a 3D maze, the other difficulty is that <
# there is a separate digging (eating), and moving.    >
# Symmetry can be ignored, cos the initial cube can be <
# not symmetrical.                                     >
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ <
# Algorithm outline:                                   >
# [0|init]                                             >
# dOthEMth( position ):                                <
#   [1|can't dig]                                      >
#   "If there are no moos, capitalize and gerout."     <
#   [2|dig loof]                                       >
#   "Loof over all digging combinations."              <
#   -> dig                                             >
#     [3|moo loof]                                     <
#     "Figure all possible moos."                      >
#     -> make a moo                                    <
#     -- dOthEMth( position )                          >
#     <- take back last moo                            <
#   <- undig                                           >
# |||||||||||||||||||||||||||||||||||||||||||||||||||| >
import numpy as np
# maze types
SHELL = 2
CORE  = 1
EMPTY = 0
def getmaze( shape ):
    ''' As in chess positions and similar frame the 
    board with guards to handle out-of-bound cks.
    '''
    shape = np.array( shape ) # switch addition on
    maze = np.full(( shape + 2 ), SHELL )
    x, y, z = shape + 1
    maze[1:x, 1:y, 1:z] = np.full( shape, CORE )
    return maze
# directions: y - up, down
#             x - left, ryte
#             z - forward, backward
#      z (k)
#    / 
#   /
#  /
#  --------- x (j)
#  \
#   \
#    \
#     \ y (i)
#     [dz, dy, dx]
DR = ([ 0, -1,  0], # up
      [ 0,  1,  0], # down
      [ 0,  0, -1], # left
      [ 0,  0,  1], # ryte
      [-1,  0,  0], # forward
      [ 1,  0,  0]) # backward
DR = tuple( map( np.array, DR ))
########################################################
def nbors( v ):
    ''' generate v nbors '''
    return ( tuple( v + dr ) for dr in DR )
########################################################
def is_empty( u ): return maze[u] == EMPTY
########################################################
def select( P, v ):
    ''' filter v nbors with predicate function P '''
    return filter( P, nbors( v ))
########################################################
def is_eatable( u ):
    '''ck vhether u is CORE and has most 1 EMPTY nbor'''
    if maze[u] != CORE: return False
    return len( list( select( is_empty, u ))) < 2
########################################################
def get_lunch( u ):
    ''' get list of eatable nbors of u '''
    return list( select( is_eatable, u ))
########################################################
from itertools import combinations as combinat
dighist = [] # digging history
maxhist = [] # thats
########################################################
def dig( combo ):
    for v in combo:
        maze[v] = EMPTY
        dighist.append( v )
########################################################
def undig( combo ):
    for v in combo:
        maze[v] = CORE
        dighist.pop()
########################################################
path = set()
########################################################
def get_mooz( u ):
    ''' get non visited EMPTY nbors '''
    mooz = select( is_empty, u )
    # discard visited lmnts
    return filter( lambda y: y not in path, mooz )
########################################################
def dOthEMth( v ):
    """"""
    path.add( v )
    lunch = get_lunch( v )
    if not lunch:
        if len( dighist ) > len( maxhist ):
            maxhist[:] = dighist
    else:
        for k in range( 1, 1 + len( lunch )):
            for combo in combinat( lunch, k ):
                dig( combo )
                for u in get_mooz( v ): dOthEMth( u )
                undig( combo )
    path.discard( v )
########################################################
if __name__ == '__main__':
    if 0: import pdb; pdb.set_trace()
    ## [ i n i t ]
    maze = getmaze([ 2, 3, 3 ])
    v = 1, 1, 1
    dighist.append( v )
    maze[v] = EMPTY
    ## [ 3 + x = 8 ]
    dOthEMth( v )
    print( maxhist )
# ==================================================== >
# log:                                                 <
# - output for 3, 3, 3 after LONG thinking:
# [(1, 1, 1), (1, 2, 1), (1, 1, 2), (2, 2, 1), (2, 3, 1),
#  (2, 2, 2), (3, 2, 1), (3, 1, 1), (3, 1, 2), (3, 1, 3),
#  (3, 2, 3), (2, 1, 3), (3, 3, 3), (3, 3, 2), (2, 3, 3),
#  (1, 3, 3), (1, 2, 3), (1, 3, 2)]
###################################################### >
