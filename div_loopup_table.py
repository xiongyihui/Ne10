
from __future__ import print_function


def print_table(table):
    print('')
    for i in range(len(table)):
        if i % 16 == 15:
            print('{},'.format(table[i]))
        else:
            print('{}, '.format(table[i]), end='')

    print('')



#-------------------------------------------------------------------------------
#                     @//outBlockSize = blockSize / S->M
# #ifdef __PIC__
#                     @/* position-independent access of LDR pMask,=ne10_divLookUpTable */
#                     LDR         pTemp,.L_PIC1_GOT_OFFSET
#                     LDR         pMask,.L_GOT_ne10_divLookUpTable
# .L_PIC1:
#                     ADD         pTemp,pTemp,pc
#                     LDR         pMask,[pTemp,pMask]
# #else
#                     LDR         pMask,=ne10_divLookUpTable
# #endif
#                     SUBS        mask,decimationFact,#1
#                     ADD         pMask,pMask,mask,LSL #2
#                     LDR         mask,[pMask]
#                     @//MOV         pX,#0


#                     SMULWB      outBlockSize,blockSize,mask
#                     CMP         outBlockSize,#0
#                     IT          LT
#                     RSBLT       outBlockSize,#0
#-------------------------------------------------------------------------------



div_loopup_table = [
    65535,32768,21845,16384,13107,10923,9362,8192,7282,6554,5958,5461,5041,4681,4369,4096,
    3855,3641,3449,3277,3121,2979,2849,2731,2621,2521,2427,2341,2260,2185,2114,2048,
    1986,1928,1872,1820,1771,1725,1680,1638,1598,1560,1524,1489,1456,1425,1394,1365,
    1337,1311,1285,1260,1237,1214,1192,1170,1150,1130,1111,1092,1074,1057,1040,1024,
    1008,993,978,964,950,936,923,910,898,886,874,862,851,840,830,819,
    809,799,790,780,771,762,753,745,736,728,720,712,705,697,690,683,
    676,669,662,655,649,643,636,630,624,618,612,607,601,596,590,585,
    580,575,570,565,560,555,551,546,542,537,533,529,524,520,516,512,
    508,504,500,496,493,489,485,482,478,475,471,468,465,462,458,455,
    452,449,446,443,440,437,434,431,428,426,423,420,417,415,412,410,
    407,405,402,400,397,395,392,390,388,386,383,381,379,377,374,372,
    370,368,366,364,362,360,358,356,354,352,350,349,347,345,343,341,
    340,338,336,334,333,331,329,328,326,324,323,321,320,318,317,315,
    314,312,311,309,308,306,305,303,302,301,299,298,297,295,294,293,
    291,290,289,287,286,285,284,282,281,280,279,278,277,275,274,273,
    272,271,270,269,267,266,265,264,263,262,261,260,259,258,257]


N = 2000
result1 = []

for i in range(len(div_loopup_table)):
    decimate_factor = i + 1
    block_size = N * decimate_factor
    out_block_size = int(block_size * div_loopup_table[i]) >> 16
    result1.append(out_block_size)

    # if out_block_size != int(block_size / decimate_factor):
    #     div_loopup_table[i] += 1
 
print_table(result1)


# result2 = []

# for i in range(len(div_loopup_table)):
#     decimate_factor = i + 1
#     block_size = 100 * decimate_factor
#     out_block_size = int(block_size * div_loopup_table[i] / (1 << 16))
#     result2.append(out_block_size)

# print_table(result2)

# print_table(div_loopup_table)


# import numpy as np


# test_size = np.random.randint(32, 10240, 100)

# for i in range(len(div_loopup_table)):
#     decimate_factor = i + 1

#     for size in test_size:
#         block_size = size * decimate_factor
#         out_block_size = int(block_size * div_loopup_table[i] / (1 << 16))

#         if out_block_size != int(block_size / decimate_factor):
#             print((i, div_loopup_table[i], out_block_size, size))
#             break