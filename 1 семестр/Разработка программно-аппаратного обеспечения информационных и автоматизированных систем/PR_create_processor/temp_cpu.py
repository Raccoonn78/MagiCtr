from enum import Enum

c_mem = [0] * 65536

EZ = False
TF = False
OF = False
LZ = False
PC = 0
REG_CMD = 32
REG_MEMORY = 32767


class CMD_TYPE(Enum):
    EMPTY = 0x0
    IREG = 0x7
    IMEM = 0x8
    RTM = 0x9
    RTR = 0xA
    MTRA = 0xB
    INC = 0xC
    DEC = 0xD
    SUB = 0xF
    JEZ = 0x10
    JLZ = 0x11
    JP = 0x12


def file_parse():
    file_path = 'text5.txt'
    f = open(file_path, 'r+')
    lines = [line.replace("\n", "").strip() for line in f.readlines()]
    return lines


def convert_to_bitset(array):
    t = [1 if array & (1 << (7 - n)) else 0 for n in range(8)]
    result = ''.join(str(x) for x in t)
    return result


def EMPTY():
    pass


def AND(op1, literal):
    c_mem[op1] &= literal >> 8
    c_mem[op1 + 1] &= literal & 255


def OR(op1, literal):
    c_mem[op1] |= literal >> 8
    c_mem[op1 + 1] |= literal & 255


def XOR(op1, literal):
    c_mem[op1] ^= literal >> 8
    c_mem[op1 + 1] ^= literal & 255


def NOT(op1):
    c_mem[op1] = ~c_mem[op1]
    c_mem[op1 + 1] = ~c_mem[op1 + 1]


def SHL(op1):
    c_mem[op1] = c_mem[op1] << 1
    c_mem[op1 + 1] = c_mem[op1 + 1] << 1


def SHR(op1):
    c_mem[op1] = c_mem[op1] >> 1
    c_mem[op1 + 1] = c_mem[op1 + 1] >> 1


def IREG(op1, literal):
    c_mem[op1] = literal


def IMEM(op1, literal):
    c_mem[op1] = literal


def RTM(op1, op2):
    c_mem[op1] = c_mem[op2]
    c_mem[op1 + 1] = c_mem[op2 + 1]


def RTR(op1, op2):
    c_mem[op1] = c_mem[op2]
    c_mem[op1 + 1] = c_mem[op2 + 1]


def MTRA(op1, op2):
    c_mem[op1] = c_mem[(c_mem[op2] << 8 | c_mem[op2 + 1])]
    c_mem[op1 + 1] = c_mem[(c_mem[op2] << 8 | c_mem[op2 + 1]) + 1]


def INC(op1):
    global EZ
    global TF
    if c_mem[op1 + 1] == 0 & c_mem[op1] == 0:
        EZ = True
    else:
        EZ = False
    if c_mem[op1 + 1] == 255:
        c_mem[op1 + 1] = 0
        c_mem[op1] += 1
        TF = True
    else:
        c_mem[op1 + 1] += 1


def DEC(op1):
    global EZ, TF
    if c_mem[op1 + 1] == 0 & c_mem[op1] == 0:
        EZ = True
    else:
        EZ = False
    if c_mem[op1 + 1] == 0:
        c_mem[op1 + 1] = 255
        c_mem[op1] -= 1
        TF = True
    else:
        c_mem[op1 + 1] -= 1


def ADD(op1, op2):
    global OF
    global LZ
    OF = ((c_mem[op1 + 1] < 0) == (c_mem[op2 + 1] < 0) & (c_mem[op1 + 1] + c_mem[op2 + 1] < 0) != (c_mem[op1 + 1] < 0))
    RTM(65534, op1)
    RTM(65532, op2)
    c_mem[op1 + 1] = ((c_mem[65534] << 8 | c_mem[65535]) + (c_mem[65532] << 8 | c_mem[65533]))
    c_mem[op1] = ((c_mem[65534] << 8 | c_mem[65535]) + (c_mem[65532] << 8 | c_mem[65533])) >> 8
    if int(c_mem[op1] << 8 | c_mem[op1 + 1]) < 0:
        LZ = True
    else:
        LZ = False


