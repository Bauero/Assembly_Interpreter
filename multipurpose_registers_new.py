
def get_low(register, range : list, value = None):
    if value:
        register[range[0]:range[1]] = value
        return
    return register[range[0]:range[1]]

class sub_register():

    def


EAX = [0 for _ in range(32)]

AL = get_low(EAX, [24, 0])

print(AL)

EAX[-1] = 10

print(AL)

