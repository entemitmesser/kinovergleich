def reverse(x: int) -> int:
    x_tostring = str(x)
    int_list = list(x_tostring)
    reverse_str = ""
    for i in range(len(int_list)):
        int_list.insert(0, int_list[-1])
        int_list.pop(-1)
    for x in int_list:
        reverse_str += x

    return(int(reverse_str))

