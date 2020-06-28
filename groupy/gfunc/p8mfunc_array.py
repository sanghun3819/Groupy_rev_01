
import groupy.garray.p8m_array as p8ma
from groupy.gfunc.gfuncarray import GFuncArray


class P8MFuncArray(GFuncArray):

    def __init__(self, v, umin=None, umax=None, vmin=None, vmax=None):

        if umin is None or umax is None or vmin is None or vmax is None:
            if not (umin is None and umax is None and vmin is None and vmax is None):
                raise ValueError('Either all or none of umin, umax, vmin, vmax must equal None')

            # If (u, v) ranges are not given, determine them from the shape of v,
            # assuming the grid is centered.
            nu, nv = v.shape[-2:] # 3 3
            hnu = nu // 2 # 1
            hnv = nv // 2 # 1

            umin = -hnu
            umax = hnu
            vmin = -hnv
            vmax = hnv

        self.umin = umin
        self.umax = umax
        self.vmin = vmin
        self.vmax = vmax

        i2g = p8ma.meshgrid(
            m=p8ma.m_range(),
            #r=p4ma.r_range(0, 2, step=0.5),
            r=p8ma.r_range(0, 8),
            u=p8ma.u_range(self.umin, self.umax + 1),
            v=p8ma.v_range(self.vmin, self.vmax + 1)
        )
        #print('p8m',i2g.shape)

        if v.shape[-3] == 8:
            i2g = i2g.reshape(8, i2g.shape[-2], i2g.shape[-1])
            self.flat_stabilizer = True
        else:
            self.flat_stabilizer = False

        super(P8MFuncArray, self).__init__(v=v, i2g=i2g)

    def g2i(self, g):
        # TODO: check validity of indices and wrap / clamp if necessary
        # (or do this in a separate function, so that this function can be more easily tested?)

        gint = g.reparameterize('int').data.copy()
        gint[..., 2] -= self.umin
        gint[..., 3] -= self.vmin

        if self.flat_stabilizer:
            gint[..., 1] += gint[..., 0] * 4
            gint = gint[..., 1:]

        return gint
