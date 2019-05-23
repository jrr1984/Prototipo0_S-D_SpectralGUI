// DataRecorder.cpp : Defines the entry point for the console application.
//


#include <stdio.h>
#include <conio.h>
#include <windows.h>
#include "PI_GCS2_DLL.h"

int main()
{ 
	int ID;
	char szErrorMesage[1024];
	char szUsbController[1024];
	int	iError;
	BOOL bOK = TRUE;




	/////////////////////////////////////////
	// connect to the controller over USB. //
	/////////////////////////////////////////
	PI_EnumerateUSB(szUsbController, 1024, "PI E-727");
	ID = PI_ConnectUSB(szUsbController);
	if (ID<0)
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("ConnectUSB: ERROR %d: %s\n", iError, szErrorMesage);
		return(1);
	}
   


	/////////////////////////////////////////
	// Get the name of the connected axis. //
	/////////////////////////////////////////
	char szAxes[17];
	if (!PI_qSAI(ID, szAxes, 16))
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("SAI?: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">SAI?:\n%s\n", szAxes);

	// Use only the first axis.
	strcpy(szAxes, "1");



	/////////////////////////////////////////
	// close the servo loop (closed-loop). //
	/////////////////////////////////////////
	BOOL bFlags[3];

	// Switch on the Servo for all axes
	bFlags[0] = TRUE; // servo on for the axis in the string 'axes'.

	// call the SerVO mode command.
	if(!PI_SVO(ID, szAxes, bFlags))
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("SVO: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">SVO 1 1\n\n");



    ///////////////////////////////////////////
    // Write a sin wave to the wave table 1. //
    ///////////////////////////////////////////
	int iWaveTableIds[3];
	iWaveTableIds[0] = 1;
	if((bOK = PI_WAV_SIN_P(ID, iWaveTableIds[0], 1, 1000, 0, 500, 10, 0, 1000)) == FALSE)
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("WAV_SIN_P: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">WAV 1 X SIN_P 1000 10.0 0.0 1000 1 500\n\n");




    ////////////////////////////////////////
    // define the data recorder channels. //
    ////////////////////////////////////////
	
	// select the desired record channels to change.
	int iDataRecorderChannelIds[2];
	iDataRecorderChannelIds[0] = 1;
	
    // select the corresponding record source id's.
	char szDataRecorderChannelSources[] = "1";

	// select the corresponding record mode.
	int iDataRecorderOptions[] = {1};

	// Call the data recorder configuration command
	if((bOK = PI_DRC(ID, iDataRecorderChannelIds, szDataRecorderChannelSources, iDataRecorderOptions)) == FALSE)
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("DRC: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">DRC 1 1 1\n\n");


	
	// select the desired record channels to change.
	iDataRecorderChannelIds[0] = 2;
	
    // the corresponding record source id's remains the same.

	// select the corresponding record mode.
	iDataRecorderOptions[0] = 2;

	// Call the data recorder configuration command
	if((bOK = PI_DRC(ID, iDataRecorderChannelIds, szDataRecorderChannelSources, iDataRecorderOptions)) == FALSE)
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("DRC: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">DRC 2 2 1\n\n");




    ////////////////////////////
    // Select the wave table. //
    ////////////////////////////

    // select the desired wave table.
    iWaveTableIds[0] = 1;

    // select the desired wave generator.
	int iWaveGenerator[] = {1};


    // Call the wave selection command
    if (PI_WSL(ID, iWaveGenerator, iWaveTableIds, 1) == 0)
    {
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("WSL: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
    }
	printf(">WSL 1 1\n\n");



    /////////////////////////////////
    // start the wave generator 1. //
    /////////////////////////////////

    // select the desired wave generators to run (only wave generator 1 is used in this example).
    iWaveGenerator[0] = 1;

    // select the start mode for the corresponding wave generator.
	int iStatMode[] = {1};

	if((bOK = PI_WGO(ID, iWaveGenerator, iStatMode, 1)) == FALSE)
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("WGO: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">WGO 1 1\n\n");



    ///////////////////////////////////
    // start reading asynchronously. //
    ///////////////////////////////////

    // select the desired record channels to change.
	iDataRecorderChannelIds[0] = 1;
	iDataRecorderChannelIds[1] = 2;

	double* dDataTable;
	char szHeader[301];
	int iNReadChannels = 2;
	int iNReadValues = 1000;
	if((bOK = PI_qDRR(ID, iDataRecorderChannelIds, iNReadChannels, 1, iNReadValues, &dDataTable, szHeader, 300)) == FALSE)
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("DRR?: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">DRR? 100 1 1 2 3:\n%s\n", szHeader);



    /////////////////////////////////////////////////////////////
    // wait until the read pointer does not increase any more. //
    /////////////////////////////////////////////////////////////

	int iIndex = -1;
	int iOldIndex;
	do// wait until the read pointer does not increase any more
	{
		iOldIndex = iIndex;
		Sleep(100);
		iIndex = PI_GetAsyncBufferIndex(ID);
	}while(iOldIndex < iIndex);



    /////////////////////////////////////
    // read the values from the array. //
    /////////////////////////////////////

	int k;
	for(iIndex = 0; iIndex < (iOldIndex / iNReadChannels); iIndex++)
	{// print read data
	// the data columns 
	// c1_1 c2_1 c3_1 c4_1
	// c1_2 c2_2 c3_2 c4_2
	// ...
	// c1_n c2_n c3_n c4_n
	// are aligned as follows:
	// dDataTable:
	// {c1_1,c2_1,c3_1,c4_1,c1_2,c2_2,...,c4_n}

		printf("%03d", iIndex);

		for(k = 0; k < iNReadChannels; k++)
		  printf("\t%05.05f", dDataTable[(iIndex * iNReadChannels) + k]);

		printf("\n");  
	}
	

    /////////////////////////////////
    // stop the wave generator 1. //
    /////////////////////////////////

    // select the desired wave generators to run (only wave generator 1 is used in this example).
	iWaveGenerator[0] = 1;

    // select the start mode for the corresponding wave generator.
	iStatMode[0] = 0;

	if((bOK = PI_WGO(ID, iWaveGenerator, iStatMode, 1)) == FALSE)
	{
		iError = PI_GetError(ID);
		PI_TranslateError(iError, szErrorMesage, 1024);
		printf("WGO: ERROR %d: %s\n", iError, szErrorMesage);
		PI_CloseConnection(ID);
		return(1);
	}
	printf(">WGO 1 0\n\n");


	PI_CloseConnection(ID);

	if(bOK)
		printf("No Errors");
	
	getch();

	return 0;
}

