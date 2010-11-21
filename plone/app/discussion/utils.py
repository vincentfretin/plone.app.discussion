def safe_decode(x):
    if type(x) == unicode:
        return x
    else:
        return x.decode('utf-8')
    
