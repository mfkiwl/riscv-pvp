from isa.inst import *
import numpy as np

class Vfmacc_vv(Inst):
    name = 'vfmacc.vv'

    def golden(self):
        if 'v0' in self:
            mask = []
            for no in range(0, self['rs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)          
            return np.where( mask == 1, self['rs1'] * self['rs2'] + self['rds'], self['rds'])
        else:
            return self['rs1'] * self['rs2'] + self['rds']