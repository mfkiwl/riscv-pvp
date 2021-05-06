from isa.inst import *
import numpy as np
import math

class Vfcvt_rtz_xu_f_v(Inst):
    name = 'vfcvt.rtz.xu.f.v'

    def golden(self):

        vd = np.where( self['vs2'] < 0, 0, self['vs2'] )

        if self['vs2'].dtype == np.float16:
            target_dtype = np.uint16
            vd = np.where( vd > 65535, 65535, vd )
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.uint32
            vd = np.where( vd > 4294967295, 4294967295, vd )
        elif self['vs2'].dtype == np.float64:
            target_dtype = np.uint64
            vd = np.where( vd > 18446744073709551615, 18446744073709551615, vd )

        vd = np.trunc( vd )
        vd = vd.astype( target_dtype )
        

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd