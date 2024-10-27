

Prac_4_Binary.py 
______________________________________________________________________________________
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

class BinaryTree:
    def __init__(self, root_value):
        self.root = Node(root_value)

    def insert_left(self, current_node, value):
        if current_node.left is None:
            current_node.left = Node(value)
        else:
            new_node = Node(value)
            new_node.left = current_node.left
            current_node.left = new_node

    def insert_right(self, current_node, value):
        if current_node.right is None:
            current_node.right = Node(value)
        else:
            new_node = Node(value)
            new_node.right = current_node.right
            current_node.right = new_node

    def preorder_traversal(self, start, traversal):
        """Root > Left > Right"""
        if start:
            traversal.append(start.value)
            self.preorder_traversal(start.left, traversal)
            self.preorder_traversal(start.right, traversal)
        return traversal

    def inorder_traversal(self, start, traversal):
        """Left > Root > Right"""
        if start:
            self.inorder_traversal(start.left, traversal)
            traversal.append(start.value)
            self.inorder_traversal(start.right, traversal)
        return traversal

    def postorder_traversal(self, start, traversal):
        """Left > Right > Root"""
        if start:
            self.postorder_traversal(start.left, traversal)
            self.postorder_traversal(start.right, traversal)
            traversal.append(start.value)
        return traversal

# Example usage
tree = BinaryTree(1)
tree.insert_left(tree.root, 2)
tree.insert_right(tree.root, 3)
tree.insert_left(tree.root.left, 4)
tree.insert_right(tree.root.left, 5)
tree.insert_left(tree.root.right, 6)
tree.insert_right(tree.root.right, 7)
tree.insert_left(tree.root.left.left, 8)
tree.insert_right(tree.root.left.left, 9)
tree.insert_left(tree.root.right.right, 10)
tree.insert_right(tree.root.right.right, 11)

print("Preorder:", tree.preorder_traversal(tree.root, []))
print("Inorder:", tree.inorder_traversal(tree.root, []))
print("Postorder:", tree.postorder_traversal(tree.root, []))

----------------------------------------------- OUTPUT -----------------------------------------------------------------------------------
D:\BC_Python_2024\venv\Scripts\python.exe D:\BC_Python_2024\Prac_4_Binary.py 
Preorder: [1, 2, 4, 8, 9, 5, 3, 6, 7, 10, 11]
Inorder: [8, 4, 9, 2, 5, 1, 6, 3, 10, 7, 11]
Postorder: [8, 9, 4, 5, 2, 6, 10, 11, 7, 3, 1]

Process finished with exit code 0



*****************************************************************************************************************************************************

Prac_4_merkle.py
_______________________________________________________________________________________________________________________________________________________
from typing import List
import hashlib

class Node:
    def __init__(self, left, right, value: str, content, is_copied=False) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        self.is_copied = is_copied

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return str(self.value)

    def copy(self):
        return Node(self.left, self.right, self.value, self.content, True)

class MerkleTree:
    def __init__(self, values: List[str]) -> None:
        self.buildTree(values)

    def buildTree(self, values: List[str]) -> None:
        leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])  # Duplicate last element if odd number of elements
        self.root: Node = self.buildTreeRec(leaves)

    def buildTreeRec(self, nodes: List[Node]) -> Node:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())
        half: int = len(nodes) // 2
        if len(nodes) == 2:
            return Node(
                nodes[0], nodes[1],
                Node.hash(nodes[0].value + nodes[1].value),
                nodes[0].content + "+" + nodes[1].content
            )
        left: Node = self.buildTreeRec(nodes[:half])
        right: Node = self.buildTreeRec(nodes[half:])
        value: str = Node.hash(left.value + right.value)
        content: str = left.content + "+" + right.content
        return Node(left, right, value, content)

    def printTree(self) -> None:
        self.printTreeRec(self.root)

    def printTreeRec(self, node) -> None:
        if node is not None:
            if node.left is not None:
                print("Left:\n" + str(node.left))
                print("Right:\n" + str(node.right))
            else:
                print("Input")
            if node.is_copied:
                print('(Padding)')
            print("Value:\n" + str(node.value))
            print("Content:\n" + str(node.content))
            print()
            self.printTreeRec(node.left)
            self.printTreeRec(node.right)

    def getRootHash(self) -> str:
        return self.root.value

