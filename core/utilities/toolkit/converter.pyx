
cdef class Converter:
    def date_obj_to_str(self, int element) -> str:
        if element <= 9:
            return "0" + str(element)
        return str(element)