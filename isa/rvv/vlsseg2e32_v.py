from isa.inst import *
import numpy as np
import math

class Vlsseg2e32_v(Inst):
    name = 'vlsseg2e32.v'

    def golden(self):

        vl = self['rs1'].size/(self['rs2']/self['rs1'].itemsize)
        vd_size = vl * self['nfields']
        vd = np.zeros( int(vd_size), dtype=self['rs1'].dtype )
        for no in range(0, int(vl)):
            for idx in range(0, self['nfields']):
                vd[ int(self['nfields']*no+idx) ] = self['rs1'][int((self['rs2']/self['rs1'].itemsize)*no+idx)]

        if 'v0' in self:
            mask = []
            for no in range(0,int(vl)):
                mask = ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int(self['nfields']*no+idx) ] = self['orig'][int(self['nfields']*no+idx)]
            return vd
        else:
            return vd
