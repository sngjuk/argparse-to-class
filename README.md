# Argparse2class for Jupyter execution.

Argparse transformation for Jupyter execution. (for quick testing in .ipynb)<br />
Copy & paste class-transformed argument class to replace parser <br/>

If you find some buggy outputs please mail me : <u> sngjuk@gmail.com </u>
### update : 5/Aug/18 
05/Aug/18 : action syntax, bool type, ('inf') syntax fixed.  <br>
31/Mar/18 : set_defaults & long arguments error fix. 

### Online quick transformation :
http://35.192.144.192:8000/arg2cls.html

### Usage : 
```
python arg2cls.py [target.py] [target2.py(optional)] ...
```

### Make argument parser into..
```
parser = argparse.ArgumentParser(description='PyTorch PennTreeBank RNN/LSTM Language Model')
parser.add_argument('--data', type=str, default='./data/penn',
                    help='location of the data corpus')
parser.add_argument('--model', type=str, default='LSTM',
                    help='type of recurrent net (RNN_TANH, RNN_RELU, LSTM, GRU)')
parser.add_argument('--emsize', type=int, default=200,
                    help='size of word embeddings')
parser.add_argument('--nhid', type=int, default=200,
                    help='number of hidden units per layer')
args = parser.parse_args()
```
### Class format!
```
class args:
    data = './data/penn'
    model = 'LSTM'
    emsize = 200
    nhid = 200
```

### Input (Source with argument parser) :

![alt text](http://pds27.egloos.com/pds/201709/01/00/c0134200_59a941fb9501e.png)


### Ouput (args class) :

![alt text](http://thumbnail.egloos.net/600x0/http://pds25.egloos.com/pds/201709/01/00/c0134200_59a936974c78f.png)


### Transformed usage : 
If there's no default value for argument, It will have warning value. (###manual_setting_required###)

![alt text](http://pds21.egloos.com/pds/201709/01/00/c0134200_59a937f65f737.png)