def SUB(op1, op2):
    NOT(op2)
    INC(op2)
    ADD(op1, op2)
    DEC(op2)
    NOT(op2)


def JEZ(literal):
    global EZ
    global PC
    if EZ:
        PC = literal
        EZ = False

    else:
        PC += 1


def JLZ(literal):
    global LZ
    global PC
    if LZ:
        PC = literal
        LZ = False

    else:
        PC += 1


def JMP(literal):
    global PC
    PC = literal


def show_command_memory():
    shows_elem = 108
    print("Память команд: \n")
    for i in range(REG_CMD, REG_CMD + shows_elem, 4):
        bitset1 = convert_to_bitset(c_mem[i])
        bitset2 = convert_to_bitset(c_mem[i + 1])
        bitset3 = convert_to_bitset(c_mem[i + 2])
        bitset4 = convert_to_bitset(c_mem[i + 3])
        print(i, ": ", bitset1, bitset2, bitset3, bitset4)


def show_data_memory():
    shows_elem = 16
    print("\nПамять данных")
    for i in range(REG_MEMORY, REG_MEMORY + shows_elem, 2):
        bitset1 = convert_to_bitset(c_mem[i])
        bitset2 = convert_to_bitset(c_mem[i + 1])
        number = int(bitset1 + bitset2, base=2)
        print(i, ": ", bitset1, bitset2, number)

    m_bitset1 = convert_to_bitset(c_mem[32775])
    m_bitset2 = convert_to_bitset(c_mem[32776])
    print('Максимальный элемент массива: ', int(m_bitset1 + m_bitset2, base=2))


def dec_to_bin(x):
    return str(int(bin(x)[2:]))


def hex_to_bin(x):
    return bin(int(x, 16))[2:].zfill(len(x) * 4)


