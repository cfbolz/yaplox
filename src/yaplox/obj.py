class W_Root(object):
    def str(self):
        return str(self)

class W_Bool(W_Root):
    pass

class W_True(W_Bool):
    def str(self): return "true"

w_true = W_True()

class W_False(W_Bool):
    def str(self): return "false"

w_false = W_False()

def newbool(b):
    if b:
        return w_true
    return w_false

class W_Nil(W_Root):
    def str(self): return "nil"

w_nil = W_Nil()

class W_Number(W_Root):
    def __init__(self, num):
        self.num = num

    def str(self):
        return str(self.num)

class W_String(W_Root):
    def __init__(self, val):
        self.val = val

    def str(self):
        return self.val
