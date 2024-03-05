#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tiny-P CPU Simulator.
Tiny-P is a simple CPU Simulator intended as a teaching aid for students
learning about computer architecture.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Randall Morgan"
__contact__ = "rmorgan@coderancher.us"
__copyright__ = "Copyright 2022, SensorNet"
__credits__ = ["Randall Morgan", "SensorNet.Us"]
__date__ = "2022/05/23"
__deprecated__ = False
__email__ =  "rmorgan@coderancher.us"
__license__ = "GPLv2 or Later"
__maintainer__ = "Randall Morgan"
__status__ = "Production"
__version__ = "1.0.0"

# Tiny-P Machine Code Loader
# Assumes machine code is stored in
# a *.bin file and is formatted as:
# <address> <opcode>
# Where the address is a 3-digit decimal
# value and the opcode is a 3-digit
# decimal value.

import sys, getopt

from microcode import CPU


class Loader:
    def __init__(self, cpu: CPU, code_text: str):
        self.machine_code = code_text
        self.code = self.machine_code.split('\n')
        self.cpu = cpu

    def cpu_init(self):
        self.cpu.init_rom()
        self.cpu.reset()

    def load(self):
        for line in self.code:
            code = line.split()
            if len(code) == 2:
                addr = int(code[0])
                opcode = int(code[1])
                self.cpu.program(addr, opcode)


def main(argv):
    inputfile = 'C:\\Users\\Admin\\Desktop\\VS_code\\magic\\MagiCtr\\Разработка программно-аппаратного обеспечения информационных и автоматизированных систем\\PR_create_processor\\example.bin'
    usage_message = "Usage: assembler.py -i <inputfile> "

    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "ifile="])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage_message)
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg

    if not inputfile:
        print(usage_message)
        sys.exit(2)

    with open(inputfile, 'r') as ifh:
        program_text = ifh.read()
    ifh.close()

    # Loader program
    cpu = CPU()
    loader = Loader(cpu, program_text)
    loader.cpu_init()
    loader.load()

    # Exit message
    print(f"Loader: {inputfile} loaded in to cpu.")
    print(f"Ready to run!")

    # Run the program
    cpu.step()
    dump(cpu)
    cpu.step()
    dump(cpu)
    cpu.step()
    dump(cpu)


def dump(cpu: CPU):
    print(f"ACC: {cpu.acc}, PC: {cpu.pc}, Z: {cpu.zero_flag}, P: {cpu.pos_flag}")
    dump_mem(cpu.mem)
    print()
    dump_mem(cpu.prog)
    print('\n')


def dump_mem(mem: list):
    for i, data in enumerate(mem):
        if i % 15 == 0: print(f"\n{i} : ", end='')
        print(f" {data}, ", end='')


if __name__ == "__main__":
    main(sys.argv[1:])