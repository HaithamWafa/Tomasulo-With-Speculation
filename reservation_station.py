
class Reservation_Station:
    def __init__(self,name_station,delay_cycles):
        self.name=name_station
        self.busy= 'N'
        self.opcode= "NOP"
        self.vj= "NULL"
        self.vk= "NULL"
        self.qj= "NULL"
        self.qk= "NULL"
        self.a= "NULL"
        self.delay=delay_cycles
