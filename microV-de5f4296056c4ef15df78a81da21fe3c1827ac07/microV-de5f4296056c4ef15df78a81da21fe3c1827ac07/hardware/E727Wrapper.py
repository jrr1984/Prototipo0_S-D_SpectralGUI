import ctypes# give location of dll
from ctypes import c_int, c_bool, c_void_p, c_float, c_double, c_char, c_char_p, c_ulong, byref, create_string_buffer
import os

libDLL = ctypes.windll.LoadLibrary( os.path.abspath(__file__).split('E727Wrapper.py')[0]+'PI_GCS2_DLL_x64.dll')


#BOOL PI_GcsCommandset (int ID, const char* szCommand)
#BOOL PI_GcsGetAnswer (int ID, char* szAnswer, int iBufferSize)
#BOOL PI_GcsGetAnswerSize (int ID, int* piAnswerSize)

PI_GcsCommandset = libDLL['PI_GcsCommandset']
PI_GcsCommandset.argtypes = (c_int, c_char_p)
PI_GcsCommandset.restype = c_int

PI_GcsGetAnswer = libDLL['PI_GcsGetAnswer']
PI_GcsGetAnswer.argtypes = (c_int, c_char_p, c_int)
PI_GcsGetAnswer.restype = c_int

PI_GcsGetAnswerSize = libDLL['PI_GcsGetAnswerSize']
PI_GcsGetAnswerSize.argtypes = (c_int, ctypes.POINTER(c_int))
PI_GcsGetAnswerSize.restype = c_int

PI_EnumerateUSB = libDLL['PI_EnumerateUSB']
PI_EnumerateUSB.argtypes = (c_char_p,c_int,c_char_p)

PI_ConnectUSBWithBaudRate = libDLL['PI_ConnectUSBWithBaudRate']
PI_ConnectUSBWithBaudRate.argtypes = (c_char_p, c_int)
PI_ConnectUSBWithBaudRate.restype = c_int

PI_ConnectUSB = libDLL['PI_ConnectUSB']
PI_ConnectUSB.argtypes = (c_char_p,)
PI_ConnectUSB.restype = c_int

PI_CloseConnection = libDLL['PI_CloseConnection']
PI_CloseConnection.argtypes = (c_int,)
PI_CloseConnection.restype = c_void_p

PI_GetError = libDLL['PI_GetError']
PI_GetError.argtypes = (c_int,)
PI_GetError.restype = c_int

#PI_BRA = libDLL['PI_BRA']
#PI_BRA.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
#PI_BRA.restype = c_bool

#PI_qBRA = libDLL['PI_qBRA']
#PI_qBRA.argtypes = (c_int,c_char_p, c_int)
#PI_qBRA.restype = c_bool

PI_TranslateError = libDLL['PI_TranslateError']
PI_TranslateError.argtypes = (c_int,c_char_p,c_int)
PI_TranslateError.restype = c_bool

PI_qCTV = libDLL['PI_qCTV']
PI_qCTV.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double))
PI_qCTV.restype = c_bool

PI_qSAI = libDLL['PI_qSAI']
PI_qSAI.argtypes = (c_int,c_char_p, c_int)
PI_qSAI.restype = c_bool

PI_SVO = libDLL['PI_SVO']
PI_SVO.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
PI_SVO.restype = c_bool

PI_qSVO = libDLL['PI_qSVO']
PI_qSVO.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
PI_qSVO.restype = c_bool

PI_ATZ = libDLL['PI_ATZ']
PI_ATZ.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double),ctypes.POINTER(c_bool))
PI_ATZ.restype = c_bool

PI_MOV = libDLL['PI_MOV']
PI_MOV.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double))
PI_MOV.restype = c_bool

PI_qPOS = libDLL['PI_qPOS']
PI_qPOS.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double))
PI_qPOS.restype = c_bool

PI_IsMoving = libDLL['PI_IsMoving']
PI_IsMoving.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
PI_IsMoving.restype = c_bool

'''
BOOL PI_EAX (int ID, const char* szAxes, const BOOL* pbValueArray)
Enable Axis
'''
#PI_EAX = libDLL['PI_EAX']
#PI_EAX.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
#PI_EAX.restype = c_bool

'''
BOOL PI_qEAX (int ID, const char* szAxes, BOOL* pbValueArray)
Get Enable Status Of Axes
'''

#PI_qEAX = libDLL['PI_qEAX']
#PI_qEAX.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
#PI_qEAX.restype = c_bool

'''
BOOL PI_CMO (int ID, const char* szAxes, const int* piValueArray)
Select closed-loop control mode
'''
#PI_CMO = libDLL['PI_CMO']
#PI_CMO.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
#PI_CMO.restype = c_bool

'''
BOOL PI_qCMO (int ID, const char* szAxes, int* piValueArray)
Get closed-loop control mode
'''

#PI_qCMO = libDLL['PI_qCMO']
#PI_qCMO.argtypes = (c_int,c_char_p, ctypes.POINTER(c_int))
#PI_qCMO.restype = c_bool

'''
BOOL PI_qCTV (int ID, const char* szAxes, double* pdValueArray)
Get Target Values
'''

'''BOOL PI_VEL (int ID, const char* szAxes, const double* pdValueArray)
Set Closed-Loop Velocity
'''
PI_VEL = libDLL['PI_VEL']
PI_VEL.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double))
PI_VEL.restype = c_bool

