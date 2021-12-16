from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Set, Tuple, Dict, Callable, Deque, Iterator


@dataclass(frozen=True)
class Node:
    name: str

    @property
    def is_small(self):
        return self.name.islower()

    def __repr__(self):
        return self.name


Graph = Dict[Node, Set[Node]]


def parse_data(data: str) -> Graph:
    return get_nodes(data.split("\n"))


def get_nodes(rows: List[str]) -> Graph:
    all_nodes = list(map(get_nodes_from_string, rows))
    graph = defaultdict(set)
    for start, stop in all_nodes:
        graph[start].add(stop)
        graph[stop].add(start)
    return graph


def get_nodes_from_string(row: str) -> Tuple[Node, Node]:
    start, stop = row.split("-")
    return Node(start), Node(stop)


def get_routes(graph: Graph, traverse_rule: Callable[[Node, List[Node]], bool]) -> List[List[Node]]:
    return list(_get_routes(graph, deque([[Node("start")]]), traverse_rule))


def _get_routes(graph: Graph, stack: Deque[List[Node]], traverse_rule: Callable[[Node, List[Node]], bool]) \
        -> Iterator[List[Node]]:
    while stack:
        current_route = stack[0]
        next_nodes = list(filter(lambda n: traverse_rule(n, current_route), graph[current_route[-1]]))
        for node in next_nodes:
            if node == Node("end"):
                yield current_route + [node]
            else:
                stack.append(current_route + [node])
        stack.popleft()


def traverse_rule_for_single_small_twice(node: Node, nodes: List[Node]) -> bool:
    if node == Node("start"):
        return False
    if not node.is_small:
        return True
    if node not in nodes:
        return True
    small_nodes = list(filter(lambda n: n.is_small, nodes))
    if len(small_nodes) == len(set(small_nodes)):
        return True
    return False


def solve_part_1(data: str) -> int:
    traverse_rule = lambda n, ns: not (n.is_small and n in ns)
    return len(get_routes(parse_data(data), traverse_rule))


def solve_part_2(data: str) -> int:
    traverse_rule = traverse_rule_for_single_small_twice
    return len(get_routes(parse_data(data), traverse_rule))


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
