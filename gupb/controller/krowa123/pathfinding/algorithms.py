from typing import Dict, Optional, List

from gupb.model.coordinates import Coords
from .node import Node
from ..model import SeenTile
from ..utils import neighboring_coords


# A* search
def astar_search(terrain: Dict[Coords, SeenTile], start: Coords, end: Coords) -> Optional[List[Coords]]:
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)
    # Loop until the open list is empty
    while len(open) > 0:

        # Sort the open list to get the node with the lowest cost first
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
        # Add the current node to the closed list
        closed.append(current_node)

        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            # path.append(start)
            # Return reversed path
            return path[::-1]

        # Unzip the current node position
        pos = current_node.position
        # Get neighbors
        neighbors = neighboring_coords(pos)
        # Loop neighbors
        for next in neighbors:
            # Get value from terrain
            terrain_value = terrain.get(next)
            # Check if the node is a wall
            if not terrain_value.tile.terrain_passable():
                continue
            # Create a neighbor node
            neighbor = Node(next, current_node)
            # Check if the neighbor is in the closed list
            if neighbor in closed:
                continue
            # Generate heuristics (Manhattan distance)
            dist_start = neighbor.position - start_node.position
            dist_goal = neighbor.position - goal_node.position
            neighbor.g = abs(dist_start.x) + abs(dist_start.y)
            neighbor.h = abs(dist_goal.x) + abs(dist_goal.y)
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if _add_to_open(open, neighbor):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None


# Check if a neighbor should be added to open list
def _add_to_open(open, neighbor):
    for node in open:
        if neighbor == node and neighbor.f >= node.f:
            return False
    return True
