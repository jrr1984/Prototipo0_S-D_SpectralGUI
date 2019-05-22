# Generated from "master.h"
#PV_CDECL = __cdecl
#PV_DECL = __declspec(dllexport) PV_CDECL
#PV_CALL_CONV = PV_CDECL
#PV_DECL = __declspec(dllexport) __stdcall
#PV_CALL_CONV = __stdcall
#LIB_EXPORT = __declspec(dllexport)
#PV_CALL_CONV = __stdcall
#PV_PTR_DECL = *
#PV_BUFP_DECL = *
#FALSE = PV_FAIL
#TRUE = PV_OK
#BIG_ENDIAN = FALSE
CAM_NAME_LEN = 32
PARAM_NAME_LEN = 32
MAX_CAM = 16


# Generated from "pvcam.h"
TYPE_CHAR_PTR = 13
TYPE_INT8 = 12
TYPE_UNS8 = 5
TYPE_INT16 = 1
TYPE_UNS16 = 6
TYPE_INT32 = 2
TYPE_UNS32 = 7
TYPE_UNS64 = 8
TYPE_FLT64 = 4
TYPE_ENUM = 9
TYPE_BOOLEAN = 11
TYPE_VOID_PTR = 14
TYPE_VOID_PTR_PTR = 15
CLASS0 = 0
CLASS1 = 1
CLASS2 = 2
CLASS3 = 3
CLASS4 = 4
CLASS5 = 5
CLASS6 = 6
CLASS7 = 7
CLASS29 = 29
CLASS30 = 30
CLASS31 = 31
CLASS32 = 32
CLASS91 = 91
CLASS92 = 92
CLASS93 = 93
CLASS94 = 94
CLASS95 = 95
CLASS96 = 96
CLASS97 = 97
CLASS98 = 98
CLASS99 = 99
PARAM_DD_INFO_LENGTH = ((CLASS0<<16) + (TYPE_INT16<<24) + 1)
PARAM_DD_VERSION = ((CLASS0<<16) + (TYPE_UNS16<<24) + 2)
PARAM_DD_RETRIES = ((CLASS0<<16) + (TYPE_UNS16<<24) + 3)
PARAM_DD_TIMEOUT = ((CLASS0<<16) + (TYPE_UNS16<<24) + 4)
PARAM_DD_INFO = ((CLASS0<<16) + (TYPE_CHAR_PTR<<24) + 5)
PARAM_MIN_BLOCK = ((CLASS2<<16) + (TYPE_INT16<<24)     +  60)
PARAM_NUM_MIN_BLOCK = ((CLASS2<<16) + (TYPE_INT16<<24)     +  61)
PARAM_SKIP_AT_ONCE_BLK = ((CLASS2<<16) + (TYPE_INT32<<24)     + 536)
PARAM_NUM_OF_STRIPS_PER_CLR = ((CLASS2<<16) + (TYPE_INT16<<24)     +  98)
PARAM_CONT_CLEARS = ((CLASS2<<16) + (TYPE_BOOLEAN<<24)     + 540)
PARAM_ANTI_BLOOMING = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 293)
PARAM_LOGIC_OUTPUT = ((CLASS2<<16) + (TYPE_ENUM<<24)      +  66)
PARAM_EDGE_TRIGGER = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 106)
PARAM_INTENSIFIER_GAIN = ((CLASS2<<16) + (TYPE_INT16<<24)     + 216)
PARAM_SHTR_GATE_MODE = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 217)
PARAM_ADC_OFFSET = ((CLASS2<<16) + (TYPE_INT16<<24)     + 195)
PARAM_CHIP_NAME = ((CLASS2<<16) + (TYPE_CHAR_PTR<<24)  + 129)
PARAM_COOLING_MODE = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 214)
PARAM_PREAMP_DELAY = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 502)
PARAM_PREFLASH = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 503)
PARAM_COLOR_MODE = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 504)
PARAM_MPP_CAPABLE = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 224)
PARAM_PREAMP_OFF_CONTROL = ((CLASS2<<16) + (TYPE_UNS32<<24)     + 507)
PARAM_SERIAL_NUM = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 508)
PARAM_PREMASK = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  53)
PARAM_PRESCAN = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  55)
PARAM_POSTMASK = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  54)
PARAM_POSTSCAN = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  56)
PARAM_PIX_PAR_DIST = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 500)
PARAM_PIX_PAR_SIZE = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  63)
PARAM_PIX_SER_DIST = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 501)
PARAM_PIX_SER_SIZE = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  62)
PARAM_SUMMING_WELL = ((CLASS2<<16) + (TYPE_BOOLEAN<<24)   + 505)
PARAM_FWELL_CAPACITY = ((CLASS2<<16) + (TYPE_UNS32<<24)     + 506)
PARAM_PAR_SIZE = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  57)
PARAM_SER_SIZE = ((CLASS2<<16) + (TYPE_UNS16<<24)     +  58)
PARAM_ACCUM_CAPABLE = ((CLASS2<<16) + (TYPE_BOOLEAN<<24)   + 538)
PARAM_FLASH_DWNLD_CAPABLE = ((CLASS2<<16) + (TYPE_BOOLEAN<<24)   + 539)
PARAM_CONTROLLER_ALIVE = ((CLASS2<<16) + (TYPE_BOOLEAN<<24)   + 168)
PARAM_READOUT_TIME = ((CLASS2<<16) + (TYPE_FLT64<<24)     + 179)
PARAM_CLEAR_CYCLES = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 97)
PARAM_CLEAR_MODE = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 523)
PARAM_FRAME_CAPABLE = ((CLASS2<<16) + (TYPE_BOOLEAN<<24)   + 509)
PARAM_PMODE = ((CLASS2<<16) + (TYPE_ENUM <<24)     + 524)
PARAM_CCS_STATUS = ((CLASS2<<16) + (TYPE_INT16<<24)     + 510)
PARAM_TEMP = ((CLASS2<<16) + (TYPE_INT16<<24)     + 525)
PARAM_TEMP_SETPOINT = ((CLASS2<<16) + (TYPE_INT16<<24)     + 526)
PARAM_CAM_FW_VERSION = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 532)
PARAM_HEAD_SER_NUM_ALPHA = ((CLASS2<<16) + (TYPE_CHAR_PTR<<24)  + 533)
PARAM_PCI_FW_VERSION = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 534)
PARAM_CAM_FW_FULL_VERSION = ((CLASS2<<16) + (TYPE_CHAR_PTR<<24)  + 534)
PARAM_EXPOSURE_MODE = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 535)
PARAM_BIT_DEPTH = ((CLASS2<<16) + (TYPE_INT16<<24)     + 511)
PARAM_GAIN_INDEX = ((CLASS2<<16) + (TYPE_INT16<<24)     + 512)
PARAM_SPDTAB_INDEX = ((CLASS2<<16) + (TYPE_INT16<<24)     + 513)
PARAM_READOUT_PORT = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 247)
PARAM_PIX_TIME = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 516)
PARAM_SHTR_CLOSE_DELAY = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 519)
PARAM_SHTR_OPEN_DELAY = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 520)
PARAM_SHTR_OPEN_MODE = ((CLASS2<<16) + (TYPE_ENUM <<24)     + 521)
PARAM_SHTR_STATUS = ((CLASS2<<16) + (TYPE_ENUM <<24)     + 522)
PARAM_SHTR_CLOSE_DELAY_UNIT = ((CLASS2<<16) + (TYPE_ENUM <<24)     + 543)
PARAM_IO_ADDR = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 527)
PARAM_IO_TYPE = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 528)
PARAM_IO_DIRECTION = ((CLASS2<<16) + (TYPE_ENUM<<24)      + 529)
PARAM_IO_STATE = ((CLASS2<<16) + (TYPE_FLT64<<24)     + 530)
PARAM_IO_BITDEPTH = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 531)
PARAM_GAIN_MULT_FACTOR = ((CLASS2<<16) + (TYPE_UNS16<<24)     + 537)
PARAM_GAIN_MULT_ENABLE = ((CLASS2<<16) + (TYPE_BOOLEAN<<24)   + 541)
PARAM_PP_FEAT_NAME = ((CLASS2<<16) + (TYPE_CHAR_PTR<<24)	+  542)
PARAM_PP_INDEX = ((CLASS2<<16) + (TYPE_INT16<<24)	+  543)
PARAM_ACTUAL_GAIN = ((CLASS2<<16) + (TYPE_UNS16<<24)	+  544)
PARAM_PP_PARAM_INDEX = ((CLASS2<<16) + (TYPE_INT16<<24)	+  545)
PARAM_PP_PARAM_NAME = ((CLASS2<<16) + (TYPE_CHAR_PTR<<24)	+  546)
PARAM_PP_PARAM = ((CLASS2<<16) + (TYPE_UNS32<<24)	+  547)
PARAM_READ_NOISE = ((CLASS2<<16) + (TYPE_UNS16<<24)	+  548)
PARAM_PP_FEAT_ID = ((CLASS2<<16) + (TYPE_UNS16<<24)	+  549)
PARAM_PP_PARAM_ID = ((CLASS2<<16) + (TYPE_UNS16<<24)	+  550)
PARAM_EXP_TIME = ((CLASS3<<16) + (TYPE_UNS16<<24)     +   1)
PARAM_EXP_RES = ((CLASS3<<16) + (TYPE_ENUM<<24)      +   2)
PARAM_EXP_MIN_TIME = ((CLASS3<<16) + (TYPE_FLT64<<24)     +   3)
PARAM_EXP_RES_INDEX = ((CLASS3<<16) + (TYPE_UNS16<<24)     +   4)
PARAM_BOF_EOF_ENABLE = ((CLASS3<<16) + (TYPE_ENUM<<24)      +   5)
PARAM_BOF_EOF_COUNT = ((CLASS3<<16) + (TYPE_UNS32<<24)     +   6)
PARAM_BOF_EOF_CLR = ((CLASS3<<16) + (TYPE_BOOLEAN<<24)   +   7)
PARAM_CIRC_BUFFER = ((CLASS3<<16) + (TYPE_BOOLEAN<<24)   + 299)
PARAM_HW_AUTOSTOP = ((CLASS3<<16) + (TYPE_INT16<<24)     + 166)
ERROR_MSG_LEN = 255
CCD_NAME_LEN = 17
MAX_ALPHA_SER_NUM_LEN = 32
MAX_PP_NAME_LEN = 32
PP_MAX_PARAMETERS_PER_FEATURE = 10
