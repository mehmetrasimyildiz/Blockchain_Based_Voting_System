
import hashlib
import math


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def isFull(self):
        return self.left and self.right

    def __str__(self):
        return self.data

    def isLeaf(self):
        return ((self.left == None) and (self.right == None))


class merkleTree:

    def __init__(self):
        self.root = None
        self._merkleRoot = ''

    def __returnHash(self, x):
        return (hashlib.sha256(x.encode()).hexdigest())

    def makeTreeFromArray(self, arr):

        def __noOfNodesReqd(arr):
            x = len(arr)
            return (2 * x - 1)

        def __buildTree(arr, root, i, n):

            if i < n:
                temp = Node(str(arr[i]))
                root = temp

                root.left = __buildTree(arr, root.left, 2 * i + 1, n)

                root.right = __buildTree(arr, root.right, 2 * i + 2, n)

            return root


        def __addLeafData(arr, node):

            if not node:
                return

            __addLeafData(arr, node.left)
            if node.isLeaf():
                node.data = self.__returnHash(arr.pop())
            else:
                node.data = ''
            __addLeafData(arr, node.right)


        nodesReqd = __noOfNodesReqd(arr)
        nodeArr = [num for num in range(1, nodesReqd + 1)]
        self.root = __buildTree(nodeArr, self.root, 0, nodesReqd)
        __addLeafData(arr, self.root)

    def inorderTraversal(self, node):
        if not node:
            return

        self.inorderTraversal(node.left)
        print(node)
        self.inorderTraversal(node.right)


    def calculateMerkleRoot(self):

        def __merkleHash(node):
            if node.isLeaf():
                return node

            left = __merkleHash(node.left).data
            right = __merkleHash(node.right).data
            node.data = self.__returnHash(left + right)
            return node

        merkleRoot = __merkleHash(self.root)
        self._merkleRoot = merkleRoot.data

        return self._merkleRoot


    def getMerkleRoot(self):
        return self._merkleRoot


    def verifyUtil(self, arr1):
        hash1 = self.getMerkleRoot()
        new_tree = merkleTree()
        new_tree.makeTreeFromArray(arr1)
        new_tree.calculateMerkleRoot()
        hash2 = new_tree.getMerkleRoot()
        if hash1 == hash2:
            print("Transactions verified Successfully")
            return True
        else:
            print("Transactions have been tampered")
            return False
