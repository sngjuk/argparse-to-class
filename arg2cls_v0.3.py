#!/usr/bin/env python

from __future__ import print_function
import sys

def transform():
    if len(sys.argv) <2:
        print('Usage : python arg2cls.py target.py target2.py(optional) ...')
        sys.exit(0)

    sys.argv.pop(0)
    for fname in sys.argv:
        if(__name__!='__main__'):
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

                name=[]
                val=[]
                for i, x in enumerate(t):
                    t =x.split('--')[1]
                    name.append(t.split('\'')[0].replace('-','_'))
                    dtype = ''
                    if('type' in t):
                        dtype = t.split('type=')[1].split(',')[0]

                    dfult = t.split('default=')
                    if len(dfult) <2:
                        val.append('###manual_setting_required###')
                    elif (dtype in ['int','float','long']):
                        val.append(dfult[1].split(',')[0].replace('\'',''))
                    else:
                        val.append(dfult[1].split(',')[0])

                print('')
                print('class args:')
                for i in zip(name,val):
                    print('    ',end='')
                    print(i[0],'=',i[1].replace('\"',''))
                print('')

        except IOError:
            print('IOError : Maybe no such file.', fname)
            
if(__name__ == "__main__"):
    transform()