def mixmerkletree() -> None:
    elems = ["xyz", "abc", "SYMCA A", "00", "VESIT", "https://xyz.com/"]
    print("Inputs:")
    print(*elems, sep=" | ")
    print()
    mtree = MerkleTree(elems)
    print("Root Hash:\n" + mtree.getRootHash() + "\n")
    mtree.printTree()

mixmerkletree()

------------------------------------------------------------------- OUTPUT --------------------------------------------------------------------------------------
D:\BC_Python_2024\venv\Scripts\python.exe D:\BC_Python_2024\Prac_4_merkle.py 
Inputs:
xyz | abc | SYMCA A | 00 | VESIT | https://xyz.com/

Root Hash:
f07f5f3b7b8da7ddecc5c95b7be0bb8e518bc0ea66746cef12998ed4ca30d122

Left:
e236b3a0015128d5f6c7a6b0e1099917a37fbf7cbddb1ccfdf88f1b1c504257f
Right:
7bc5a547fbdf108d30a4410b337df76b5c9ef9a156002fd3badc185ec5cb3202
Value:
f07f5f3b7b8da7ddecc5c95b7be0bb8e518bc0ea66746cef12998ed4ca30d122
Content:
xyz+abc+SYMCA A+SYMCA A+00+VESIT+https://xyz.com/+https://xyz.com/

Left:
411d380534131858d0d7b07d3d816a7b1a1fc22591114dd44f29dfcf0b8fafbb
Right:
dcf483f7d536872c381fbb7f5288c4efe9a8b5d06d005ad22dd173458bfb84ad
Value:
e236b3a0015128d5f6c7a6b0e1099917a37fbf7cbddb1ccfdf88f1b1c504257f
Content:
xyz+abc+SYMCA A+SYMCA A

Left:
3608bca1e44ea6c4d268eb6db02260269892c0b42b86bbf1e77a6fa16c3c9282
Right:
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
Value:
411d380534131858d0d7b07d3d816a7b1a1fc22591114dd44f29dfcf0b8fafbb
Content:
xyz+abc

Input
Value:
3608bca1e44ea6c4d268eb6db02260269892c0b42b86bbf1e77a6fa16c3c9282
Content:
xyz

Input
Value:
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
Content:
abc

Left:
87b94c4560b7931a0e6eff225a605e84255365c26d5c8da556263c3b44484726
Right:
87b94c4560b7931a0e6eff225a605e84255365c26d5c8da556263c3b44484726
Value:
dcf483f7d536872c381fbb7f5288c4efe9a8b5d06d005ad22dd173458bfb84ad
Content:
SYMCA A+SYMCA A

Input
Value:
87b94c4560b7931a0e6eff225a605e84255365c26d5c8da556263c3b44484726
Content:
SYMCA A

Input
(Padding)
Value:
87b94c4560b7931a0e6eff225a605e84255365c26d5c8da556263c3b44484726
Content:
SYMCA A

Left:
e361189f9363a9d8b69b58f48184096282e2b8a7e3b07a28854707de32ad2e18
Right:
b40441469667d9e22dc2c10e86a2eef53f213043439bfda7931ddf9628c87310
Value:
7bc5a547fbdf108d30a4410b337df76b5c9ef9a156002fd3badc185ec5cb3202
Content:
00+VESIT+https://xyz.com/+https://xyz.com/

Left:
f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e
Right:
b2443eb348658d1b4a4375bf5bcf50896cd45a7ee8c73797449ccd949a628118
Value:
e361189f9363a9d8b69b58f48184096282e2b8a7e3b07a28854707de32ad2e18
Content:
00+VESIT

Input
Value:
f1534392279bddbf9d43dde8701cb5be14b82f76ec6607bf8d6ad557f60f304e
Content:
00

Input
Value:
b2443eb348658d1b4a4375bf5bcf50896cd45a7ee8c73797449ccd949a628118
Content:
VESIT

Left:
656a4169d83cb92bf63b87384d844ab85c4d2c8dca59a11ba791d99bb81348e0
Right:
656a4169d83cb92bf63b87384d844ab85c4d2c8dca59a11ba791d99bb81348e0
Value:
b40441469667d9e22dc2c10e86a2eef53f213043439bfda7931ddf9628c87310
Content:
https://xyz.com/+https://xyz.com/

Input
Value:
656a4169d83cb92bf63b87384d844ab85c4d2c8dca59a11ba791d99bb81348e0
Content:
https://xyz.com/

Input
(Padding)
Value:
656a4169d83cb92bf63b87384d844ab85c4d2c8dca59a11ba791d99bb81348e0
Content:
https://xyz.com/


Process finished with exit code 0