'''BOOL PI_qVEL (int ID, const char* szAxes, double* pdValueArray)
Get Closed-Loop Velocity
'''
PI_qVEL = libDLL['PI_qVEL']
PI_qVEL.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double))
PI_qVEL.restype = c_bool

'''
BOOL PI_WAV_SIN_P (int ID, int iWaveTableId, int iOffsetOfFirstPointInWaveTable,
 int iNumberOfPoints, int iAppendWave, int iCenterPointOfWave,
 double dAmplitudeOfWave, double dOffsetOfWave, int iSegmentLength)
'''

PI_WAV_SIN_P = libDLL['PI_WAV_SIN_P']
PI_WAV_SIN_P.argtypes = (c_int, c_int, c_int, c_int, c_int, c_int, c_double, c_double, c_int)
PI_WAV_SIN_P.restype = c_bool

'''
BOOL PI_DRC (int ID, const int* piRecordTableIdsArray, const char* szRecordSource, const int* piRecordOptionsArray)
Set Data Recorder Configuration
'''

PI_DRC = libDLL['PI_DRC']
PI_DRC.argtypes = (c_int, ctypes.POINTER(c_int), c_char_p, ctypes.POINTER(c_int))
PI_DRC.restype = c_bool

'''
BOOL PI_WSL (int ID, const int* piWaveGeneratorIdsArray, const int* piWaveTableIdsArray, int iArraySize)
Wave table selection: connects a wave table to a wave generator
'''

PI_WSL = libDLL['PI_WSL']
PI_WSL.argtypes = (c_int, ctypes.POINTER(c_int), ctypes.POINTER(c_int), c_int)
PI_WSL.restype = c_bool


'''
BOOL PI_WGO (int ID, const int* piWaveGeneratorIdsArray, condt int* piStartModArray, int iArraySize)
Start and stop the specified wave generator
'''

PI_WGO = libDLL['PI_WGO']
PI_WGO.argtypes = (c_int, ctypes.POINTER(c_int), ctypes.POINTER(c_int), c_int)
PI_WGO.restype = c_bool

'''
BOOL PI_qWGO (int ID, const int piWaveGeneratorIdsArray, int* piValueArray, int iArraySize)
Get the start/stop mode of the given wave generator
'''
PI_qWGO = libDLL['PI_WGO']
PI_qWGO.argtypes = (c_int, ctypes.POINTER(c_int), ctypes.POINTER(c_int), c_int)
PI_qWGO.restype = c_bool

'''
BOOL PI_qDRR (int ID, const int* piRecTableIdsArray, int iNumberOfRecTables,
int iOffsetOfFirstPointInRecordTable, int iNumberOfValues,
double** pdValueArray, char* szGcsArrayHeader, int iGcsArrayHeaderMaxSize)
Get Recorded Data Values
'''
PI_qDRR = libDLL['PI_qDRR']
PI_qDRR.argtypes = (c_int, ctypes.POINTER(c_int), c_int, c_int, c_int, ctypes.POINTER(ctypes.POINTER(c_double)),c_char_p,c_int)
PI_qDRR.restype = c_bool

'''
BOOL PI_qDRR_SYNC (int ID, int iRecordTableId, int iOffsetOfFirstPointInRecordTable, int iNumberOfValues, double* pdValueArray)
'''
PI_qDRR_SYNC = libDLL['PI_qDRR_SYNC']
PI_qDRR_SYNC.argtypes = (c_int, c_int, c_int, c_int, ctypes.POINTER(c_double))
PI_qDRR_SYNC.restype = c_bool

'''
int PI_GetAsyncBufferIndex (int ID)
Get index used for the internal buffer
'''
PI_GetAsyncBufferIndex = libDLL['PI_GetAsyncBufferIndex']
PI_GetAsyncBufferIndex.argtypes = (c_int,)
PI_GetAsyncBufferIndex.restype = c_int

'''
BOOL PI_WAV_PNT (int ID, int iWaveTableId, int iOffsetOfFirstPointInWaveTable,
int iNumberOfWavePoints, int iAppendWave, const double* pdWavePoints )
'''

PI_WAV_PNT = libDLL['PI_WAV_PNT']
PI_WAV_PNT.argtypes = (c_int, c_int, c_int, c_int, c_int, ctypes.POINTER(c_double))
PI_WAV_PNT.restype = c_bool


'''
BOOL PI_qTWG (int ID, int* iNumberOfWaveGenerators)
Get the number of wave generators
'''
PI_qTWG = libDLL['PI_qTWG']
PI_qTWG.argtypes = (c_int, ctypes.POINTER(c_int))
PI_qTWG.restype = c_bool


'''
BOOL PI_qDTL (int ID, const int* piDdlTableIdsArray, int* piValueArray, int iArraySize)
Get DDL table length
'''
PI_qDTL = libDLL['PI_qDTL']
PI_qDTL.argtypes = (c_int, ctypes.POINTER(c_int),ctypes.POINTER(c_int),c_int)
PI_qDTL.restype = c_bool


'''
BOOL PI_WGC (int ID, const int* piWaveGeneratorIdsArray, const int* piNumberOfCyclesArray, int iArraySize)
Set the number of cycles for the wave generator output
'''

PI_WGC = libDLL['PI_WGC']
PI_WGC.argtypes = (c_int, ctypes.POINTER(c_int),ctypes.POINTER(c_int),c_int)
PI_WGC.restype = c_bool
