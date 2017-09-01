import sys

if len(sys.argv) <2:
    print('Usage : python arg2cls.py [target.py] [target2.py(optional)] ...')
    sys.exit(0)

sys.argv.pop(0)
for fname in sys.argv:
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
                dfult = t.split('default=')
                if len(dfult) <2:
                    val.append('###manual_setting_required###')
                else:
                    val.append(dfult[1].split(',')[0].replace('-','_'))

            print('')
            print('class args:')
            for i in zip(name,val):
                print('    ',end='')
                print(i[0],'=',i[1].replace('\"',''))
            print('')

    except IOError:
        print('IOError : Maybe no such file.', fname)
