#pragma once
#include <malloc.h>
#include <pspkernel.h>
#include <pspctrl.h>
#include <psputility.h>
#include <string.h>
#define RAM_BLOCK      (1024 * 1024)

/**
* Gets the maximum available ram in bytes
*/
u32 ramAvailableMax(void);
/**
* Gets the current free ram in bytes
*/
u32 freeMemory(void);