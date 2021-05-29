# coding=UTF-8
import os

func = [{
  'add':'100000',
  'addu':'100001',
  'sub':'100010',
  'subu':'100011',
  'and':'100100',
  'or':'100101',
  'xor':'100110',
  'nor':'100111',
  'slt':'101010',
  'sltu':'101000',
  'sll':'000000',
  'srl':'000010',
  'sra':'000011',
  'sllv':'000100',
  'srlv':'000110',
  'srav':'000111',
  'jr':'001000'
},{
  '100000':'add',
  '100001':'addu',
  '100010':'sub',
  '100011':'subu',
  '100100':'and',
  '100101':'or',
  '100110':'xor',
  '100111':'nor',
  '101010':'slt',
  '101000':'sltu',
  '000000':'sll',
  '000010':'srl',
  '000011':'sra',
  '000100':'sllv',
  '000110':'srlv',
  '000111':'srav',
  '001000':'jr'
}
]

opcode = [{
  'R':'000000',
  # i型指令
  'addi':'001000',
  'addiu':'001001',
  'andi':'001100',
  'ori':'001101',
  'xori':'001110',
  'lui':'001111',
  'lw':'100011',
  'sw':'101011',
  'beq':'000100',
  'bne': '000101',
  'slti':'001010',
  'sltiu':'001011',
  # j型指令
  'j':'000010',
  'jal':'000011',
},{
  '000000':'R',
  # i型指令
  '001000':'addi',
  '001001':'addiu',
  '001100':'andi',
  '001101':'ori',
  '001110':'xori',
  '001111':'lui',
  '100011':'lw',
  '101011':'sw',
  '000100':'beq',
  '000101':'bne',
  '001010':'slti',
  '001011':'sltiu',
  # j型指令
  '000010':'j',
  '000011':'jal'
}
]


def bin2s(ins):
  op = ins[0:6]
  s = ''
  if opcode[1][op] == 'R':
    funct = ins[26:32]
    Rop = func[1][funct]
    s = Rop + ' '
    if (Rop == 'sll' or Rop == 'srl' or Rop == 'sra'):
      shamt = hex(int(ins[21:26],base=10))
      reg1 = '$' + hex(int(ins[16:21],base=2))[2:]
      reg2 = '$' + hex(int(ins[11:16],base=2))[2:]
      s +=  reg2 + ' ' + reg1 + ' ' + shamt
      return s
    elif funct == 'jr':
      reg1 = '$' + hex(int(ins[6:11],base=2))[2:]
      s+=reg1
    else :
      reg1 = '$' + hex(int(ins[16:21],base=2))[2:]
      reg2 = '$' + hex(int(ins[11:16],base=2))[2:]
      reg3 = '$' + hex(int(ins[6:11],base=2))[2:]
      s += reg3 + ' ' + reg2 + ' ' + reg1
      return s

  elif opcode[1][op] == 'j' or opcode[1][op] == 'jal':
    s = opcode[1][op] + ' '
    address = hex(int(ins[6:32],base=2))
    s += address
    return s

  else :
    s = opcode[1][op] + ' '
    imm = hex(int(ins[16:32],base=2))
    reg1 = '$' + hex(int(ins[6:11],base=2))[2:]
    reg2 = '$' + hex(int(ins[11:16],base=2))[2:]
    if s == 'lui ':
      s +=  reg2 + ' ' + imm
    elif s == 'sw ' or s == 'lw ' :
      if imm != '0x0':
        s += reg1 + ' ' +imm + '(' + reg2 + ')'
      else :
        s+= reg1 + ' (' + reg2 + ')'
    else:
      s += reg1 + ' ' + reg2 + ' ' + imm
    return s


def formatBin(ins,length=32,ba = 2): 
  # 将一个合法字符串格式化为指令二进制表示
  if len(ins) >= 2 and ins[0:2] == '0x':
    ins = ins[2:]
  ins = int(ins,base=ba)
  ins = bin(ins)[2:]
  if len(ins) < length:
    for i in range(0,length-len(ins)):
      ins  = '0' + ins
  return ins

