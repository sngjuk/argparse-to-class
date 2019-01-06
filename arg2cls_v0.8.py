#!/usr/bin/env python3
from collections import OrderedDict
import sys
import re
DBG = False

#add_argument, set_defaults only available.
ListStartPatt = re.compile('(\[.*)')
ListPatt = re.compile('(\[.*?\])')
GbgPatt = re.compile('(.*)\)[A-z0-9*]')
LpRegex = re.compile('\({1,}\s{0,}')
RpRegex = re.compile('\s{0,}\){1,}')
PrRegex = re.compile('\((.*)(\))(?!.*\))') # from \( to last \)
CmRegex = re.compile('\s{0,},\s{0,}')
StrRegex = re.compile('\'(.*?)\'')

# Argument dict : store {arg_name : value}
argDct=OrderedDict()

# Remove empty line & Concatenate line-separated syntax.
def preprocess(fname):
  try :
    with open(fname, 'r', encoding='UTF8') as f:
      txt = f.read()
      t = txt.splitlines(True)
      t = str_list = list( filter(None, t) )
      # remove empty line
      t = [x for x in t if not re.match('\s{0,}\n',x)]
      # concatenate multiple lined arguments.
      empl = []
      for i in range(len(t)-1, 0, -1):
        if not re.search('add_argument|set_defaults', t[i]):
          t[i-1] += t[i]
          t[i-1]=re.sub('\s{0,}\n{0,}\s{0,}','',t[i-1])
          empl.append(t[i])

      for d in empl:
        t.remove(d)
      for i, line in enumerate(t):
        t[i] = line.replace('\"', '\'')
      return t

  except IOError:
      print('IOError : no such file.', fname)

# Handling add_argument()
def add_argument(arg_line):
  global argDct

  arg_line = arg_line
  if DBG:
    print('in add_argument : **Pr regex : ' + str(arg_line))

  #argname = DdRegex.split(arg_line)[1] # Dash or regex for arg name.
  argname = re.search('\'--(.*?)\'',arg_line)
  if not argname:
    argname = re.search('\'-+(.*?)\'',arg_line)
  if argname:
    argname = argname.group(1).replace('-', '_')
  else :
    argname = StrRegex.search(arg_line).group(1)
    if not argname:
        return # no argument name

  argDct[argname]=''
  dtype = re.search(',\s*type\s*=(.*)', arg_line)
  if dtype:
    dtype = dtype.group(1)
    dtype = CmRegex.split(dtype)[0]
  else :
    dtype = ''

  dfult = re.search(',\s*default\s*=(.*)',arg_line)
  rquird = re.search(',\s*required\s*=(.*)',arg_line)
  action = re.search(',\s*action\s*=(.*)',arg_line)

  tval = ''
  if dfult:
    if DBG:
      print('default exist')
    # type exist
    if re.search('int|float|long|bool|complex', dtype):
      tval = dfult.group(1)
      if DBG:
        print('type exist tval :' +str(tval))

      # default value handling..
      # Check if default value has list starting patern.
      CommaSeparated = CmRegex.split(tval)[0]
      if ListStartPatt.search(CommaSeparated):
        tval = ListPatt.search(tval).group(1)
        if DBG:
          print('list patt exist tval : ' + str(tval))
      else :
        tval = CmRegex.split(tval)[0]
        if DBG:
          print('no list tval :' +str(tval))
      
      # if default value is not like - int('inf') , remove characters after ')' and remove garbage.
      if not re.search('int|float|long|bool|complex', tval) and not LpRegex.search(tval):
        tval = re.split('\s{0,}\){1,}',tval)[0]
        if DBG:
          print('before gbg, handling paranthes')
      gbg = re.search(GbgPatt, tval)
      if gbg:
        tval = gbg.group(1)

    # As type is not specified, we assume it as str type.
    else:
      if DBG:
        print('no type exist')
      tval = dfult.group(1)
      
      # find str pattern in default value.
      regres = StrRegex.match(tval) 
      if regres:
        tval = regres.group(0)
      # not found.
      else:
        # default value handling..
        # Check if default value has list starting patern.
        CommaSeparated = CmRegex.split(tval)[0]
        if ListStartPatt.search(CommaSeparated):
          tval = ListPatt.search(tval).group(1)
          if DBG:
            print('list patt exist tval : ' + str(tval))
        else:
          tval = CmRegex.split(tval)[0]
          if DBG:
            print('no list tval : ' +str(tval))

        # if default value is not like - int('inf') , remove characters after ')' and remove garbage.
        if not re.search('int|float|long|bool|complex', tval) and not LpRegex.search(tval):
          tval = re.split('\s{0,}\){1,}',tval)[0]
          if DBG:
            print('before gbg, handling paranthes')
        gbg = re.search(GbgPatt, tval)
        if gbg:
          tval = gbg.group(1)

   
    if DBG:
      print('value determined : ' + str(tval) +'\n')

  # action or required syntaxes exist
  elif action or rquird :
    if DBG:
      print('in action handling')
    msg_str = ''
    if action:
      tval = action.group(1)
      msg_str = 'action'
    else : #required.
      tval = rquird.group(1)
      msg_str = 'required'

    regres = StrRegex.search(tval)
    if regres:
      tval = regres.group(0)
    else :
      tval = CmRegex.split(tval)[0]
    tval = '## ' + msg_str + ' ' + tval + ' ##'
  
  else :
    argDct[argname] = '## default None ##'

  if tval:
    argDct[argname] = tval

# Handling set_default()
def set_defaults(arg_line):
  global argDct
  if DBG:
    print('Set_defaults : ' + str(arg_line))

  dfult = re.split('\s{0,}=\s{0,}', arg_line)
  tn = dfult[0] # arg name
  tv = RpRegex.split(dfult[1])[0] #arg value
  argDct[tn]=tv

def transform(fname):
  # t : list() contains add_argument|set_defaults lines.
  arg_line_list = preprocess(fname)

  for i, arg_line in enumerate(arg_line_list):
    t = PrRegex.search(arg_line)
    if t:
      t = t.group(1) # t: content of add_argument Parentheses.
    else :
      continue # nothing to parse.

    if re.search('add_argument\s*\(', arg_line):
      add_argument(t)
    elif re.search('set_defaults\s*\(',arg_line):
      set_defaults(t)
    else :
      # Nothing to parse.
      continue

  print('\nclass args:')
  for i in argDct:
    print(' ',i, '=', argDct[i])
  print()

def main():
  if len(sys.argv) <2:
    print('Usage : python arg2cls.py [target.py] [target2.py(optional)] ...')
    sys.exit(0)
  sys.argv.pop(0)

  #handling multiple file input.
  for fname in sys.argv:
    transform(fname)

# TODO : choices=, multiple keywords occurence fix.    

if(__name__ == "__main__"):
  main()
