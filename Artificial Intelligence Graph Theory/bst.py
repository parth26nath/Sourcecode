# Import necessary libraries
from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Int, Field, Schema, List, Mutation, Argument

# Define the Node class for Binary Search Tree
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

# Binary Search Tree class with insertion, search, and deletion functionalities
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def search(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def deleteNode(self, root, key):
        if root is None:
            return root
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.minValueNode(root.right)
            root.val = temp.val
            root.right = self.deleteNode(root.right, temp.val)
        return root

    def inOrderTraversal(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inOrderTraversal(root.left, result)
            result.append(root.val)
            self.inOrderTraversal(root.right, result)
        return result

# Instantiate Binary Search Tree object
bst = BinarySearchTree()

# Define GraphQL Types
class BSTNode(ObjectType):
    value = Int()

class Query(ObjectType):
    search = Field(BSTNode, key=Int(required=True))
    inOrder = List(Int)

    def resolve_search(self, info, key):
        result = bst.search(bst.root, key)
        return BSTNode(value=result.val) if result else None

    def resolve_inOrder(self, info):
        return bst.inOrderTraversal(bst.root)

class InsertNode(Mutation):
    class Arguments:
        key = Int(required=True)

    ok = String()

    def mutate(self, info, key):
        bst.root = bst.insert(bst.root, key)
        return InsertNode(ok=f"Node with key {key} inserted.")

class DeleteNode(Mutation):
    class Arguments:
        key = Int(required=True)

    ok = String()

    def mutate(self, info, key):
        bst.root = bst.deleteNode(bst.root, key)
        return DeleteNode(ok=f"Node with key {key} deleted.")

class Mutation(ObjectType):
    insert = InsertNode.Field()
    delete = DeleteNode.Field()

# Create the Schema for GraphQL
schema = Schema(query=Query, mutation=Mutation)

# Setup Flask and GraphQL endpoint
app = Flask(__name__)
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=True)