def formatHex(ins,ba = 16,length = 8):
  # 将一个合法字符串格式化为指令的16进制表示
  ins = int(ins,base=ba)
  print(hex(ins))
  ins = hex(ins)[2:]
  if ins[len(ins)-1] == 'L':
    ins = ins[:-1]
  if len(ins) < length:
    for i in range(0,length - len(ins)):
      ins = '0' + ins
  return ins

def s2Hex(ins):
  token = ins.split()
  print(token)
  s=''
  temp = ''
  # 处理指令名
  if opcode[0].get(token[0]) == None:
    s = '000000'
    temp = formatBin(func[0][token.pop(0)],length=6)
  else :
    temp =formatBin( opcode[0][token.pop(0)],length=6)
    s += temp
  # 特殊处理一地址指令 jr,j,jal
  if len(token) == 1:
    if s == '000000':
      reg1 = formatBin(bin(int(token[0][1:],base=16)),length=5)
      s = s + reg1 + formatBin('0',15) + temp
      print(s)
      return formatHex(s,ba=2)
    else :
      address = formatBin(token[0],length=26,ba=16)
      s += address
      return formatHex(s,ba=2)
  # r型指令
  if s == '000000':
    funct = func[1][temp]
    if funct == 'sll' or funct == 'srl' == funct == 'sra':
      reg1 = formatBin(token.pop(0)[1:],length=5,ba=16)
      reg2 = formatBin(token.pop(0)[1:],length=5,ba=16)
      shamt = formatBin(token.pop(0),length=5,ba=16)
      s = s + '00000' + reg1 + reg2 + shamt + temp
      print(s)
      return formatHex(s,ba=2,length=8)
    else :
      reg1 = formatBin(token.pop(0)[1:],length=5,ba=16)
      reg2 = formatBin(token.pop(0)[1:],length=5,ba=16)
      reg3 = formatBin(token.pop(0)[1:],length=5,ba=16)
      s = s + reg1 + reg2 + reg3 + '00000' + temp
      print(s)
      return formatHex(s,ba=2,length=8)
  # i型指令的翻译
  if opcode[1][s] == 'lui':
    reg1 = formatBin(token.pop(0)[1:],length=5,ba=16)
    imm = formatBin(token.pop(0),length=16,ba=16)
    s = s + '00000' + reg1 + imm
    print(s)
    return formatHex(s,ba=2,length=8)
  # sw 和 lw 的特殊处理
  elif opcode[1][s] == 'sw' or opcode[1][s] == 'lw':
    reg1 = formatBin(token.pop(0)[1:],length=5,ba=16)
    index = token[0].find("(")
    if index > 0:
      imm = formatBin(token[0][0:index],length=16,ba=16)
    else :
      imm = formatBin('0',length=16)
    reg2 = formatBin(token[0][index + 2 :token[0].find(")")],length=5,ba=16)
    s = s + reg1 + reg2 + imm
    return formatHex(s,ba=2)
  else :
    reg1 = formatBin(token.pop(0)[1:],length=5,ba=16)
    reg2 = formatBin(token.pop(0)[1:],length=5,ba=16)
    imm = formatBin(token.pop(0),length=16,ba=16)
    s =  s + reg1 + reg2 + imm
    print(s)
    return formatHex(s,ba=2)

def sFile(file):
  writeFile = open(r'data.txt','w')
  with open(file,'r') as f:
      ins = f.readline()
      while ins:
        ins = formatBin(ins[:-1],length=32,ba=16)
        inst = bin2s(ins)
        print(ins)
        print(inst)
        writeFile.write(inst + '\n')
        ins = f.readline()
      f.close()
  writeFile.close()

def hexFile(file):
  writeFile = open(r'hex.data','w')
  with open(file,'r') as f:
    ins = f.readline()
    while ins:
      inst = s2Hex(ins[:-1])
      # print(ins)
      # print(inst)
      writeFile.write(inst + '\n')
      ins = f.readline()
    f.close()
  writeFile.close()

if __name__ == "__main__":
  file = 'C:\Users\wnx\Desktop\inst.data'
  sFile(file)
  hexFile('data.txt')
 
 