def parse_assembly():
    lines = file_parse()
    global ptr, pt
    ptr = 0
    pt = 0
    for line in lines:
        command = line.replace(",", "").split(" ")
        if command[0] == CMD_TYPE.IMEM.name.lower():
            hex_n = hex(int(command[2])).replace("0x", "")
            l = len(hex_n) + 1
            part_1 = hex_n[0:l // 2]
            part_2 = hex_n[l // 2:]

            c_mem[REG_CMD + ptr] = CMD_TYPE.IMEM.value
            c_mem[REG_CMD + ptr + 1] = (int(hex_to_bin(part_1), 2))
            c_mem[REG_CMD + ptr + 2] = 128
            c_mem[REG_CMD + ptr + 3] = pt + 1

            c_mem[REG_CMD + ptr + 4] = CMD_TYPE.IMEM.value
            c_mem[REG_CMD + ptr + 5] = (int(hex_to_bin(part_2), 2))
            c_mem[REG_CMD + ptr + 6] = 128
            c_mem[REG_CMD + ptr + 7] = pt + 2
            ptr += 8
            pt += 2

        if command[0] == CMD_TYPE.IREG.name.lower():
            c_mem[REG_CMD + ptr] = CMD_TYPE.IREG.value
            c_mem[REG_CMD + ptr + 1] = int(command[2])
            c_mem[REG_CMD + ptr + 2] = 0x0
            c_mem[REG_CMD + ptr + 3] = int(command[1])
            ptr += 4

        if command[0] == CMD_TYPE.MTRA.name.lower():
            c_mem[REG_CMD + ptr + 1] = CMD_TYPE.MTRA.value
            c_mem[REG_CMD + ptr + 2] = int(command[1])
            c_mem[REG_CMD + ptr + 3] = 0x0
            c_mem[REG_CMD + ptr + 4] = int(command[2])
            ptr += 4

        if command[0] == CMD_TYPE.JEZ.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.JEZ.value
            c_mem[REG_CMD + 2] = 0x0
            c_mem[REG_CMD + 3] = 0x0
            c_mem[REG_CMD + 4] = 0x68
            ptr += 4

        if command[0] == CMD_TYPE.JP.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.JP.value
            c_mem[REG_CMD + 2] = 0x0
            c_mem[REG_CMD + 3] = 0x0
            c_mem[REG_CMD + 4] = 0x40
            ptr += 4

        if command[0] == CMD_TYPE.RTM.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.RTM.value
            c_mem[REG_CMD + 2] = int(command[2])
            c_mem[REG_CMD + 3] = 0x80
            c_mem[REG_CMD + 4] = 0x07
            ptr += 4

        if command[0] == CMD_TYPE.DEC.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.DEC.value
            c_mem[REG_CMD + 2] = 0x0
            c_mem[REG_CMD + 3] = 0x0
            c_mem[REG_CMD + 4] = int(command[1])
            ptr += 4

        if command[0] == CMD_TYPE.INC.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.INC.value
            c_mem[REG_CMD + 2] = 0x0
            c_mem[REG_CMD + 3] = 0x0
            c_mem[REG_CMD + 4] = int(command[1])
            ptr += 4

        if command[0] == CMD_TYPE.SUB.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.SUB.value
            c_mem[REG_CMD + 2] = int(command[1])
            c_mem[REG_CMD + 3] = 0x0
            c_mem[REG_CMD + 4] = int(command[2])
            ptr += 4

        if command[0] == CMD_TYPE.JLZ.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.JLZ.value
            c_mem[REG_CMD + 2] = 0x0
            c_mem[REG_CMD + 3] = 0x0
            c_mem[REG_CMD + 4] = 0x54
            ptr += 4

        if command[0] == CMD_TYPE.RTR.name.lower():
            c_mem[REG_CMD + 1] = CMD_TYPE.RTR.value
            c_mem[REG_CMD + 2] = int(command[1])
            c_mem[REG_CMD + 3] = 0x0
            c_mem[REG_CMD + 4] = int(command[2])
            ptr += 4


def main():
    global PC
    parse_assembly()

    while True:
        cmd_type = c_mem[REG_CMD + PC * 4]
        literal = c_mem[REG_CMD + PC * 4 + 1]
        op1 = c_mem[REG_CMD + PC * 4 + 2]
        op2 = c_mem[REG_CMD + PC * 4 + 3]
        cmd_address = op1 << 8 | op2

        if PC * 4 == 100:
            break

        if cmd_type == CMD_TYPE.EMPTY.value:
            EMPTY()
            PC += 1

        elif cmd_type == CMD_TYPE.IREG.value:
            IREG(cmd_address, literal)
            PC += 1

        elif cmd_type == CMD_TYPE.IMEM.value:
            IMEM(cmd_address, literal)
            PC += 1

        elif cmd_type == CMD_TYPE.RTM.value:
            RTM(cmd_address, literal)
            PC += 1

        elif cmd_type == CMD_TYPE.RTR.value:
            RTR(literal, cmd_address)
            PC += 1

        elif cmd_type == CMD_TYPE.MTRA.value:
            MTRA(literal, cmd_address)
            PC += 1

        elif cmd_type == CMD_TYPE.INC.value:
            INC(cmd_address)
            PC += 1

        elif cmd_type == CMD_TYPE.DEC.value:
            DEC(cmd_address)
            PC += 1

        elif cmd_type == CMD_TYPE.SUB.value:
            SUB(literal, cmd_address)
            PC += 1

        elif cmd_type == CMD_TYPE.JEZ.value:
            JEZ(cmd_address / 4)

        elif cmd_type == CMD_TYPE.JLZ.value:
            JLZ(cmd_address / 4)

        elif cmd_type == CMD_TYPE.JP.value:
            JMP(cmd_address / 4)

        else:
            PC += 1

    show_data_memory()


if __name__ == '__main__':
    main()
