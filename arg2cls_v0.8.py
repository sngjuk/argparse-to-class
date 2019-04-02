#!/usr/bin/env python3
from collections import OrderedDict
import sys
import re
DBG = False

#add_argument(), set_defaults() only available.
ListStartPatt = re.compile(r'\s*\[.*')
ListStartPatt2 = re.compile(r'\).*\[.*') # list out of function scope.
ListPatt = re.compile(r'(\[.*?\])')
GbgPatt = re.compile(r'(.*?)\)[^\)]+') # for float('inf') cmplx.
GbgPatt2 = re.compile(r'(.*?)\).*') # general gbg, ? for non greedy.
LpRegex = re.compile(r'\({1,}\s{0,}')
RpRegex = re.compile(r'\s{0,}\){1,}')
PrRegex = re.compile(r'\((.*)(\))(?!.*\))') # from \( to last \).
CmRegex = re.compile(r'\s{0,},\s{0,}')
StrRegex = re.compile(r'\'(.*?)\'')

# Argument dict : {arg_name : value}
argDct=OrderedDict()

# process 'default=' value.
def default_value(tval, dtype=''):
  # string pattern.
  regres = StrRegex.match(tval) 
  if regres and not re.search('int|float|long|bool|complex', dtype):
    if DBG:
      print('default_value: str patt found')
    tval = regres.group(0)
    return tval

  # typed pattern.
  CommaSeparated = CmRegex.split(tval)[0]
  if DBG:
    print('comma sepearated value:', CommaSeparated)
  
  if ListStartPatt.match(CommaSeparated) and not ListStartPatt2.match(CommaSeparated):
    lres = ListPatt.search(tval)
    if lres:
      tval = lres.group(1)
    if DBG:
      print('list patt exist tval: ', tval)
  else :
    tval = CmRegex.split(tval)[0]
    if DBG:
      print('no list format tval: ', tval)

  # if default value is not like - int('inf') , remove characters after ')' garbage chars.
  ires = RpRegex.split(tval)[0]
  if not (re.search('int|float|long|bool|complex', ires) and re.search(r'[a-z]+\(',ires)):
    if DBG:
      print('not int("inf") format. Rp removed tval : ', tval)
    tval = re.split(r'\s{0,}\){1,}',tval)[0]
    gbg = GbgPatt2.search(tval)
    if gbg:
      tval = gbg.group(1)  
      if DBG:
        print('garbage exist & removed. tval : ', tval)

  # int('inf') patt.
  else:
    if DBG:
      print('type("inf") value garbaging!')
    gbg = GbgPatt.search(tval)
    if gbg:
      if DBG:
        print('garbage found, extract!')
      tval = gbg.group(1)

  return tval

# Handling add_argument()
def add_argument(arg_line):
  global argDct
  if DBG:
    print('\nin add_argument : **Pre regex: ', arg_line)

  '''    
  argument name
  '''
  # argname = DdRegex.split(arg_line)[1] # Dash or regex for arg name.
  argname = re.search('\'--(.*?)\'', arg_line)
  if not argname:
    argname = re.search('\'-+(.*?)\'', arg_line)
  
  # dest= keyword handling.
  dest = re.search(r',\s*dest\s*=(.*)', arg_line)
  if dest:
    dval = dest.group(1)
    dval = default_value(dval)
    argname = StrRegex.search(dval)

  # hyphen(-) to underscore(_)
  if argname:
    argname = argname.group(1).replace('-', '_')
  else :
    # naive str argname.
    sres = StrRegex.match(arg_line)
    if sres:
      argname = sres.group(1)
    if not argname:
      return # no argument name 
  
  '''
  check for syntaxes (type=, default=, required=, action=, help=, choices=)
  '''
  dtype = ''
  dres = re.search(r',\s*type\s*=\s*(.*)', arg_line)
  if dres:
    dtype = dres.group(1)
    dtype = CmRegex.split(dtype)[0]

  dfult = re.search(r',\s*default\s*=\s*(.*)', arg_line)
  rquird = re.search(r',\s*required\s*=\s*(.*)', arg_line)
  action = re.search(r',\s*action\s*=\s*(.*)', arg_line)
  hlp = re.search(r',\s*help\s*=\s*(.*)', arg_line)
  chice = re.search(r',\s*choices\s*=\s*(.*)', arg_line)

  # help message
  hlp_msg = ''
  if hlp:
    thl = hlp.group(1)
    if DBG:
      print('handling help=')
    hlp_msg = default_value(thl)
    if hlp_msg:
      hlp_msg = 'help='+hlp_msg

  # choice message
  choice_msg = ''
  if chice:
    tch = chice.group(1)
    if DBG:
      print('handling choices=')
    choice_msg = default_value(tch)
    if choice_msg:
      choice_msg = 'choices='+choice_msg+' '

  '''
  argument value
  '''
  # tval: argument value.
  tval = ''
  # default exist.
  if dfult:
    tval = dfult.group(1)
    tval = default_value(tval, dtype)
    if DBG:
      print('value determined : ', tval)

  # action or required syntaxes exist.
  elif action or rquird:
    if DBG:
      print('in action/required handling')
    msg_str = ''
    if action:
      tval = action.group(1)
      msg_str = 'action'
    elif rquird:
      tval = rquird.group(1)
      msg_str = 'required'

    tval = default_value(tval)
    tval = ' ** ' + msg_str + ' '+tval+'; '+choice_msg+ hlp_msg

  # no default, action, required.
  else : 
    argDct[argname] = ' ** default not found; '+choice_msg+ hlp_msg

  # value found.
  if tval:
    argDct[argname] = tval

