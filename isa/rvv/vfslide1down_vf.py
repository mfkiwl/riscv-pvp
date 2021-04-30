from isa.inst import *
import numpy as np

class Vfslide1down_vf(Inst):
    name = 'vfslide1down.vf'

    def golden(self):

        vd = self['vs2'].tolist()
        vd =vd[1:]
        vd.append( self['rs1'].astype( self['vs2'].dtype ) )
        vd = np.array(vd, dtype=self['vs2'].dtype )


        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd