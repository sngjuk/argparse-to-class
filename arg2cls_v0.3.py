#!/usr/bin/env python
from __future__ import print_function
from collections import OrderedDict
import sys
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
                t = txt.split('argparse.ArgumentParser')
                if len(t) <2:
                    print('Nothing to make from file.')
                    sys.exit(0)
                t = t[1].split('.parse_args')[0].split('add_argument')
                t.pop(0)
                argDct=OrderedDict()
                for i, x in enumerate(t):
                    t =x.split('--')[1]
                    aname =t.split('\'')[0].replace('-','_')
                   
                    argDct[aname]=''
                    dtype = ''
                    if('type' in t):
                        dtype = t.split('type=')[1].split(',')[0]
                    dfult = t.split('default=')
                    if len(dfult) <2:
                        dfult=dfult[0].split('set_defaults(')

                        if(len(dfult)>1):
                          dfult=dfult[1]                          
                          tn = dfult.split('=')[0]
                          tv = dfult.split('=')[1].split(')')[0]
                          argDct[tn]=tv

                        else :
                          argDct[aname]='###manual_setting_required###'
                    elif (dtype in ['int','float','long']):
                        argDct[aname]=dfult[1].split(',')[0].replace('\'','')
                    else:
                        argDct[aname]=dfult[1].split(',')[0]

                print('')
                print('class args:')
                for i in argDct:
                    print('  ',end='')
                    print(i,'=',argDct[i].replace('\"',''))
                print('')

        except IOError:
            print('IOError : Maybe no such file.', fname)
            
if(__name__ == "__main__"):
    transform()
