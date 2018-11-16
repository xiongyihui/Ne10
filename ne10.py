import os
from ctypes import (cdll, create_string_buffer,
                    CFUNCTYPE, ARRAY, Structure, POINTER, pointer,
                    c_char_p, c_ubyte, c_ushort, c_int, c_uint, c_float, c_void_p)


c_float_p = POINTER(c_float)

# typedef struct
# {
#     ne10_uint8_t  M;            /**< Decimation Factor. */
#     ne10_uint16_t numTaps;      /**< Length of the filter. */
#     ne10_float32_t    *pCoeffs;      /**< Points to the coefficient array. The array is of length numTaps.*/
#     ne10_float32_t    *pState;       /**< Points to the state variable array. The array is of length numTaps+maxBlockSize-1. */
# } ne10_fir_decimate_instance_f32_t;

class DecimatorStructure(Structure):
    _fields_ = [
        ('M', c_ubyte),
        ('numTaps', c_ushort),
        ('pCoeffs', c_float_p),
        ('pState', c_float_p)]


class Decimator(object):
    def __init__(self, factor, coeffs, block_size):
        if block_size % factor:
            raise ValueError('The block size must be a multiple of the decimation factor')

        self.block_size = block_size

        _lib_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libNE10.so')
        self._lib = cdll.LoadLibrary(_lib_path)

        self._lib.ne10_init.argtypes = []
        self._lib.ne10_init.restype = c_int


        # ne10_result_t ne10_fir_decimate_init_float (
        #     ne10_fir_decimate_instance_f32_t * S,
        #     ne10_uint16_t numTaps,
        #     ne10_uint8_t M,
        #     ne10_float32_t * pCoeffs,
        #     ne10_float32_t * pState,
        #     ne10_uint32_t blockSize)


        self._lib.ne10_fir_decimate_init_float.argtypes = [c_void_p, c_ushort, c_ubyte, c_float_p, c_float_p, c_uint]
        self._lib.ne10_fir_decimate_init_float.restype = c_int


        # void ne10_fir_decimate_float_c (const ne10_fir_decimate_instance_f32_t * S,
        #                                 ne10_float32_t * pSrc,
        #                                 ne10_float32_t * pDst,
        #                                 ne10_uint32_t blockSize)
        self._lib.ne10_fir_decimate_float_c.argtypes = [c_void_p, c_float_p, c_float_p, c_uint]
        self._lib.ne10_fir_decimate_float_c.restype = None


        # void ne10_fir_decimate_float_neon (const ne10_fir_decimate_instance_f32_t * S,
        #                                    ne10_float32_t * pSrc,
        #                                    ne10_float32_t * pDst,
        #                                    ne10_uint32_t blockSize)
        self._lib.ne10_fir_decimate_float_neon.argtypes = [c_void_p, c_float_p, c_float_p, c_uint]
        self._lib.ne10_fir_decimate_float_neon.restype = None

        self._instance = DecimatorStructure()

        self.src = ARRAY(c_float, block_size)()
        self.dst = ARRAY(c_float, block_size / factor)()

        #CoeffsBuffer = ARRAY(c_float, len(coeffs))
        self.coeffs_buf = ARRAY(c_float, len(coeffs))()
        StateBuffer = ARRAY(c_float, len(coeffs) + block_size) 
        self.state_buf = StateBuffer()

        for i in range(len(coeffs)):
            self.coeffs_buf[i] = coeffs[i]

        if self._lib.ne10_init():
            raise RuntimeError('ne10_init() failed')

        if self._lib.ne10_fir_decimate_init_float(pointer(self._instance), len(coeffs), factor, self.coeffs_buf, self.state_buf, block_size):
            raise RuntimeError('ne10_fir_decimate_init_float() failed')

    def process(self, data, neon=False):
        if len(data) > self.block_size:
            raise ValueError('data exceeds block size')
        for i in range(len(data)):
            self.src[i] = data[i]

        if neon:
            self._lib.ne10_fir_decimate_float_neon(pointer(self._instance), self.src, self.dst, len(data))
        else:
            self._lib.ne10_fir_decimate_float_c(pointer(self._instance), self.src, self.dst, len(data))

        return self.dst



coeffs = [1., 1., 1., 1.]

decimator = Decimator(3, coeffs, 48)
print([decimator._instance.M, decimator._instance.numTaps, decimator._instance.pCoeffs])


x = [1., 1.] * 48
y = decimator.process(x)
print([f for f in y])
