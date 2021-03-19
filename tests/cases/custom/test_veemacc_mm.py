import pytest
from tests.cases.case import *
from tests.cases.params import *
from isa.simulate import *
from isa.custom.veemacc_mm import *

class BaseCase_veemacc_mm(BaseCase):
    head = '#include "veemacc.h"'
    env = 'RVTEST_RV32STC'

class Case_shape(BaseCase_veemacc_mm):
    def template( self, num, name, rd, rs1, rs2, dim, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if dim == 0:
            return f'VEEMACC_DIM_H( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, 0, 0, 0 )'
        else:
            return f'VEEMACC_DIM_W( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, 0, 0, 0 )'

class Case_stride(BaseCase_veemacc_mm):
    def template( self, num, name, rd, rs1, rs2, stride_s1, stride_s2, dim, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if dim == 0:
            return f'VEEMACC_DIM_H( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_s1}, {stride_s2}, 0 )'
        else:
            return f'VEEMACC_DIM_W( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {rs1_shape[0]}, {rs1_shape[1]}, {stride_s1}, {stride_s2}, 0 )'

class Case_rs_rd_overlapping(BaseCase_veemacc_mm):
    def template( self, num, name, rd, rs1, rs2, overlap_addr, dim, rs1_data, rs1_shape, rs2_data, rs2_shape ):
        if dim == 0:
            return f'VEEMACC_DIM_H_RS_RD_OVERLAPPING( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {overlap_addr} )'
        else:
            return f'VEEMACC_DIM_W_RS_RD_OVERLAPPING( {num}, {name}, {rd}, {rs1_data}, {rs2_data}, {rs1_shape[0]}, {rs1_shape[1]}, {overlap_addr} )'

class Case_misaligned_base_addr(BaseCase_veemacc_mm):
    def template( self, num, name, rd, dim, height, width, off_s1, off_s2, off_d ):
        return f'VEEMACC_MISALIGNED_BASE_ADDR( {num}, {name}, {dim}, {height}, {width}, {off_s1}, {off_s2}, {off_d} )'

class Case_misaligned_stride(BaseCase_veemacc_mm):
    def template( self, num, name, rd, dim, height, width, stride_s1, stride_s2 ):
        return f'VEEMACC_MISALIGNED_STRIDE( {num}, {name}, {dim}, {height}, {width}, {stride_s1}, {stride_s2}, 0 )'

class Case_invalid_param(BaseCase_veemacc_mm):
    def template( self, num, name, rd, dim, height, width ):
        return f'TEST_VEEMACC_INVALID_PARAM( {num}, {name}, {dim}, {height}, {width} )'

class Case_access_fault(BaseCase_veemacc_mm):
    def template( self, num, name, rd, result, val1, val2, dim, height, width ):
        return f'TEST_VEEMACC_ACCESS_FAULT( {num}, {name}, {result}, {val1}, {val2}, {dim}, {height}, {width} )'

class BaseTest_veemacc_mm(BaseTest):

    @pytest.mark.parametrize( 'rs1, rs2, dim', [
        #************************************************
        # Test shapes
        #************************************************/
        #dim_h

        #small shapes, m(odd, odd)
        ramdom_veemacc_mm( 1, 1, 0 ),
        ramdom_veemacc_mm( 1, 3, 0 ),
        ramdom_veemacc_mm( 3, 1, 0 ),
        ramdom_veemacc_mm( 3, 3, 0 ),

        #m(even, even)
        ramdom_veemacc_mm( 2, 10, 0 ),
        ramdom_veemacc_mm( 10, 2, 0 ),
        ramdom_veemacc_mm( 2, 2, 0 ),
        ramdom_veemacc_mm( 10, 10, 0 ),

        #m(odd, even), m(even ,odd)
        ramdom_veemacc_mm( 19, 28, 0 ),
        ramdom_veemacc_mm( 28, 19, 0 ),

        #64 MAC Engine boundary
        ramdom_veemacc_mm( 31, 63, 0 ),
        ramdom_veemacc_mm( 32, 64, 0 ),
        ramdom_veemacc_mm( 33, 65, 0 ),

        #middle shapes
        ramdom_veemacc_mm( 35, 129, 0 ),
        ramdom_veemacc_mm( 36, 257, 0 ),
        ramdom_veemacc_mm( 131, 38, 0 ),
        ramdom_veemacc_mm( 258, 260, 0 ),

        #full of L1 buffer
        ramdom_veemacc_mm( 54613, 4, 0 ),
        ramdom_veemacc_mm( 256, 853, 0 ),
        ramdom_veemacc_mm( 853, 256, 0 ),

        # dim_w

        #small shapes, m(odd, odd)
        ramdom_veemacc_mm( 1, 1, 1 ),
        ramdom_veemacc_mm( 1, 3, 1 ),
        ramdom_veemacc_mm( 3, 1, 1 ),
        ramdom_veemacc_mm( 3, 3, 1 ),

        #m(even, even)
        ramdom_veemacc_mm( 2, 10, 1 ),
        ramdom_veemacc_mm( 10, 2, 1 ),
        ramdom_veemacc_mm( 2, 2, 1 ),
        ramdom_veemacc_mm( 10, 10, 1 ),

        #m(odd, even), m(even ,odd)
        ramdom_veemacc_mm( 19, 28, 1 ),
        ramdom_veemacc_mm( 28, 19, 1 ),

        #64 MAC Engine boundary
        ramdom_veemacc_mm( 31, 63, 1 ),
        ramdom_veemacc_mm( 32, 64, 1 ),
        ramdom_veemacc_mm( 33, 65, 1 ),

        #middle shapes
        ramdom_veemacc_mm( 35, 129, 1 ),
        ramdom_veemacc_mm( 36, 257, 1 ),
        ramdom_veemacc_mm( 131, 38, 1 ),
        ramdom_veemacc_mm( 258, 260, 1 ),

        #full of L1 buffer
        ramdom_veemacc_mm( 213, 1024, 1 ),
        ramdom_veemacc_mm( 256, 853, 1 ),
        ramdom_veemacc_mm( 853, 256, 1 ),

    ] )
    def test_shape( self, rs1, rs2, dim ):
        simulate( self, Case_shape, rs1=rs1, rs2=rs2, dim=dim )

    @pytest.mark.parametrize( 'rs1, rs2, stride_s1, stride_s2, dim', [
        #******************************************************
        #Test  stride,  stride >= ESIZE*width
        #******************************************************/
        ramdom_veemacc_mm_stride( 15, 15, 30, 30, 0 ),
        ramdom_veemacc_mm_stride( 15, 15, 30, 0, 0 ),
        ramdom_veemacc_mm_stride( 15, 15, 0, 30, 0 ),

        ramdom_veemacc_mm_stride( 15, 15, 0, 92, 0 ),
        ramdom_veemacc_mm_stride( 15, 15, 92, 0, 0 ),
        ramdom_veemacc_mm_stride( 15, 15, 92, 92, 0 ),
        ramdom_veemacc_mm_stride( 15, 15, 80, 68, 0 ),

        ramdom_veemacc_mm_stride( 15, 15, 30, 30, 1 ),
        ramdom_veemacc_mm_stride( 15, 15, 30, 0, 1 ),
        ramdom_veemacc_mm_stride( 15, 15, 0, 30, 1 ),

        ramdom_veemacc_mm_stride( 15, 15, 0, 92, 1 ),
        ramdom_veemacc_mm_stride( 15, 15, 92, 0, 1 ),
        ramdom_veemacc_mm_stride( 15, 15, 92, 92, 1 ),
        ramdom_veemacc_mm_stride( 15, 15, 80, 68, 1 ),

        ramdom_veemacc_mm_stride( 34, 34, 130, 0, 0 ),
        ramdom_veemacc_mm_stride( 34, 34, 0, 130, 0 ),
        ramdom_veemacc_mm_stride( 34, 34, 130, 130, 0 ),

        ramdom_veemacc_mm_stride( 34, 34, 150, 0, 0 ),
        ramdom_veemacc_mm_stride( 34, 34, 210, 0, 0 ),
        ramdom_veemacc_mm_stride( 34, 34, 262, 130, 0 ),
        ramdom_veemacc_mm_stride( 34, 34, 262, 512, 0 ),

        ramdom_veemacc_mm_stride( 34, 34, 130, 0, 1 ),
        ramdom_veemacc_mm_stride( 34, 34, 0, 130, 1 ),
        ramdom_veemacc_mm_stride( 34, 34, 130, 130, 1 ),

        ramdom_veemacc_mm_stride( 34, 34, 150, 0, 1 ),
        ramdom_veemacc_mm_stride( 34, 34, 210, 0, 1 ),
        ramdom_veemacc_mm_stride( 34, 34, 262, 130, 1 ),
        ramdom_veemacc_mm_stride( 34, 34, 262, 512, 1 ),

        #dim=dim_h, row=1, rs1 and rs2 all stride < width test
        ramdom_veemacc_mm_stride( 1, 15, 7, 7, 0 ),
        #dim=dim_w, row=1, rs1 and rs2 all stride < width test
        ramdom_veemacc_mm_stride( 1, 15, 7, 7, 1 ),
    ] )
    def test_stride( self, rs1, rs2, stride_s1, stride_s2, dim ):
        simulate( self, Case_stride, rs1=rs1, rs2=rs2, stride_s1=stride_s1, stride_s2=stride_s2, dim=dim )

    @pytest.mark.parametrize( 'rs1, rs2, overlap_addr, dim', [
        #******************************************************
        #Test rd and rs with same base address
        #******************************************************/
        #rd=rs1
        ramdom_veemacc_mm_overlap( 23, 24, 'VEADD_RS1_ADDR', 0 ),
        ramdom_veemacc_mm_overlap( 23, 24, 'VEADD_RS1_ADDR', 1 ),
    ] )
    def test_rs_rd_overlapping( self, rs1, rs2, overlap_addr, dim ):
        simulate( self, Case_rs_rd_overlapping, rs1=rs1, rs2=rs2, overlap_addr=overlap_addr, dim=dim )    

    @pytest.mark.parametrize( 'dim, height, width, off_s1, off_s2, off_d', [
        #******************************************************
        #Exception test with misaligned base addr
        #******************************************************/
        #dim_h, rd misaligned
        [ 0, 31, 32, 0, 0, 1 ],
        #rs2 misaligned
        [ 0, 31, 32, 0, 1, 0 ],
        #rd and rs2 misaligned
        [ 0, 31, 32, 0, 1, 1 ],
        #rs1 misaligned
        [ 0, 31, 32, 1, 0, 0 ],
        #rs1 and rd misaligned
        [ 0, 31, 32, 1, 0, 1 ],
        #rs1 and rs2 misaligned
        [ 0, 31, 32, 1, 1, 0 ],
        #rs1, rs2 and rd all misaligned
        [ 0, 31, 32, 1, 1, 1 ],

        #dim_w, rd misaligned
        [ 1, 31, 32, 0, 0, 1 ],
        #rs2 misaligned
        [ 1, 31, 32, 0, 1, 0 ],
        #rd and rs2 misaligned
        [ 1, 31, 32, 0, 1, 1 ],
        #rs1 misaligned
        [ 1, 31, 32, 1, 0, 0 ],
        #rs1 and rd misaligned
        [ 1, 31, 32, 1, 0, 1 ],
        #rs1 and rs2 misaligned
        [ 1, 31, 32, 1, 1, 0 ],
        #rs1, rs2 and rd all misaligned
        [ 1, 31, 32, 1, 1, 1 ],
    ] )
    def test_misaligned_base_addr( self, dim, height, width, off_s1, off_s2, off_d ):
        simulate( self, Case_misaligned_base_addr, dim=dim, height=height, width=width, off_s1=off_s1, off_s2=off_s2, off_d=off_d )

    @pytest.mark.parametrize( 'dim, height, width, stride_s1, stride_s2', [
        #******************************************************
        #Exception test with misaligned stride
        #******************************************************/
        # dim_h
        [ 0, 32, 32, 67, 0 ],
        [ 0, 32, 32, 0, 67 ],
        [ 0, 32, 32, 67, 67],

        #dim_w
        [ 1, 32, 32, 67, 0 ],
        [ 1, 32, 32, 0, 67 ],
        [ 1, 32, 32, 67, 67 ],

    ] )
    def test_misaligned_stride( self, dim, height, width, stride_s1, stride_s2 ):
        simulate( self, Case_misaligned_stride, dim=dim, height=height, width=width, stride_s1=stride_s1, stride_s2=stride_s2 )

    @pytest.mark.parametrize( 'dim, height, width', [
        #******************************************************
        #Exception test with invalid params
        #******************************************************/
        #dim_h,height=0
        [ 0, 0, 32],
        #width=0
        [ 0, 32, 0],
        #height=width=0
        [ 0, 0, 0],

        #dim_w,height=0
        [ 1, 0, 32],
        #width=0
        [ 1, 32, 0],
        #height=width=0
        [ 1, 0, 0],
    ] )
    def test_invalid_param( self, dim, height, width ):
        simulate( self, Case_invalid_param, dim=dim, height=height, width=width )

    @pytest.mark.parametrize( 'result, val1, val2, dim, height, width', [
        #******************************************************
        #Exception test with access fault
        #******************************************************/
        #dim_h
        #rd in ddr 1k
        [ 0x400, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 0, 24, 24 ],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 0xbffffffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 0, 32, 32 ],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 0xc013fffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 0, 12, 24 ],
        #rd span from reserved to IB，0xc0400000 - 4 = 0xc03ffffc
        [ 0xc03ffffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 0, 32, 32 ],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 0xc043fffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 0, 32, 32 ],

        #rs1 in ddr 1k
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 0x400, 'VEADD_RS2_ADDR', 0, 24, 24 ],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 'VEADD_RD_ADDR', 0xbffffffc, 'VEADD_RS2_ADDR', 0,  32, 32 ],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 'VEADD_RD_ADDR', 0xc013fffc, 'VEADD_RS2_ADDR', 0, 12, 24 ],
        #rd span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [ 'VEADD_RD_ADDR', 0xc03ffffc, 'VEADD_RS2_ADDR', 0, 32, 32 ],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 0xc043fffc, 'VEADD_RS2_ADDR', 0, 32, 32 ],


        #rs2 in ddr 1k
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0x400, 0, 24, 24 ],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xbffffffc, 0,  32, 32 ],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xc013fffc, 0, 12, 24 ],
        #rd span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xc03ffffc, 0, 32, 32 ],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xc043fffc, 0, 32, 32 ],

        #dim_w
        #rd in ddr 1k
        [ 0x400, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 1, 24, 24 ],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 0xbffffffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 1, 32, 32 ],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 0xc013fffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 1, 12, 24 ],
        #rd span from reserved to IB，0xc0400000 - 4 = 0xc03ffffc
        [ 0xc03ffffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 1, 32, 32 ],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 0xc043fffc, 'VEADD_RS1_ADDR', 'VEADD_RS2_ADDR', 1, 32, 32 ],

        #rs1 in ddr 1k
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 0x400, 'VEADD_RS2_ADDR', 1, 24, 24 ],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 'VEADD_RD_ADDR', 0xbffffffc, 'VEADD_RS2_ADDR', 1,  32, 32 ],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 'VEADD_RD_ADDR', 0xc013fffc, 'VEADD_RS2_ADDR', 1, 12, 24 ],
        #rd span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [ 'VEADD_RD_ADDR', 0xc03ffffc, 'VEADD_RS2_ADDR', 1, 32, 32 ],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 0xc043fffc, 'VEADD_RS2_ADDR', 1, 32, 32 ],

        #rs2 in ddr 1k
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0x400, 1, 24, 24 ],
        #rd span from ddr to L1, 0xc0000000 - 4 = 0xbffffffc, should height * width > 4
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xbffffffc, 1,  32, 32 ],
        #rd span from L1 to 0xc0140000 reserved addr ,0xc0140000 - 4 = 0xc013fffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xc013fffc, 1, 12, 24 ],
        #rd span from reserved to IB， 0xc0400000 - 4 = 0xc03ffffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xc03ffffc, 1, 32, 32 ],
        #rd span from IB to reserved 0xc0440000 - 4 = 0xc043fffc
        [ 'VEADD_RD_ADDR', 'VEADD_RS1_ADDR', 0xc043fffc, 1, 32, 32 ],
    ] )
    def test_access_fault( self, result, val1, val2, dim, height, width ):
        simulate( self, Case_access_fault, result=result, val1=val1, val2=val2, dim=dim, height=height, width=width )

class Test_veemacc_mm(BaseTest_veemacc_mm):
    inst = Veemacc_mm