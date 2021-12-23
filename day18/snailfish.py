import json
from dataclasses import dataclass
from functools import reduce
from typing import List, Union, Optional, Callable, Tuple


@dataclass
class Tree:
    left: Union[int, "Tree"]
    right: Union[int, "Tree"]
    parent: Optional["Tree"]

    def __repr__(self):
        return f"({self.left}-{self.right})"

    def __add__(self, other):
        if not isinstance(other, Tree):
            raise TypeError
        t = Tree(self, other, None)
        t.left.parent = t
        t.right.parent = t
        return t


def parse_data(data: str) -> List[Tree]:
    return list(map(parse_row, data.split("\n")))


def parse_row(data: str) -> Tree:
    return list_to_tree(json.loads(data))


def list_to_tree(pairs: list, root: None | Tree = None) -> Tree:
    match pairs:
        case [int(left), int(right)]:
            return Tree(left, right, root)
        case [list(left), int(right)]:
            t = Tree(list_to_tree(left), right, root)
            t.left.parent = t
            return t
        case [int(left), list(right)]:
            t = Tree(left, list_to_tree(right), root)
            t.right.parent = t
            return t
        case [list(left), list(right)]:
            t = Tree(list_to_tree(left), list_to_tree(right), root)
            t.left.parent = t
            t.right.parent = t
            return t
        case _:
            raise ValueError("Bad tree")


def explode_tree(tree: int | Tree, depth: int = 0) -> None | Tree:
    match tree, depth:
        case int(_), _:
            return
        case Tree(Tree() as left, int(_)), _:
            return explode_tree(left, depth + 1)
        case Tree(int(_), Tree() as right), _:
            return explode_tree(right, depth + 1)
        case Tree(int(left), int(right)), d if d >= 4:
            _ = change_closest_left_node(tree, lambda v: v + left)
            _ = change_closest_right_node(tree, lambda v: v + right)
            if tree.parent.left is tree:
                tree.parent.left = 0
            else:
                tree.parent.right = 0
            return get_root(tree)
        case _:
            return explode_tree(tree.left, depth + 1) or explode_tree(tree.right, depth + 1)


def change_closest_left_node(tree: Tree, func: Callable[[int], int]) -> Tree:
    while True:
        if tree.parent is None:
            return get_root(tree)
        if tree.parent.left is not tree:
            break
        tree = tree.parent

    tree = tree.parent

    if isinstance(tree.left, int):
        tree.left = func(tree.left)
        return get_root(tree)

    tree = tree.left

    while True:
        if isinstance(tree.right, int):
            tree.right = func(tree.right)
            return get_root(tree)
        tree = tree.right


def change_closest_right_node(tree: Tree, func: Callable[[int], int]) -> Tree:
    while True:
        if tree.parent is None:
            return get_root(tree)
        if tree.parent.right is not tree:
            break
        tree = tree.parent

    tree = tree.parent

    if isinstance(tree.right, int):
        tree.right = func(tree.right)
        return get_root(tree)

    tree = tree.right

    while True:
        if isinstance(tree.left, int):
            tree.left = func(tree.left)
            return get_root(tree)
        tree = tree.left


def split_tree(tree: int | Tree, parent: Tree = None) -> None | Tree:
    match tree:
        case int(x) if x >= 10:
            if parent.left is x:
                parent.left = Tree(*get_splitting(x), parent)
            else:
                parent.right = Tree(*get_splitting(x), parent)
            return get_root(parent)
        case int(_):
            return
        case Tree(left, right):
            return split_tree(left, tree) or split_tree(right, tree)


def get_splitting(val: int) -> Tuple[int, int]:
    return val // 2, val - val // 2


def get_root(tree: Tree) -> Tree:
    if tree.parent is None:
        return tree
    return get_root(tree.parent)


def reduce_tree(tree: Tree) -> Tree:
    return (tree and (reduce_tree(explode_tree(tree) or split_tree(tree, tree.parent)))) or tree


def get_magnitude(tree: int | Tree) -> int:
    match tree:
        case int(x):
            return x
        case Tree(left, right):
            return 3 * get_magnitude(left) + 2 * get_magnitude(right)


def get_largest_magnitude(trees: List[str]) -> int:
    return max(map(lambda ts: get_magnitude(reduce_tree(parse_row(ts[0]) + parse_row(ts[1]))),
                   ((t1, t2) for t1 in trees for t2 in trees if t1 != t2)))


def solve_part_1(data: str) -> int:
    trees = parse_data(data)
    trees_sum = reduce(lambda acc, x: reduce_tree(acc + x), trees)
    return get_magnitude(trees_sum)


def solve_part_2(data: str) -> int:
    trees = data.split("\n")
    return get_largest_magnitude(trees)


def main():
    input_filename = "input.txt"

    with open(input_filename) as file:
        input_data = file.read()

    print(solve_part_1(input_data))
    print(solve_part_2(input_data))


if __name__ == "__main__":
    main()
