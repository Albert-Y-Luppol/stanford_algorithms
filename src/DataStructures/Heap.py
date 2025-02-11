import uuid
from typing import TypeVar, Callable, Union, Dict, Tuple

T = TypeVar('T')
K = Union[str, int]


class Heap:
    def __init__(
            self,
            comparison_fn: Callable[[T, T], bool] = lambda a, b: a < b,
    ):
        self.__heap: [Tuple[K, T]] = []
        self.__dictionary: Dict[K, int] = {}
        self.__is_first_parent_of_second = comparison_fn

    def __setitem__(self, key: K, value: T):
        self._add_item(value, key)

    def __getitem__(self, key: K) -> T:
        if key not in self.__dictionary:
            return None

        return self.__heap[self.__dictionary[key]][1]

    def __delitem__(self, key: K) -> None:
        if key not in self.__dictionary:
            return

        self._delete_item(key)

    def __len__(self):
        return len(self.__heap)

    def __iter__(self):
        return iter(self.__heap)

    def __get_parent_item(self, child_key: K) -> Union[Tuple[K, T], Tuple[None, None]]:
        if self.__dictionary[child_key] == 0:
            return None, None
        return self.__heap[(self.__dictionary[child_key] - 1) // 2]

    def __bubble_up_item(self, item_key: K) -> None:
        while True:
            parent_key, parent_item = self.__get_parent_item(item_key)
            if parent_item is None \
                    or self.__is_first_parent_of_second(parent_item, self.__heap[self.__dictionary[item_key]][1]):
                break

            self.__swap(item_key, parent_key)

    def __swap(self, key_a: K, key_b: K) -> None:
        item_a_index = self.__dictionary[key_a]
        item_a = self.__heap[item_a_index]
        self.__heap[item_a_index] = self.__heap[self.__dictionary[key_b]]
        self.__heap[self.__dictionary[key_b]] = item_a
        self.__dictionary[key_a] = self.__dictionary[key_b]
        self.__dictionary[key_b] = item_a_index

    def __get_children(self, child_key: K) -> Tuple[Tuple[K, T], Tuple[K, T]]:
        left_child_index = self.__dictionary[child_key] * 2 + 1
        right_child_index = left_child_index + 1

        return self.__heap[left_child_index] if len(self.__heap) > left_child_index else None,\
            self.__heap[right_child_index] if len(self.__heap) > right_child_index else None

    def __bubble_down_item(self, item_key: K) -> None:
        item = self.__heap[self.__dictionary[item_key]]

        while True:
            left_child, right_child = self.__get_children(item_key)

            should_swap_left_child = left_child is not None and self.__is_first_parent_of_second(left_child[1], item[1])
            should_swap_right_child = right_child is not None and self.__is_first_parent_of_second(right_child[1], item[1])

            if should_swap_left_child and should_swap_right_child:
                child_to_swap = left_child if self.__is_first_parent_of_second(left_child[1], right_child[1]) else \
                    right_child
            elif should_swap_right_child:
                child_to_swap = right_child
            elif should_swap_left_child:
                child_to_swap = left_child
            else:
                child_to_swap = None

            if child_to_swap is None:
                break

            self.__swap(item_key, child_to_swap[0])

    def __get_uuid(self):
        while True:
            key = uuid.uuid4().hex
            if key not in self.__dictionary:
                return key

    def _add_item(self, key: K, item: T) -> None:
        if key in self.__dictionary:
            raise KeyError(f'Original Key Exception: Item with key "{key}" already in the heap.')

        item_index = len(self.__heap)
        self.__heap.append((key, item))
        self.__dictionary[key] = item_index
        self.__bubble_up_item(key)

    def _delete_item(self, item_key: K) -> None:
        if item_key not in self.__dictionary:
            return

        last_item_key = self.__heap[len(self.__heap) - 1][0]

        if last_item_key == item_key:
            self.__heap.pop()
        else:
            self.__swap(last_item_key, item_key)
            self.__heap.pop()
            self.__bubble_down_item(last_item_key)

        del self.__dictionary[item_key]

    def pop(self) -> T:
        if len(self.__heap) == 0:
            return None

        key, item = self.__heap[0]
        self._delete_item(key)
        return item

    def add(self, item: T) -> None:
        key = self.__get_uuid()
        self._add_item(key, item)

    def items(self) -> [T]:
        return list(map(lambda x: x[1], self.__heap))

    def peak(self) -> T:
        return None if len(self.__heap) == 0 else self.__heap[0][1]

    def __repr__(self):
        if len(self.__heap) == 0:
            return 'None'

        lines, *_ = self.__display_aux(self.__heap[0][0])
        return '\n'.join(lines)

    def __display_aux(self, key: K):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        left_child, right_child = self.__get_children(key)
        # No child.
        if left_child is None and right_child is None:
            line = '%s' % self[key]
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if right_child is None:
            lines, n, p, x = self.__display_aux(left_child[0])
            s = '%s' % self[key]
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if left_child is None:
            lines, n, p, x = self.__display_aux(left_child[0])
            s = '%s' % self[key]
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.__display_aux(left_child[0])
        right, m, q, y = self.__display_aux(right_child[0])
        s = '%s' % self[key]
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

