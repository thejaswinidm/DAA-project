   
import os
import math
import argparse
import numpy as np
from core import Symbol
import core
from encoder import encode
from decoder import decode
from saveToFile import saveToFile
from readFromFile import readFromFile

def blocks_write(blocks, file, filesize):
    """ Write the given blocks into a file
    """

    count = 0
    for data in recovered_blocks[:-1]:
        file_copy.write(data)
        count += len(data)

    # Convert back the bytearray to bytes and shrink back 
    last_bytes = bytes(recovered_blocks[-1])
    shrinked_data = last_bytes[:filesize % core.PACKET_SIZE]
    file_copy.write(shrinked_data)

#########################################################

parser = argparse.ArgumentParser(description="Robust implementation of LT Codes encoding/decoding process.")
parser.add_argument("filename", help="file path of the file to split in blocks")
parser.add_argument("-r", "--redundancy", help="the wanted redundancy.", default=2.0, type=float)
parser.add_argument("--systematic", help="ensure that the k first drops are exactly the k first blocks (systematic LT Codes)", action="store_true")
parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("--x86", help="avoid using np.uint64 for x86-32bits systems", action="store_true")
args = parser.parse_args()

core.NUMPY_TYPE = np.uint32 if args.x86 else core.NUMPY_TYPE
core.SYSTEMATIC = True if args.systematic else core.SYSTEMATIC 
core.VERBOSE = True if args.verbose else core.VERBOSE    
filesize = os.path.getsize(args.filename)

file_symbols1 = readFromFile("byteFiles")
file_blocks_size_file = open("file_blocks_size_file.txt","r+")
file_blocks_n = int(file_blocks_size_file.read())
file_blocks_size_file.close()
# HERE: Simulating the loss of packets?
file_symbols = file_symbols1
# Recovering the blocks from symbols
print("file size",len(file_symbols),len(file_symbols1))

recovered_blocks, recovered_n = decode(file_symbols, blocks_quantity=file_blocks_n)

if core.VERBOSE:
    print(recovered_blocks)
    print("------ Blocks :  \t-----------")
    print(file_blocks)

if recovered_n != file_blocks_n:
    print("All blocks are not recovered, we cannot proceed the file writing")
    exit()

splitted = args.filename.split(".")
if len(splitted) > 1:
    filename_copy = "".join(splitted[:-1]) + "-copy." + splitted[-1] 
else:
    filename_copy = args.filename + "-copy"

# Write down the recovered blocks in a copy 
with open(filename_copy, "wb") as file_copy:
    blocks_write(recovered_blocks, file_copy, filesize)

print("Wrote {} bytes in {}".format(os.path.getsize(filename_copy), filename_copy))


