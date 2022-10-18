'''
commons.py
'''
import json
import random



with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())
    f.close()



# TODO DSE questa nuova struttura va utilizzata e non creare pin a caso
_pin_list = []



def init_pin_list(exclude_pin_list):
    '''
    init_pin_list(exclude_pin_list)
    '''
    pin_min = int(f"1{'0' * (config['server']['pin_length'] - 1)}")
    pin_max = int('9' * config['server']['pin_length'])
    for i in range(pin_min, pin_max + 1):
        if str(i) not in exclude_pin_list:
            _pin_list.append(str(i))

def put_pin(pin):
    '''
    put_pin(pin)
    '''
    _pin_list.append(pin)

def get_pin():
    '''
    get_pin()
    '''
    return _pin_list.pop(random.randint(0, len(_pin_list)))
