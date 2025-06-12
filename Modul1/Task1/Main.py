# первый мой вариант реализации

class LinkedList():
    head = None
    tail = None

    def add_obj(self, obj):
        if self.head == None:
            self.head = obj
        else:
            if self.head.get_next() == None:
                self.head.set_next(obj)

            if self.tail == None:
                self.tail = obj
                self.tail.set_prev(self.head)
            else:
                self.tail.set_next(obj)

                prev_obj = self.tail

                self.tail = obj

                self.tail.set_prev(prev_obj)

    def remove_obj(self):
        if not (self.tail and self.head):
            return None

        self.tail = self.tail.get_prev()
        if self.tail != None:
            self.tail.set_next(None)
        else:
            self.head = None

    def get_data(self):
        list_obj = []

        if self.head != None:
            current_obj = self.head
        else:
            return []

        while True:
            list_obj.append(current_obj.get_data())

            if current_obj.get_next() == None:
                break

            current_obj = current_obj.get_next()

        return list_obj


class ObjList():

    def __init__(self, data, next=None, prev=None):
        self.__next = next
        self.__prev = prev
        self.__data = data

    def set_next(self, obj):
        self.__next = obj

    def get_next(self):
        return self.__next

    def set_prev(self, obj):
        self.__prev = obj

    def get_prev(self):
        return self.__prev

    def set_data(self, data):
        self.__data = data

    def get_data(self):
        return self.__data

