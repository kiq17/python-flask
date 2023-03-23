class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self.last = None

    def printList(self):
        node = self.head
        string = ""

        if node is None:
            print("Lista vazia")
        while node:
            string += f"{str(node.data)} -> "
            node = node.next

        string += " Fim da lista"
        print(string)

    def inesertBegining(self, data):
        if self.head is None:
            self.head = Node(data)
            self.last = self.head
            return

        node = Node(data, self.head)
        self.head = node

    def insertAtEnd(self, data):
        if self.head is None:
            self.inesertBegining(data)
            return

        self.last.next = Node(data)
        self.last = self.last.next

    def userById(self, id):
        node = self.head
        while node:
            if node.data["id"] is int(id):
                return node.data
            node = node.next

        return None
        




list = LinkedList()
list.inesertBegining("New head")
list.inesertBegining("New head 2")
list.insertAtEnd("Final Node")
list.printList()
