# -*- coding: utf-8 -*-
"""
Created on Sun Jul 2 2023

@author: Sanket Jain
"""

import numpy as np
import networkx as nx


def create_D_matrix(G):
    number_of_vertices = len(G.nodes)
    D = np.zeros((number_of_vertices, number_of_vertices))
    for start_node in G.nodes:
        for end_node in G.nodes:
            if end_node == start_node:
                pass
            else:
                path = nx.shortest_path(G, start_node, end_node)
                shortest_path_length = 0
                found_in_edges_of_G = False
                for edge in G.edges(data=True):
                    if start_node == edge[0] and end_node == edge[1]:
                        found_in_edges_of_G = True
                        shortest_path_length = edge[2]['weight']
                if found_in_edges_of_G == False:
                    continuity_maintained = 1
                    for n in range(len(path)-1):
                        for edge1 in G.edges(data=True):
                            if path[n] == edge1[0] and path[n+1] == edge1[1]:
                                continuity_maintained = continuity_maintained*1
                                shortest_path_length = shortest_path_length + edge1[2]['weight']    
                            else:
                                continuity_maintained = continuity_maintained*1
                        if continuity_maintained == 0:
                            shortest_path_length = 0
                D[start_node][end_node] = shortest_path_length
    return D


def F(x, y):
    return x*y


def get_out_transmission_numbers_vector(G, w):
    D = create_D_matrix(G)
    h = []
    for j in G.nodes:
        hj = 0
        for k in G.nodes:
            hj = hj + F(D[j][k], w[k])
        h.append(hj)
    return h


def get_in_transmission_numbers_vector(G, w):
    D = create_D_matrix(G)
    h = []
    for j in G.nodes:
        hj = 0
        for k in G.nodes:
            hj = hj + F(D[k][j], w[k])
        h.append(hj)
    return h


def get_V_mho(G, delta_h_out):
    V_mho = []
    maximum = max(delta_h_out)
    for i in range(len(G.nodes)):
        if delta_h_out[i] == maximum:
            V_mho.append(i)
    return V_mho


def get_vj(G, delta_h_in, delta_h_in_greater_than_zero):
    for i in range(len(G.nodes)):
        if delta_h_in[i] == delta_h_in_greater_than_zero[0]:
            return i


def get_V_s(G, V_mho, vj):
    V_s = []
    D = create_D_matrix(G)
    for node_i in V_mho:
        for node_k in V_mho:
            if D[node_k][vj] < D[node_i][vj]:
                V_s.append(node_k)
    return V_s


def get_fault_edge(G, G1, weights_of_vertices):

    h_out = get_out_transmission_numbers_vector(G, weights_of_vertices)

    h1_out = get_out_transmission_numbers_vector(G1, weights_of_vertices)
    
    h_in = get_in_transmission_numbers_vector(G, weights_of_vertices)
    
    h1_in = get_in_transmission_numbers_vector(G1, weights_of_vertices)
    
    delta_h_out = [h1_out[i] - h_out[i] for i in range(len(h_out))]
    
    V_mho = get_V_mho(G, delta_h_out)
    
    delta_h_in = [h1_in[i] - h_in[i] for i in range(len(h_in))]
    
    delta_h_in_greater_than_zero = [elem for elem in delta_h_in if elem > 0]
    
    vj = get_vj(G, delta_h_in, delta_h_in_greater_than_zero)
    
    V_s = get_V_s(G, V_mho, vj)
    
    vp = V_s[0]
    
    shortest_path_from_vp_to_vj = nx.shortest_path(G, vp, vj)
    
    vq = shortest_path_from_vp_to_vj[1]
    
    fault_edge = [vp, vq]

    return(fault_edge)


#main


A = np.matrix([[0, 1, 2, 0], [1, 0, 0, 2], [0, 2, 0, 2], [2, 0, 2, 0]])

G=nx.from_numpy_matrix(A,create_using=nx.MultiDiGraph())

A1 = np.matrix([[0, 1, 3, 0], [1, 0, 0, 2], [0, 2, 0, 2], [2, 0, 2, 0]])

G1=nx.from_numpy_matrix(A1,create_using=nx.MultiDiGraph())
              
weights_of_vertices = [1, 1, 1, 1]
            
fault_edge = get_fault_edge(G, G1, weights_of_vertices)

print(fault_edge)