class PathlessTreeSearch:
    """
    Implements a pathless tree search that supports BFS and DFS exploration.

    Attributes:
        order (str): Search order strategy ("bfs" or "dfs").
        best (Any): Best known solution found during the search.
        active (bool): True if the search can continue, False otherwise.
    """

    def __init__(self, n0, succ, goal, better=None, order="bfs"):
        """
        Initializes the search instance.
        """

        self.initial = n0 # n0 (Any): Initial node in the search.
        self.succ = succ # succ (Callable): Function that returns successors of a node.
        self.goal = goal # goal (Callable): Function that returns True if a node is a goal.
        self.better = better # better (Callable, optional): Comparator that returns True if first arg is better.
        self.order = order # order (str): Exploration strategy ("bfs" or "dfs").
        self.reset()

    def reset(self):
        """
        Resets the search to its initial configuration.
        Useful for re-running the search from scratch.
        """
        self.OPEN = [self.initial] # Reinicia OPEN con el nodo inicial
        self._best = None # Reinicia la solución
        self._active = True # Búsqueda activa

    def step(self):
        """
        Executes a single step in the tree search.

        Returns:
            bool: True if a new best solution is found; False otherwise.
        """
        if not self.OPEN:  # Si no hay más nodos por explorar la búsqueda para
            self._active = False
            return False

        if self.order == "bfs":
            node = self.OPEN.pop(0)  # BFS = cola
        else:
            node = self.OPEN.pop()   # DFS = pila

        if self.goal(node): # Si el nodo actual cumple la condición de ser solución (goal)
            if self._best is None: # Nueva mejor solución cuando antes no había ninguna
                self._best = node
                return True
            elif self.better and self.better(node, self._best): # Compara las soluciones
                self._best = node # Actualiza a la mejor solución
                return True  

        self.OPEN.extend(self.succ(node))
        return False

    @property
    def active(self):

        return len(self.OPEN) > 0 # Returns true if there are nodes left to explore.
    
    @property
    def best(self):

        return self._best # Returns the best node found so far, the current best solution.

def encode_problem(domains, constraints, better=None):
    """
    Encodes a fixed-variable search problem as a tree search.

    Args:
        domains (dict): Mapping of variable names to domain lists.
        constraints (Callable): Function that returns True if partial assignment is valid.
        better (Callable, optional): Function that compares two full assignments.

    Returns:
        PathlessTreeSearch: Configured search object.
    """
    variables = list(domains.keys()) # Lista de variables

    def succ(node): # Función que genera los nodos hijos de un nodo actual
        if len(node) == len(variables):
            return []

        next_variable = variables[len(node)]
        children = []

        for value in domains[next_variable]: # Prueba todos los valores de la variable
            new_node = node.copy()
            new_node[next_variable] = value
            if constraints(new_node):
                children.append(new_node)

        return children # Devuelve los hijos

    def goal(node):
        return len(node) == len(variables) # Si el tamaño de ambas es igual no hay más hijos

    return PathlessTreeSearch(n0={}, succ=succ, goal=goal, better=better) # Returns configured search object.
