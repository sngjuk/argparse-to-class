#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
import sys
import re

#add_argument, set_defaults only available.
ArgPatt = re.compile('add_argument|set_defaults')
add_argument_Patt = re.compile('add_argument')
set_defaults_Patt = re.compile('set_defaults')
EqualPatt = re.compile('\s{0,}=\s{0,}')
WsPatt = re.compile('\s{0,}\n')
# handling multiple white spaces.
LpRegex = re.compile('\({1,}\s{0,}')
RpRegex = re.compile('\s{0,}\){1,}')
LcRegex = re.compile('\'\s{0,}')
RcRegex = re.compile('\s{0,}\'')
DdRegex = re.compile('\s{0,}--*')
CmRegex = re.compile('\s{0,},\s{0,}')
NlRegexStr = '\s{0,}\n{0,}\s{0,}'

def transform():
  if len(sys.argv) <2:
    print('Usage : python arg2cls.py [target.py] [target2.py(optional)] ...')
    sys.exit(0)

  sys.argv.pop(0)
  for fname in sys.argv:
    if(__name__!="__main__"):
            print(fname)
    try :
      with open(fname, 'r') as f:
        
        txt = f.read()
        t = txt.splitlines(True)
        t = str_list = list( filter(None, t) )
        # filter empty line
        t = [x for x in t if not WsPatt.match(x)]

        # handling multiple lined arguments.
        empl = []
        for i, z in reversed(list(enumerate(t))):
          if i>0 and not ArgPatt.search(t[i]):
            t[i-1] += t[i]
            t[i-1]=re.sub(NlRegexStr,'',t[i-1])
            empl.append(t[i])
        for d in empl:
          t.remove(d)

        argDct=OrderedDict()
        for i, x in enumerate(t):
          if not ArgPatt.search(x):
            continue

          #add_argument()
          if add_argument_Patt.search(x) :
            t = LpRegex.split(x)[1]
            tname = RcRegex.split( LcRegex.split(t)[1] )[0]
            if DdRegex.search(tname):
              tname = tname.replace('--','')
            aname = tname.replace('-','_')
            argDct[aname]=''
            dtype = ''
            if('type' in t):
              dtype = EqualPatt.split(t.split('type')[1])[1]
              dtype = CmRegex.split(dtype)[0]

            dfult = t.split('default')
            if len(dfult) > 1 :
              if (dtype in ['int','float','long']):
                tval = re.split(EqualPatt, dfult[1])[1]  
                tval = RpRegex.split(tval)[0]
                if LcRegex.search(tval):
                  tval = LcRegex.split(tval)[1]
                tval = CmRegex.split(tval)[0]
                if RcRegex.search(tval):
                  tval = RcRegex.split(tval)[0]
                argDct[aname] = tval
            
              else:
                tval = re.split(EqualPatt, dfult[1])[1]
                tval = RpRegex.split(tval)[0]
                tval = CmRegex.split(tval)[0]
                argDct[aname] = tval
            
            elif len(argDct[aname]) == 0 :
                argDct[aname] = '## Default None ##'

          #set_defaults()
          elif set_defaults_Patt.search(x) :
            dfult = re.split(EqualPatt, x)
            tn = LpRegex.split(dfult[0])[1]
            tv = RpRegex.split(dfult[1])[0]
            argDct[tn]=tv
          #future functions.
          else :
            pass

        print('')
        print('class args:')
        for i in argDct:
            print('  ',end='')
            print(i, '=', argDct[i])

    except IOError:
        print('IOError : Maybe no such file.', fname)
          
if(__name__ == "__main__"):
    transform()
