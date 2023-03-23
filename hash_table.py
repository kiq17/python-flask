class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, tableSize):
        self.tableSize = tableSize
        self.hashTable = [None] * tableSize

    def customHash(self, key):
        hashValue = 0
        for i in key:
            hashValue += ord(i)
            # para não ser maior que o tamanho do array
            hashValue = (hashValue * ord(i)) % self.tableSize
        return hashValue

    def addKeyValue(self, key, value):
        hashedKey = self.customHash(key)
        if self.hashTable[hashedKey] is None:
            self.hashTable[hashedKey] = Node(Data(key, value), None)
        else:
            node = self.hashTable[hashedKey]
            while node.next:
                node = node.next

            node.next = Node(Data(key, value), None)

    def getValue(self, key):
        hashedKey = self.customHash(key)
       # print(hashedKey)
        if self.hashTable[hashedKey] is not None:
            node = self.hashTable[hashedKey]
            if node.next is None:
                return node.data.value

            while node.next:
                if key == node.data.key:
                    return node.data.value

                node = node.next

            # verificando o ultimo elemento do array
            if key == node.data.key:
                return node.data.value
        return None

    def printTable(self):
        print("{")
        for i, val in enumerate(self.hashTable):
            if val is not None:
                node = val
                listString = ""
                if node.next:
                    while node.next:
                        listString += (
                            str(node.data.key) + " : " +
                            str(node.data.value) + " --> "
                        )
                        node = node.next

                    listString += (
                        str(node.data.key) + " : " +
                        str(node.data.value) + " --> None"
                    )

                    print(f"   [{i}] = {listString}")
                else:
                    print(f"   [{i}] = {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] = {val}")
        print("}")


""" ht = HashTable(6)
ht.addKeyValue("title", "asd")
ht.addKeyValue("body", "aaa")
ht.addKeyValue("date", "bbb")
ht.addKeyValue("userId", 1)
print(ht.getValue("title"))
print(ht.getValue("body"))
print(ht.getValue("date"))
print(ht.getValue("userId")) """
""" ht.printTable() """
