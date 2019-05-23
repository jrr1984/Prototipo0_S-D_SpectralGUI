/****************************************************************************

   Thorlabs CCS Series (Compact Spectrometer) VISA instrument driver

   FOR DETAILED DESCRIPTION OF THE DRIVER FUNCTIONS SEE THE ONLINE HELP FILE
   AND THE PROGRAMMERS REFERENCE MANUAL.

   Copyright:  Copyright(c) 2008, Thorlabs (www.thorlabs.com)
   Author:     Olaf Wohlmann (owohlmann@thorlabs.com)

   This library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with this library; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


   Header file

   Date:          Mar-13-2013
   Built with:    NI LabWindows/CVI 2012SP1
   Version:       2.0.0

   Changelog:     see 'readme.rtf'

****************************************************************************/

#ifndef __TLCCS_H__
#define __TLCCS_H__

#include <vpptype.h>

#if defined(__cplusplus) || defined(__cplusplus__)
extern "C" {
#endif

#ifndef ViAttrState
   #if defined(_VI_INT64_UINT64_DEFINED) && defined(_VISA_ENV_IS_64_BIT)
   typedef ViUInt64             ViAttrState;
   #else
   typedef ViUInt32             ViAttrState;
   #endif
#endif


/*===========================================================================

 Macros

===========================================================================*/
/*---------------------------------------------------------------------------
 Find pattern for 'viFindRsrc()'
---------------------------------------------------------------------------*/
//                                           Thorlabs Vendor ID               Thorlabs CCS100                  Thorlabs CCS125                  Thorlabs CCS150               Thorlabs CCS175                  Thorlabs CCS200
#define TLCCS_FIND_PATTERN     "USB?*?{VI_ATTR_MANF_ID==0x1313 && ((VI_ATTR_MODEL_CODE==0x8081) || (VI_ATTR_MODEL_CODE==0x8083) || (VI_ATTR_MODEL_CODE==0x8085) || (VI_ATTR_MODEL_CODE==0x8087) || (VI_ATTR_MODEL_CODE==0x8089))}"

/*---------------------------------------------------------------------------
 USB VIDs and PIDs
---------------------------------------------------------------------------*/
#define TLCCS_VID                   0x1313   // Thorlabs
#define CCS100_PID                  0x8081   // CCS100 Compact Spectrometer
#define CCS125_PID                  0x8083   // CCS125 Special Spectrometer 
#define CCS150_PID                  0x8085   // CCS150 UV Spectrometer 
#define CCS175_PID                  0x8087   // CCS175 NIR Spectrometer 
#define CCS200_PID                  0x8089   // CCS200 UV-NIR Spectrometer  
      
/*---------------------------------------------------------------------------
 Version Macros
---------------------------------------------------------------------------*/
#define TLCCS_EXTRACT_MAJOR(revision)                ((revision & 0xFFF00000) >> 20)
#define TLCCS_EXTRACT_MINOR(revision)                ((revision & 0x000FFF00) >> 8)
#define TLCCS_EXTRACT_SUBMINOR(revision)             (revision & 0x000000FF)

/*---------------------------------------------------------------------------
 Communication timeout
---------------------------------------------------------------------------*/
#define TLCCS_TIMEOUT_MIN              1000
#define TLCCS_TIMEOUT_DEF              2000
#define TLCCS_TIMEOUT_MAX              60000

/*---------------------------------------------------------------------------
 Buffers
---------------------------------------------------------------------------*/
#define TLCCS_BUFFER_SIZE              256                     // general buffer size
#define TLCCS_ERR_DESCR_BUFFER_SIZE    512                     // buffer size for error messages
#define TLCCS_TEXT_BUFFER_SIZE         TLCCS_BUFFER_SIZE       // buffer size for texts from the SPX
#define TLCCS_NUM_PIXELS               3648                    // number of effective pixels of CCD
#define TLCCS_NUM_RAW_PIXELS           3694                    // number of raw pixels
#define TLCCS_MAX_USER_NAME_SIZE       32                      // including the trailing '\0'

#define TLCCS_MIN_NUM_USR_ADJ          4                       // minimum number of user adjustment data points
#define TLCCS_MAX_NUM_USR_ADJ          10                      // maximum number of user adjustment data points

/*---------------------------------------------------------------------------
 Driver attributes
---------------------------------------------------------------------------*/
//#define TLCCS_ATTR_USER_DATA         (VI_ATTR_USER_DATA)     // we use the same value as VISA itself (0x3FFF0007UL)
#define TLCCS_ATTR_USER_DATA           (0x3FFF0007UL)          // we do not recursively resolve this value because the LabView driver importer cannot either
#define TLCCS_ATTR_CAL_MODE            (0x3FFA0000UL)          // this attribute is either 0 = user or 1 = THORLABS amplitude correction
                                             
       
/*---------------------------------------------------------------------------
 CCS_SERIES specific constants
---------------------------------------------------------------------------*/
#define TLCCS_MAX_INT_TIME             60.0        // 60s is the maximum integration time
#define TLCCS_MIN_INT_TIME             0.00001     // 10us is the minimum integration time
#define TLCCS_DEF_INT_TIME             0.01        // 10ms is the default integration time

#define TLCCS_CAL_MODE_USER            0
#define TLCCS_CAL_MODE_THORLABS        1

#define TLCCS_AMP_CORR_FACT_MIN        0.001       // the minimum correction factor
#define TLCCS_AMP_CORR_FACT_MAX        1000.0      // the maximum correction factor, standard is 1.0
       
/*---------------------------------------------------------------------------
 Error/Warning Codes
---------------------------------------------------------------------------*/
// Driver Error Codes in the range 0xBFFC0800 ... 0xBFFC0FFF accordingto
// recommendation 3.15 of VXI plug&play Systems Alliance
// VPP-3.4 Instrument Driver Programmatic Developer Interface Spec. Rev. 2.4

#define VI_ERROR_NSUP_COMMAND       (_VI_ERROR + 0x3FFC0801L)     // 0xBFFC0801
#define VI_ERROR_TLCCS_UNKNOWN      (_VI_ERROR + 0x3FFC0802L)     // 0xBFFC0802
#define VI_ERROR_SCAN_DATA_INVALID  (_VI_ERROR + 0x3FFC0803L)     // 0xBFFC0803

#define VI_ERROR_XSVF_SIZE          (_VI_ERROR + 0x3FFC0A00L)     // 0xBFFC0A00
#define VI_ERROR_XSVF_MEMORY        (_VI_ERROR + 0x3FFC0A01L)     // 0xBFFC0A01
#define VI_ERROR_XSVF_FILE          (_VI_ERROR + 0x3FFC0A02L)     // 0xBFFC0A02

#define VI_ERROR_FIRMWARE_SIZE      (_VI_ERROR + 0x3FFC0A10L)     // 0xBFFC0A10
#define VI_ERROR_FIRMWARE_MEMORY    (_VI_ERROR + 0x3FFC0A11L)     // 0xBFFC0A11
#define VI_ERROR_FIRMWARE_FILE      (_VI_ERROR + 0x3FFC0A12L)     // 0xBFFC0A12
#define VI_ERROR_FIRMWARE_CHKSUM    (_VI_ERROR + 0x3FFC0A13L)     // 0xBFFC0A13
#define VI_ERROR_FIRMWARE_BUFOFL    (_VI_ERROR + 0x3FFC0A14L)     // 0xBFFC0A14

#define VI_ERROR_CYEEPROM_SIZE      (_VI_ERROR + 0x3FFC0A20L)     // 0xBFFC0A20
#define VI_ERROR_CYEEPROM_MEMORY    (_VI_ERROR + 0x3FFC0A21L)     // 0xBFFC0A21
#define VI_ERROR_CYEEPROM_FILE      (_VI_ERROR + 0x3FFC0A22L)     // 0xBFFC0A22
#define VI_ERROR_CYEEPROM_CHKSUM    (_VI_ERROR + 0x3FFC0A23L)     // 0xBFFC0A23
#define VI_ERROR_CYEEPROM_BUFOVL    (_VI_ERROR + 0x3FFC0A24L)     // 0xBFFC0A24


// this is the offset added to error from asking the device when it stalled
#define VI_ERROR_USBCOMM_OFFSET     (_VI_ERROR + 0x3FFC0B00L)     // 0xBFFC0B00

// TLCCS Error Codes (codes that will be returned from the device itself)
// these errors are derived from TLCCS_error.h belonging to the 09177_CCS_SERIES project
// (This is the 8051 uController within the Cypress USB chip

#define VI_ERROR_TLCCS_ENDP0_SIZE         (VI_ERROR_USBCOMM_OFFSET + 0x01) // 0xBFFC0B01
#define VI_ERROR_TLCCS_EEPROM_ADR_TO_BIG  (VI_ERROR_USBCOMM_OFFSET + 0x02) // 0xBFFC0B02

#define VI_ERROR_TLCCS_XSVF_UNKNOWN       (VI_ERROR_USBCOMM_OFFSET + 0x11) // 0xBFFC0B11
#define VI_ERROR_TLCCS_XSVF_TDOMISMATCH   (VI_ERROR_USBCOMM_OFFSET + 0x12) // 0xBFFC0B12
#define VI_ERROR_TLCCS_XSVF_MAXRETRIES    (VI_ERROR_USBCOMM_OFFSET + 0x13) // 0xBFFC0B13
#define VI_ERROR_TLCCS_XSVF_ILLEGALCMD    (VI_ERROR_USBCOMM_OFFSET + 0x14) // 0xBFFC0B14
#define VI_ERROR_TLCCS_XSVF_ILLEGALSTATE  (VI_ERROR_USBCOMM_OFFSET + 0x15) // 0xBFFC0B15
#define VI_ERROR_TLCCS_XSVF_DATAOVERFLOW  (VI_ERROR_USBCOMM_OFFSET + 0x16) // 0xBFFC0B16

#define VI_ERROR_TLCCS_I2C_NACK           (VI_ERROR_USBCOMM_OFFSET + 0x20) // 0xBFFC0B20
#define VI_ERROR_TLCCS_I2C_ERR            (VI_ERROR_USBCOMM_OFFSET + 0x21) // 0xBFFC0B21

// Driver Error Codes
#define VI_ERROR_TLCCS_READ_INCOMPLETE    (VI_ERROR_USBCOMM_OFFSET + 0x40)
#define VI_ERROR_TLCCS_NO_USER_DATA       (VI_ERROR_USBCOMM_OFFSET + 0x41) // there is no wavelength adjustment data available at the instruments nonvolatile memory
#define VI_ERROR_TLCCS_INV_USER_DATA      (VI_ERROR_USBCOMM_OFFSET + 0x42) // the given wavelength adjustment data results in negative wavelength values.
#define VI_ERROR_TLCCS_INV_ADJ_DATA       (VI_ERROR_USBCOMM_OFFSET + 0x43) // read out amplitude/wavelength adjustment data is out of range/corrupt



/*===========================================================================

 GLOBAL USER-CALLABLE FUNCTION DECLARATIONS (Exportable Functions)

===========================================================================*/
/*===========================================================================


 Init/close


===========================================================================*/
/*---------------------------------------------------------------------------
   Function:   Initialize
   Purpose:    This function initializes the instrument driver session and
               returns an instrument handle which is used in subsequent calls.

   Input Parameters:
   ViRsrc rsrcName:           Instrument Description
   ViBoolean id_query:        Boolean to query the ID or not
   ViBoolean reset_instr:     Boolean to reset the device or not

   Output Parameters:
   ViPSession vi:             Instrument Handle
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_init (ViRsrc rsrcName, ViBoolean id_query,
                              ViBoolean reset_instr, ViPSession vi);

/*---------------------------------------------------------------------------
   Function:   Close
   Purpose:    This function close an instrument driver session.

   Input Parameters:
   ViSession vi:              Instrument Handle
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_close (ViSession vi);


/*===========================================================================


 Class: Configuration Functions.


===========================================================================*/
/*---------------------------------------------------------------------------
   Function:   Set Integration Time
   Purpose:    This function set the optical integration time in seconds.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViReal64 integrationTime:  The optical integration time.
                              Min: TLCCS_MIN_INT_TIME (1.0E-5)
                              Max: TLCCS_MAX_INT_TIME (6.0E+1)
                              Default value: 1.0E-3.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_setIntegrationTime (ViSession vi, ViReal64 integrationTime);


/*---------------------------------------------------------------------------
   Function:   Get Integration Time
   Purpose:    This function returns the optical integration time in seconds.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViPReal64 integrationTime: The optical integration time.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_getIntegrationTime (ViSession vi, ViPReal64 integrationTime);

/*===========================================================================


 Class: Action/Status Functions.


===========================================================================*/
/*---------------------------------------------------------------------------
   Function:   Start Scan
   Purpose:    This function triggers the the CCS to take one single scan.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Note:
   The scan data can be read out with the function 'Get Scan Data'
   Use 'Get Device Status' to check the scan status.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_startScan (ViSession vi);


/*---------------------------------------------------------------------------
   Function:   Start Continuous Scan
   Purpose:    This function starts the CCS scanning continuously.
               Any other function except 'Get Scan Data' and 'Get Device Status'
               will stop the scanning.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Note:
   The scan data can be read out with the function 'Get Scan Data'
   Use 'Get Device Status' to check the scan status.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_startScanCont (ViSession vi);


/*---------------------------------------------------------------------------
   Function:   Start Extern Scan
   Purpose:    This function arms the external trigger of the CCS. A
               following low to high transition at the trigger input of the
               CCS then starts a scan.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Note:
   When you issue a read command 'Get Scan Data' before the CCS was
   triggered you will get a timeout error. Use 'Get Device Status' to check
   the scan status.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_startScanExtTrg (ViSession vi);


/*---------------------------------------------------------------------------
   Function:   Start Continuous Extern Scan
   Purpose:    This function arms the CCS for scanning after an external
               trigger. A following low to high transition at the trigger input
               of the CCS then starts a scan. The CCS will rearm immediately
               after the scan data is readout. Any other function except
               'Get Scan Data' or 'Get Device Status' will stop the scanning.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Note:
   The scan data can be read out with the function 'Get Scan Data'

   Note:
   When you issue a read command 'Get Scan Data' before the CCS was triggered
   you will get a timeout error. Use 'Get Device Status' to check the scan status.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_startScanContExtTrg (ViSession vi);


/*---------------------------------------------------------------------------
   Function:   Get Device Status
   Purpose:    This function returns the device status. Use macros to mask
               out single bits.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViPInt32 deviceStatus:     The device status returned from the instrument
---------------------------------------------------------------------------*/
#define TLCCS_STATUS_SCAN_IDLE         0x0002      // CCS waits for new scan to execute
#define TLCCS_STATUS_SCAN_TRIGGERED    0x0004      // scan in progress
#define TLCCS_STATUS_SCAN_START_TRANS  0x0008      // scan starting
#define TLCCS_STATUS_SCAN_TRANSFER     0x0010      // scan is done, waiting for data transfer to PC
#define TLCCS_STATUS_WAIT_FOR_EXT_TRIG 0x0080      // same as IDLE except that external trigger is armed

ViStatus _VI_FUNC tlccs_getDeviceStatus (ViSession vi, ViPInt32 deviceStatus);



/*===========================================================================


 Class: Data Functions.


===========================================================================*/
/*---------------------------------------------------------------------------
   Function:   Get Scan Data
   Purpose:    This function reads out the processed scan data.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViReal64 data[]:           The measurement array (TLCCS_NUM_PIXELS elements).
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_getScanData (ViSession vi, ViReal64 data[]);


/*---------------------------------------------------------------------------
   Function:   Get Raw Scan Data
   Purpose:    This function reads out the raw scan data.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViInt32 scanDataArray[]:   The measurement array (TLCCS_NUM_RAW_PIXELS elements).
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_getRawScanData (ViSession vi, ViInt32 scanDataArray[]);


/*---------------------------------------------------------------------------
   Function:   Set Wavelength Data
   Purpose:    This function stores data for user-defined pixel-wavelength
               correlation to the instrument's nonvolatile memory.

               The given data pair arrays are used to interpolate the
               pixel-wavelength correlation array returned by the
               TLCCS_getWavelengthData function.

   Note: In case the interpolated pixel-wavelength correlation
   contains negative values, or the values are not strictly
   increasing the function returns with error VI_ERROR_INV_USER_DATA.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViInt32 pixelDataArray[]:  The pixel data.
   ViReal64 wavelengthDataArray[]:The wavelength data.
   ViInt32 bufferLength:      The length of both arrays.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_setWavelengthData (ViSession vi, ViInt32 pixelDataArray[],
                                           ViReal64 wavelengthDataArray[], ViInt32 bufferLength);


/*---------------------------------------------------------------------------
   Function:   Get Wavelength Data
   Purpose:    This function returns data for the pixel-wavelength correlation.
               The maximum and the minimum wavelength are additionally provided
               in two separate return values.

   Note:
   If you do not need either of these values you may pass NULL.

   The value returned in Wavelength_Data_Array[0] is the wavelength
   at pixel 0, this is also the minimum wavelength, the value
   returned in Wavelength_Data_Array[1] is the wavelength at pixel
   1 and so on until Wavelength_Data_Array[TLCCS_NUM_PIXELS-1]
   which provides the wavelength at pixel TLCCS_NUM_PIXELS-1
   (3647). This is the maximum wavelength.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViInt16 dataSet:           The pixel data selection according to macros below.

   Output Parameters:
   ViReal64 wavelengthDataArray[]:  The wavelength data.
   ViPReal64 minimumWavelength:     The minimum wavelength.
   ViPReal64 maximumWavelength:     The maximum wavelength.
---------------------------------------------------------------------------*/
#define TLCCS_CAL_DATA_SET_FACTORY     0
#define TLCCS_CAL_DATA_SET_USER        1

ViStatus _VI_FUNC tlccs_getWavelengthData (ViSession vi, ViInt16 dataSet, ViReal64 wavelengthDataArray[],
                                           ViPReal64 minimumWavelength, ViPReal64 maximumWavelength);



/*---------------------------------------------------------------------------
   Function:   Get User Calibration Points
   Purpose:    This function returns the user-defined pixel-wavelength
               correlation supporting points. These given data pair arrays are
               used by the driver to interpolate the pixel-wavelength
               correlation array returned by the tlccs_getWavelengthData
               function.

   Note:
   If you do not need either of these values you may pass NULL.
   The function returns with error VI_ERROR_NO_USER_DATA if no user
   calibration data is present in the instruments nonvolatile
   memory.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViInt32 pixelDataArray[]:        The pixel data array.
   ViReal64 wavelengthDataArray[]:  The wavelength data array.
   ViPInt32 bufferLength:           The number of user calibration points.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_getUserCalibrationPoints (ViSession vi, ViInt32 pixelDataArray[],
                                                  ViReal64 wavelengthDataArray[], ViPInt32 bufferLength);

/*---------------------------------------------------------------------------
   Function:   Set Amplitude Data
   Purpose:    This function stores data for user-defined amplitude
               correction factors to nonvolatile memory of CCD device.

               The given data array can be used to correct the
               amplitude information returned by the
               tlccs_getScanDataData function.

   Note: In case the correction factors are out of the range
   TLCCS_AMP_CORR_FACT_MIN (0.001) ... TLCCS_AMP_CORR_FACT_MAX (1000.0)
   the function returns with error VI_ERROR_TLCCS_INV_USER_DATA. 

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViReal64 AmpCorrFact[]:    The array with amplitude correction factors
   ViInt32 bufferLength:      The length of the array.
   ViInt32 bufferStart:       The start index for the array.
   ViInt32 mode               With mode one can select if the new data will be applied to current measurements
                              only (ACOR_APPLY_TO_MEAS) or additionally goes to non volatile memory of the
                              device too (ACOR_APPLY_TO_MEAS_NVMEM).
                              If mode is not one of the two predefined macros the function returns VI_ERROR_INV_PARAMETER
---------------------------------------------------------------------------*/
#define ACOR_APPLY_TO_MEAS          1     // macro for parameter mode
#define ACOR_APPLY_TO_MEAS_NVMEM    2     // macro for parameter mode

ViStatus _VI_FUNC tlccs_setAmplitudeData (ViSession vi, ViReal64 AmpCorrFact[], ViInt32 bufferLength, ViInt32 bufferStart, ViInt32 mode);


/*---------------------------------------------------------------------------
   Function:   Get Amplitude Data
   Purpose:    This function retrieves data for user-defined amplitude
               correction factors from nonvolatile memory of CCD device.

               The given data array can be used to correct the
               amplitude information returned by the
               tlccs_getScanDataData function.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViInt32 bufferLength:      The length of the array.
   ViInt32 bufferStart:       The start index for the array.
   ViInt32 mode               With mode one can select if the data will be a copy of the currently used
                              amplitude correction factors (ACOR_FROM_CURRENT) or if the data is read out from the
                              device non volatile memory (ACOR_FROM_NVMEM)
                              If mode is not one of the two predefined macros the function returns VI_ERROR_INV_PARAMETER

   Output Parameters:
   ViReal64 _VI_FAR AmpCorrFact[]:  The array with amplitude correction factors
---------------------------------------------------------------------------*/
#define ACOR_FROM_CURRENT           1     // macro for parameter mode
#define ACOR_FROM_NVMEM             2     // macro for parameter mode

ViStatus _VI_FUNC tlccs_getAmplitudeData (ViSession vi, ViReal64 AmpCorrFact[], ViInt32 bufferStart, ViInt32 bufferLength, ViInt32 mode);

/*===========================================================================


 Class: Utility Functions.


===========================================================================*/
/*---------------------------------------------------------------------------
   Function:   Identification Query
   Purpose:    This function returns the device identification information.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViString manufacturerName: The manufacturers name.
   ViString deviceName:       The device name.
   ViString serialNumber:     The serial number.
   ViString firmwareRevision: The firmware revision.
   ViString instrumentDriverRevision:The instrument driver revision.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_identificationQuery (ViSession vi,
                                             ViString manufacturerName,
                                             ViString deviceName,
                                             ViString serialNumber,
                                             ViString firmwareRevision,
                                             ViString instrumentDriverRevision);


/*---------------------------------------------------------------------------
   Function:   Revision Query
   Purpose:    This function returns the revision of the instrument driver
               and the firmware revision of the instrument being used.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViString driver_rev:       Instrument driver revision
   ViString instr_rev:        Instrument firmware revision
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_revision_query (ViSession vi, ViString driver_rev, ViString instr_rev);


/*---------------------------------------------------------------------------
   Function:   Reset
   Purpose:    This function resets the device.

   Input Parameters:
   ViSession vi:              Instrument Handle
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_reset (ViSession vi);

/*---------------------------------------------------------------------------
   Function:   Self Test
   Purpose:    This function resets the device.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViPInt16 test_result:      Numeric result from self-test operation
                              0 = no error (test passed)
   ViString test_message:     Self-test status message
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_self_test (ViSession vi, ViPInt16 test_result, ViString test_message);


/*---------------------------------------------------------------------------
   Function:   Error Query
   Purpose:    This function queries the instrument and returns instrument-
               specific error information.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViPInt32 error_code:       Instrument error code
   ViString error_message:    Error message
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_error_query(ViSession vi, ViPInt32 error_code, ViString error_message);

/*---------------------------------------------------------------------------
   Function:   Error Message
   Purpose:    This function translates the error return value from a
               VXIplug&play instrument driver function to a user-readable
               string.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViStatus status_code:      Instrument driver error code

   Output Parameters:
   ViString message:          VISA or instrument driver Error message
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_error_message(ViSession vi, ViStatus status_code, ViString message);


/*---------------------------------------------------------------------------
   Function:   Set Attribute
   Purpose:    This function sets a specified attribute.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViAttr attribute:          The attribute to set. See "Driver attributes"
                              section for available attributes and further
                              information.
   ViAttrState value:         The attribute value.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_setAttribute (ViSession vi, ViAttr attribute, ViAttrState value);

/*---------------------------------------------------------------------------
   Function:   Get Attribute
   Purpose:    This function returns a specified attribute.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViAttr attribute:          The attribute to get. See "Driver attributes"
                              section for available attributes and further
                              information.

   Output Parameters:
   ViAttrState value:         The attribute value.
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_getAttribute (ViSession vi, ViAttr attribute, ViAttrState *value);

/*---------------------------------------------------------------------------
   Function:   Set User Text
   Purpose:    This function writes the given string to the novolatile memory of
               the spectrometer.

   Input Parameters:
   ViSession vi:              Instrument Handle
   ViString userText:         The new user text
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_setUserText (ViSession vi, ViString userText);


/*---------------------------------------------------------------------------
   Function:   Get User Text
   Purpose:    This function reads the user text from the novolatile memory of
               the spectrometer.

   Input Parameters:
   ViSession vi:              Instrument Handle

   Output Parameters:
   ViString userText:         The user text read out from device
---------------------------------------------------------------------------*/
ViStatus _VI_FUNC tlccs_getUserText (ViSession vi, ViString userText);

#if defined(__cplusplus) || defined(__cplusplus__)
}
#endif

#endif  /* __TLCCS_H__ */

