from isa.inst import *
import numpy as np
import math

class Vssegxex_v(Inst):
    name = 'vssegxex.v'

    def golden(self):

        vd = self['vs3'].copy()

        if 'mask' in self:
            mask = []
            for no in range(0, int(self['vs3'].size/self['nfields'])):
                mask = ( self['mask'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int(self['nfields']*no+idx) ] = 0
            return vd
        else:
            return vd
