# код верью первого варианта реализации

class LinkedList():

    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj):
        if self.head is None:
            self.head = obj
            self.tail = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj

    def remove_obj(self):
       if self.head is None:
           return
       if self.tail.get_prev() is None:
           self.head = None
           self.tail = None
       else:
           self.tail = self.tail.get_prev()
           self.tail.set_next(None)

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

    def __init__(self, data):
        self.__next = None
        self.__prev = None
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
