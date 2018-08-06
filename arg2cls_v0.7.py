#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
import sys
import re

#add_argument, set_defaults only available.
ArgPatt = re.compile('add_argument|set_defaults')
add_argument_Patt = re.compile('add_argument')
set_defaults_Patt = re.compile('set_defaults')
type_Patt = re.compile('int|float|complex|bool|str')
EqualPatt = re.compile('\s{0,}=\s{0,}')
WsPatt = re.compile('\s{0,}\n')

# handling multiple white spaces.
LpRegex = re.compile('\({1,}\s{0,}')
RpRegex = re.compile('\s{0,}\){1,}')
PrRegex = re.compile('\((.*)(\))(?!.*\))') # from \( to last \)
LcRegex = re.compile('\'\s{0,}')
RcRegex = re.compile('\s{0,}\'')
DdRegex = re.compile('\s{0,}--')
CmRegex = re.compile('\s{0,},\s{0,}')
NlRegexStr = '\s{0,}\n{0,}\s{0,}'
StrRegex = re.compile('(\')(.*)(\')')
StrRegexn = re.compile('(?<=\')(.*)(?=\')')
GbgRegex = re.compile('\)[A-z0-9]')

# Argument dict : store {arg_name : value}
argDct=OrderedDict()

# Remove empty line & Concatenate the line separated argparse syntax.
def preprocess(fname):
  try :
    with open(fname, 'r') as f:
      txt = f.read()
      t = txt.splitlines(True)
      t = str_list = list( filter(None, t) )
      # remove empty line
      t = [x for x in t if not WsPatt.match(x)]
      # concatenate multiple lined arguments.
      empl = []
      for i, z in reversed(list(enumerate(t))):
        if i>0 and not ArgPatt.search(t[i]):
          t[i-1] += t[i]
          t[i-1]=re.sub(NlRegexStr,'',t[i-1])
          empl.append(t[i])

      for d in empl:
        t.remove(d)
      for i, line in enumerate(t):
        t[i] = line.replace('\"', '\'')
      return t

  except IOError:
      print('IOError : Maybe no such file.', fname)

# Handling add_argument()
def add_argument(arg_line):
  global argDct

  t = PrRegex.split(arg_line)[1]
  print('Pr regex : ' + str(t))

  argname = DdRegex.split(arg_line)[1] # Double dash regex.
  argname = LcRegex.split(argname)[0]
  argname = argname.replace('-', '_')

  if not argname: # double dash exist.
    return # no argument name.

  argDct[argname]=''
  dtype = ''
  if('type' in t):
    dtype = EqualPatt.split(t.split('type')[1])[1]
    dtype = CmRegex.split(dtype)[0]

  # set default value regarding with 'dtype' syntax.
  dfult = t.split('default')
  rquird = t.split('required')
  action = t.split('action')

  tval = ''
  # default exist
  if len(dfult) > 1 :
    # type exist
    if (dtype in ['int','float','long','bool','complex']):
      tval = re.split(EqualPatt, dfult[1])[1]
      tval = CmRegex.split(tval)[0]

      if type_Patt.search(tval):
        pass
      else :
        if LcRegex.search(tval):
          tval = LcRegex.split(tval)[1]
        tval = CmRegex.split(tval)[0]
        if RcRegex.search(tval):
          tval = RcRegex.split(tval)[0]

      if GbgRegex.search(tval):
        tval = GbgRegex.split(tval)[0]
    
    # type not specified (str)
    else:
      tval = re.split(EqualPatt, dfult[1])[1]
      tval = StrRegex.search(tval).group(0)

  # action exist
  elif len(action) > 1 :
    tval = EqualPatt.split(action[1])[1]
    tval = StrRegexn.search(tval).group(0)
    tval = '## action : ' + tval + ' ##'

  # required exist
  elif len(rquird) > 1 :
    tval = EqualPatt.split(rquird[1])[1]
    tval = CmRegex.split(tval)[0]
    tval = RpRegex.split(tval)[0]
    tval = '## required : ' + tval + ' ##'

  else :
    argDct[argname] = '## Default None ##'

  if tval:
    argDct[argname] = tval

# Handling set_default()
def set_defaults(arg_line):
  global argDct

  dfult = re.split(EqualPatt, arg_line)
  tn = LpRegex.split(dfult[0])[1] # arg name
  tv = RpRegex.split(dfult[1])[0] # arg value
  argDct[tn]=tv

def transform(fname):
  # t : list() contains add_argument|set_defaults lines.
  arg_line_list = preprocess(fname)

  for i, arg_line in enumerate(arg_line_list):

    # skip none argparse syntax.
    if not ArgPatt.search(arg_line):
      continue
    if add_argument_Patt.search(arg_line) :
      add_argument(arg_line)
    elif set_defaults_Patt.search(arg_line) :
      set_defaults(arg_line)
    #future functions.
    else :
      pass

  print('\nclass args:')
  for i in argDct:
    print(' ',i, '=', argDct[i])

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
