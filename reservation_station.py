
class Reservation_Station:
    def __init__(self):
        self.tag = None
        self.busy= False
        self.opcode= None
        self.vj= None
        self.vk= None
        self.qj= None
        self.qk= None
        self.a= None

    def issue(self, tag, opcode, vj, vk, qj, qk, a):
        self.busy = True
        self.opcode = opcode
        self.tag = tag
        self.a = a
        if qj == None:
            self.vj = vj
        else:
            self.qj = qj
            self.vj = None
        if qk == None:
            self.vk = vk
        else:
            self.qk = qk
            self.vk = None

    def update(self, vj, vk):
        if vj != None:
            self.vj = vj
            self.qj = None
        if vk != None:
            self.vk = vk
            self.qk = None

    def clear(self)
        self.tag = None
        self.busy= False
        self.opcode= None
        self.vj= None
        self.vk= None
        self.qj= None
        self.qk= None
        self.a= None