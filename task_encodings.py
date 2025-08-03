from pathless_tree_search import PathlessTreeSearch, encode_problem
from connect4.connect_state import ConnectState
import numpy as np

def get_tree_search_for_sudoku(sudoku):
    """
    Prepares a tree search to solve a Sudoku puzzle.

    Args:
        sudoku (np.ndarray): 9x9 numpy array representing the Sudoku board.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object for solving the Sudoku.
            - decoder: Function to decode final node to 9x9 board.
    """
    variables = [] # Guardar posiciones vacías (0)
    for i in range(9):
        for j in range(9):
            if sudoku[i, j] == 0:
                variables.append((i, j))

    domains = {} # Para cada posición, el dominio es de 1 a 9 (valores del sudoku)
    for (i, j) in variables:
        used_in_row = set(sudoku[i, :])
        used_in_col = set(sudoku[:, j])
        block_i, block_j = 3 * (i // 3), 3 * (j // 3)
        used_in_block = set(sudoku[block_i:block_i+3, block_j:block_j+3].flatten())
        used = used_in_row.union(used_in_col).union(used_in_block)
        domains[(i, j)] = [val for val in range(1, 10) if val not in used]

    def constraints(partial): # Verifica si es movimiento valido
        board = sudoku.copy() # Copia del tablero
        for (i, j), val in partial.items(): # Asignar los valores
            board[i, j] = val
        
        for (i, j), val in partial.items(): # Verifica si un número está repetido
            if list(board[i, :]).count(val) > 1: # En fila
                return False
            if list(board[:, j]).count(val) > 1: # En columna
                return False
            block_i, block_j = 3 * (i // 3), 3 * (j // 3)
            block = board[block_i:block_i+3, block_j:block_j+3].flatten()
            if list(block).count(val) > 1: # En bloques de 3x3
                return False
        return True

    def decoder(node):  # Function to decode final node to 9x9 board.
        board = sudoku.copy()
        if node is None:
            return board  # Devuelve el original si no encontró solución
        for (i, j), val in node.items():
            board[i, j] = val
        return board

    search = encode_problem(domains, constraints, order="dfs") # Search object for solving the Sudoku.

    return search, decoder # Tupla con PathlessTreeSearch y decoder

def get_tree_search_for_jobshop(jobshop):
    """
    Encodes a Job Shop Scheduling problem as a tree search.

    Args:
        jobshop (tuple): A tuple (m, d) where:
            - m (int): Number of machines.
            - d (list): List of job durations.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object for solving the job shop.
            - decoder: Function to decode final node into job-machine assignments.
    """
    m, d = jobshop # A tuple (m, d) = (number machines, list of jobs durations)
    n = len(d) # Número total de trabajos
    variables = list(range(n)) # Cada trabajo es una variable
    domains = {}
    for var in variables:
        domains[var] = list(range(m))

    def constraints(partial):
        # Cualquier asignación de máquina es válida
        return True

    def better(solution_1, solution_2): # Comparar las soluciones
        def makespan(assign):
            times = [0] * m # Tiempo acumulado de cada máquina
            for job, machine in assign.items():
                times[machine] += d[job]
            return max(times)
        
        return makespan(solution_1) < makespan(solution_2)

    def decoder(node): # Function to decode final node into job-machine assignments.
        if node is None:
            return [0] * len(d)  # asigna todos los trabajos a máquina 0
        return [node[i] for i in range(len(d))]

    search = encode_problem(domains, constraints, better, order="bfs") # Search object for solving the job shop.

    return search, decoder  # Tupla con PathlessTreeSearch y decoder

def get_tree_search_for_connect_4(opponent):
    """
    Creates a tree search object to find a winning strategy for Connect-4.

    Args:
        opponent (Callable): Function mapping state to opponent's move.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object to solve the game.
            - decoder: Function to extract yellow player’s move sequence.
    """

    initial = ConnectState() # Estado inicial
    first_red_move = opponent(initial)
    first_state = initial.transition(first_red_move)
    s0 = (first_state, [])

    def goal(state): # Jugador amarillo gana
        game_state, _ = state

        return game_state.is_final() and game_state.get_winner() == 1 # Amarillo es 1

    def succ(state):
        game_state, yellow_moves = state

        if game_state.is_final(): # Si el estado es final o el tablero está lleno
            return []

        children = []
        for yellow_move in game_state.get_free_cols():  # Columnas disponibles
            yellow_state = game_state.transition(yellow_move)  # Movimiento del jugador amarillo
            updated_moves = yellow_moves + [yellow_move]

            if yellow_state.is_final():
                children.append((yellow_state, updated_moves))
            else:
                red_move = opponent(yellow_state) # Movimiento del jugador rojo 
                red_state = yellow_state.transition(red_move)
                children.append((red_state, updated_moves))

        return children

    def decoder(state): 
        # Function to extract yellow player’s move sequence
        _, yellow_moves = state
        return yellow_moves

    search = PathlessTreeSearch(n0=s0, succ=succ, goal=goal, order="dfs")  #  Search object to solve the game.

    return search, decoder # Tupla con PathlessTreeSearch y decoder    

def get_tree_search_for_tour_planning(distances, from_index, to_index):
    """
    Encodes a tour planning problem as a tree search.

    Args:
        distances (np.ndarray): Adjacency matrix of distances between cities.
        from_index (int): Starting city index.
        to_index (int): Target city index.

    Returns:
        tuple: (PathlessTreeSearch, decoder)
            - search: Search object to solve the tour planning problem.
            - decoder: Function that returns the full path of the tour.
    """
    n = len(distances)
    start = [from_index] # Nodo inicial

    def goal(path):
        # Objetivo
        return path[-1] == to_index

    def succ(path): # Construir la ruta
        current = path[-1]
        successors = []
        for next_city in range(n):
            if distances[current, next_city] > 0 and next_city not in path:
                successors.append(path + [next_city])

        return successors

    def better(path_1, path_2): # Comparar las distancias
        def total_distance(path):
            return sum(distances[path[i], path[i+1]] for i in range(len(path) - 1))
        
        return total_distance(path_1) < total_distance(path_2)

    def decoder(path):
        # Function that returns the full path of the tour.
        return path

    search = PathlessTreeSearch(n0=start, succ=succ, goal=goal, better=better, order="dfs") # Search object to solve the tour planning problem.

    return search, decoder # Tupla con PathlessTreeSearch y decoder