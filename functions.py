def mov(arg1, arg2, rejestry):
    if type(arg1) == str and type(arg2) == str:
        rejestry[arg1].mov(rejestry[arg2])

    elif type(arg1) == str and type(arg2) == int:
        rejestry[arg1].mov(arg2)

        