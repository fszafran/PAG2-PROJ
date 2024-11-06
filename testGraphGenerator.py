from HelperClasses import Graph, Node, Edge

def euclidean_between_nodes(node1: Node, node2: Node) -> float:
    return ((node1.x - node2.x)**2 + (node1.y - node2.y)**2)**0.5

def ABCDEF_1():
    """
    Do testów na zwykla odleglosc
    """
    graph = Graph()

    A = Node(1,1)
    B = Node(2,3)
    C = Node(4,1)
    D = Node(3,3)
    E = Node(4,2)
    F = Node(4,3)

    graph.add_node(A)
    graph.add_node(B)
    graph.add_node(C)
    graph.add_node(D)
    graph.add_node(E)
    graph.add_node(F)

    AC = Edge(1, A.id, C.id, 3, 0, 0)
    AB = Edge(2, A.id, B.id, euclidean_between_nodes(A,B), 0,0)
    BD = Edge(3, B.id, D.id, 1, 0,0)
    CE = Edge(4, C.id, E.id, 1, 0,0)
    DF = Edge(5, D.id, F.id, 1, 0,0)
    EF = Edge(6, E.id, F.id, 1, 0,0)

    graph.add_edge(AC)
    graph.add_edge(AB)
    graph.add_edge(BD)
    graph.add_edge(CE)
    graph.add_edge(DF)
    graph.add_edge(EF)
    
    return graph

def ABCDEF_2():
    graph = Graph()

    A = Node(1,1)
    B = Node(2,3)
    C = Node(4,1)
    D = Node(3,3)
    E = Node(4,2)
    F = Node(4,3)

    graph.add_node(A)
    graph.add_node(B)
    graph.add_node(C)
    graph.add_node(D)
    graph.add_node(E)
    graph.add_node(F)

    AC = Edge(1, A.id, C.id, 3, 140, 0)
    AB = Edge(2, A.id, B.id, euclidean_between_nodes(A,B), 100,0)
    BD = Edge(3, B.id, D.id, 1, 50,0)
    CE = Edge(4, C.id, E.id, 1, 50,0)
    DF = Edge(5, D.id, F.id, 1, 50,0)
    EF = Edge(6, E.id, F.id, 1, 50,0)

    graph.add_edge(AC)
    graph.add_edge(AB)
    graph.add_edge(BD)
    graph.add_edge(CE)
    graph.add_edge(DF)
    graph.add_edge(EF)
    
    return graph

def GHIJK_1():
    graph = Graph()

    G = Node(7,1)
    H = Node(7, 2)
    I = Node(8, 1)
    J = Node(7, 4)
    K = Node(10,1)

    graph.add_node(G)
    graph.add_node(H)
    graph.add_node(I)
    graph.add_node(J)
    graph.add_node(K)

    GH = Edge(1, G.id, H.id, 1, 0, 18) # brak atrakcji przy krawedzi (18 wybrane losowo)
    GI = Edge(2, G.id, I.id, 1, 0, 3) # sporo atrakcji
    HJ = Edge(3, H.id, J.id, 2, 0, 18) # brak atrakcji przy krawedzi (18 wybrane losowo)
    IK = Edge(4, I.id, K.id, 2, 0, 10) # malo atrakcji ale sa 
    JK = Edge(5, J.id, K.id, euclidean_between_nodes(J,K), 0, 0) # najwieksza liczba atrakcji w zbiorze
    
    graph.add_edge(GH)
    graph.add_edge(GI)
    graph.add_edge(HJ)
    graph.add_edge(IK)
    graph.add_edge(JK)

    return graph
