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

        Args:
            n0 (Any): Initial node in the search.
            succ (Callable): Function that returns successors of a node.
            goal (Callable): Function that returns True if a node is a goal.
            better (Callable, optional): Comparator that returns True if first arg is better.
            order (str): Exploration strategy ("bfs" or "dfs").
        """
        pass

    def reset(self):
        """
        Resets the search to its initial configuration.
        Useful for re-running the search from scratch.
        """
        pass

    def step(self):
        """
        Executes a single step in the tree search.

        Returns:
            bool: True if a new best solution is found; False otherwise.
        """
        pass

    @property
    def active(self):
        """
        Indicates whether the search is still ongoing.

        Returns:
            bool: True if there are nodes left to explore.
        """
        raise NotImplementedError("You must implement the 'active' property.")

    @property
    def best(self):
        """
        Returns the current best solution.

        Returns:
            Any: The best node found so far.
        """
        raise NotImplementedError("You must implement the 'best' property.")


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
    raise NotImplementedError("You must implement 'encode_problem'")