# Handling set_defaults()
def set_defaults(arg_line):
  global argDct
  if DBG:
    print('\nin set_defaults arg_line: ', arg_line)

  # arguments to process.
  tv='' 
  # arguments of set_default()
  SetPatt = re.compile(r'(.+=.+\)?)')
  sres = SetPatt.match(arg_line)
  if sres:
    tv = sres.group(1)
    if DBG:
      print("setPatt res: ", tv)
    tv = re.sub(r'\s+','', tv)
    if DBG:
      print('\nset_default values: ', tv)

  # one arguemnt regex.
  SetArgPatt = re.compile(r',?([^=]+=)[^=,]+,?')
  # handling multiple set_default() arguments. (may have a bug)
  while True:
    tname=''
    tval =''
    tnv=''
    # func closed.
    if re.match(r',*\).*',tv):
      tv=''
      break
    if DBG:
      print('set_default remaining: ', tv)

    nres = SetArgPatt.match(tv)
    if nres:
      tname = nres.group(1)
      if len(tv.split(tname, 1)) > 1:
        tval = tv.split(tname,1)[1]
        tval = default_value(tval)
        tnv=tname+tval
        tname = tname.rsplit('=',1)[0]
      
      if DBG:
        print('set_default tnam: ', tname)
        print('set_default tval: ', tval)
      if tname:
        argDct[tname] = tval

      # split with processed argument.
      tv = tv.split(tnv)
      if len(tv) > 1:
        tv = tv[1]
      # no more value to process
      else:
        break

    # no arg=value pattern found.
    else:
      break

# Remove empty line & Concatenate line-separated syntax.
def preprocess(fname):
  try :
    with open(fname, 'r', encoding='UTF8') as f:
      txt = f.read()
      t = txt.splitlines(True)
      t = list( filter(None, t) )

      # remove empty line
      t = [x for x in t if not re.match(r'\s{0,}\n',x)]
      # concatenate multiple lined arguments.
      # empl : lines to be deleted from t[].
      empl = []
      for i in range(len(t)-1, 0, -1):
        if not re.search('add_argument|set_defaults', t[i]):
          t[i-1] += t[i]
          t[i-1]=re.sub(r'\n{0,}','',t[i-1])
          t[i-1]=re.sub(r'\s{1,}',' ',t[i-1])
          empl.append(t[i])

      for d in empl:
        t.remove(d)
      for i, line in enumerate(t):
        t[i] = line.replace('\"', '\'').split('parse_args()')[0]
      return t

  except IOError:
    print('IOError : no such file.', fname)
    sys.exit()

def transform(fname):
  # t : list() contains add_argument|set_defaults lines.
  arg_line_list = preprocess(fname)

  for i, arg_line in enumerate(arg_line_list):
    t = PrRegex.search(arg_line)

    if t:
      t = t.group(1) # t: content of add_argument Parentheses.
    else :
      continue # nothing to parse.

    if re.search(r'add_argument\s*\(', arg_line):
      add_argument(t)
    elif re.search(r'set_defaults\s*\(',arg_line):
      set_defaults(t)
    else :
      # Nothing to parse.
      continue

  print('\nclass Args:')
  for i in argDct:
    print(' ',i, '=', argDct[i])
  print()
  print('args=Args()')

def main():
  if len(sys.argv) <2:
    print('Usage : python arg2cls.py [target.py] [target2.py(optional)] ...')
    sys.exit(0)
  sys.argv.pop(0)

  #handling multiple file input.
  for fname in sys.argv:
    transform(fname)

if(__name__ == "__main__"):
  main()
