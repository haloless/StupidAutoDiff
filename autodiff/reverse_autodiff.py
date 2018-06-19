

class ADBuf(object):
    """auto-diff variable
    """

    def __init__(self, val=0.0, adj=0.0):
        self.val = val
        self.adj = adj

    pass


class ADVar(object):
    """variable
    """

    def __init__(self, data, func=None):
        if not isinstance(data, ADBuf):
            data = ADBuf(data)
        self.data = data
        self.func = func

    @property
    def val(self):
        return self.data.val

    @val.setter
    def val(self, val):
        self.data.val = val

    @property
    def adj(self):
        return self.data.adj

    @adj.setter
    def adj(self, adj):
        self.data.adj = adj

    def propagate(self):
        """derivative propagate"""

        d = self.data.left
        d.b.adj = 1.0

        while d is not None:
            #
            d.c.adj += d.a * d.b.adj
            # print d.c.adj
            # next propagation
            d = d.next

        return

    # end ADVar


class DerProp(object):
    """c.adj += a * b.adj"""

    top = None

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.next = DerProp.top
        DerProp.top = self

    def __repr__(self):
        ret = super(DerProp,self).__repr__()
        ret = '%s: a=%f,b.adj=%f,c.adj=%f' % (ret, self.a, self.b.adj, self.c.adj)
        return ret

    pass


class ADFun(object):
    pass


class ADOpBinary(ADBuf):
    def __init__(self, val, lvar, lcoef, rvar, rcoef):
        # super
        super(ADOpBinary, self).__init__(val)

        self.right = DerProp(rcoef, self, rvar)
        self.left = DerProp(lcoef, self, lvar)

    pass


################################################################################


def var_add(lhs, rhs):
    """var + var"""
    lval = lhs.val
    rval = rhs.val
    op = ADOpBinary(lval+rval, lhs,1.0, rhs,1.0)
    #
    ret = ADVar(op)
    return ret


def var_sub(lhs, rhs):
    """var - var"""
    lval = lhs.val
    rval = rhs.val
    op = ADOpBinary(lval-rval, lhs, 1.0, rhs, -1.0)
    #
    ret = ADVar(op)
    return ret


def var_mul(lhs, rhs):
    """var * var"""
    lval = lhs.val
    rval = rhs.val
    op = ADOpBinary(lval*rval, lhs,rval, rhs,lval)
    #
    ret = ADVar(op)
    return ret


# bind operator
ADVar.__add__ = var_add
ADVar.__sub__ = var_sub
ADVar.__mul__ = var_mul

################################################################################


def calc_grad(purge=True):
    """calculate gradient"""

    #
    d = DerProp.top
    d.b.adj = 1.0

    while d is not None:
        #
        d.c.adj += d.a * d.b.adj

        # next propagation
        d = d.next

    #
    if purge:
        DerProp.top = None

    return




