from utils import linked_list

from copy import deepcopy

def swap(
    head
    , penultimate
    , ultimate
    , node
    , next_node=None
    , previous_node=None
):
    swapping_far = next_node or previous_node

    if swapping_far:
        node.next = next_node.next
        ultimate.next = node

        if penultimate is None:
            next_node.next = ultimate
        else:
            next_node.next = penultimate

        if previous_node:
            previous_node.next = next_node
        else:
            head = next_node

        return head, node

    else:
        next_node = node.next
        ultimate.next = next_node
        node.next = ultimate

        if penultimate is not None:
            penultimate.next = node
        else:
            head = node

        return head, node

def swap_nodes(ll, i, copy=True):
    if copy:
        ll = deepcopy(ll)

    tmp = ll

    penultimate = None
    ultimate = None

    for idx in range(i + 1):
        penultimate = ultimate
        ultimate = tmp
        tmp = tmp.next

    return swap(ll, penultimate, ultimate, tmp)

def swap_far(ll, left, right, copy=True):
    if right <= left:
        raise Exception(f"left {left} has to be less than right {right}")

    if (diff := right - left) == 1:
        return swap_nodes(ll, left, copy=copy)

    if copy:
        ll = deepcopy(ll)

    node = ll
    prev = None

    inner = [None, None]

    for idx in range(left):
        prev = node
        node = node.next

    left_node = node

    idx = left
    while idx < right:
        if diff == 2:
            if idx == left + 1:
                inner[-1] = node
        else:
            if idx == left + 1:
                inner[0] = node
            elif idx == right - 1:
                inner[1] = node

        node = node.next

        idx += 1

    print(inner, left_node, node)
    return swap(ll, inner[0], inner[1], left_node, node, prev)


# TODO: SAVE THIS, THIS WORKS, BUT CLEAN IT UP AND REMOVE
# EXTRA LOGIC. THERE IS DEFINITELY A SIMPLER WAY TO HANDLE THIS
# the trick seems to be to have inner[0] set to reverse.next
# and inner[1] to be previous node (ultimate)
# just need the minimal conditions to modify how to call swap
def reverse_nodes(ll, copy=True):
    if copy:
        ll = deepcopy(ll)

    node = ll

    penultimate = None
    ultimate = None

    previous = None
    inner = [None, None]

    idx = 1

    # TODO: need to swap reverse with node
    # then while reverse idx != node idx
    # we swap reverse with node (far)

    while node.next is not None:
        reverse = ll

        penultimate = ultimate
        ultimate = node
        node = node.next

        if penultimate is None:
            ll, node = swap(ll, penultimate, ultimate, node)
            node = node.next
            idx += 1
            continue

        ctr = 1

        print(
            '\n'.join(
                str(n) for n in [previous, reverse, penultimate, ultimate, node]
            )
        )

        while ctr < idx + 1:
            if ctr != idx:
                if ctr + 1 == idx:
                    inner = [None, ultimate]
                else:
                    inner = [reverse.next, ultimate]

                print(ll, inner, reverse, node)
                ll, node = swap(
                    ll, inner[0], inner[1]
                    , reverse, node, None if ctr == 1 else previous
                )
                print(ll, node)
            else:
                ll, node = swap(
                    ll, previous, reverse, node
                )

            reverse = ll

            for i in range(ctr):
                previous = reverse
                reverse = reverse.next

            ctr += 1

        node = node.next

        print(ll, node)
        print()

        idx += 1

    return ll

def reverse(ll, copy=True):
    if copy:
        ll = deepcopy(ll)

    node = ll

    ultimate = None

    previous = None

    while node.next is not None:
        ultimate = node
        node = node.next

        ultimate.next = node.next
        node.next = ll
        ll = node
        node = ultimate

    return ll

def reverse_k(ll, k, copy=True):
    if copy:
        ll = deepcopy(ll)

    node = ll

    ultimate = None

    idx = 1

    currhead = ll
    prevhead = None

    while node.next is not None:
        ultimate = node
        node = node.next

        if idx % k == 0:
            if prevhead is None:
                prevhead = currhead
            else:
                ll = ultimate

            currhead = ultimate.next

        else:
            ultimate.next = node.next
            node.next = currhead
            currhead = node

            if prevhead is not None:
                ll.next = currhead

            node = ultimate

        idx += 1

    return prevhead


ll = linked_list([1,2,3,4,5,6,7,8])
swapped = swap_nodes(ll, 0, True)

"""


1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> None
h    ^

2 -> 1 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> None
h    ^

2 -> 1 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> None
h    u    ^

3 -> 2 -> 1 -> 4 -> 5 -> 6 -> 7 -> 8 -> None
h    u    p    ^
|              |

swap nodes 3 & 4

4 -> 2 -> 1 -> 3 -> 5 -> 6 -> 7 -> 8 -> None
h    u    p    ^
     |         |

swap nodes 2 & 3

4 -> 3 -> 1 -> 2 -> 5 -> 6 -> 7 -> 8 -> None
h    u    p    ^
          |    |

swap nodes 1 & 2

4 -> 3 -> 2 -> 1 -> 5 -> 6 -> 7 -> 8 -> None
h    u    p    ^

"""



"""
GRAVEYARD

def reverse_nodes(ll, copy=True):
    if copy:
        ll = deepcopy(ll)

    node = ll
    reverse = ll

    penultimate = None
    ultimate = None

    idx = 0

    while node.next is not None:
        penultimate = ultimate
        ultimate = node
        node = node.next

        if idx % 2 == 0:
            ll, node = swap(ll, penultimate, ultimate, node)
            penul_rev = None

            print(ll, node)

            if reverse != node:
                new_node = node.next

                while reverse != node:
                    tmp = reverse.next
                    ll, reverse = swap(ll, penul_rev, reverse, reverse.next)
                    penul_rev = tmp
                    print(ll)
                    print(reverse)
                    print()

                node = new_node
                reverse = 


        idx += 1

    return ll

"""
