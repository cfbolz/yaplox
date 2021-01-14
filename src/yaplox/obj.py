class W_Root(object):
    pass

class W_Bool(W_Root):
    pass

class W_True(W_Bool):
    pass

w_true = W_True()

class W_False(W_Bool):
    pass

w_false = W_False()

def newbool(b):
    if b:
        return w_true
    return w_false

class W_Nil(W_Root):
    pass

w_nil = W_Nil()

class W_Number(W_Root):
    def __init__(self, num):
        self.num = num

class W_String(W_Root):
    def __init__(self, val):
        self.val = val

