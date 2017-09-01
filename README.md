# Argparse_to_class for Jupyter execution

Simple argparse transform into class format for Jupyter notebook users. (due to Jupyter argv argument passing problem)
You can just copy and paste to substitue your argparse codes.

###Usage : 
python arg2cls.py [target.py] [target2.py(optional)] ...

###Example Input file :

![alt text](http://thumbnail.egloos.net/600x0/http://pds21.egloos.com/pds/201709/01/00/c0134200_59a9363cd1dfc.png)


###Example Ouput :

![alt text](http://thumbnail.egloos.net/600x0/http://pds25.egloos.com/pds/201709/01/00/c0134200_59a936974c78f.png)


###substituted code : If there's no default value for argument, It will have warning value. (###manual_setting_required###)

![alt text](http://pds21.egloos.com/pds/201709/01/00/c0134200_59a937f65f737.png)



### Make argument parser into

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

### class format

class args:
    data = './data/penn'
    model = 'LSTM'
    emsize = 200
    nhid = 200
    

