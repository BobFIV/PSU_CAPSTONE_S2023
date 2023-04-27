/*
 * Copyright (c) 2020 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
 */

#include <zephyr/kernel.h>

#include <app_event_manager.h>

#define MODULE main
#include "module_state_event.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(MODULE);

// Start test includes
#include <stdio.h>
#include <string.h>
#include <zephyr/types.h>
#include <zephyr/fs/fs.h>
#include <ff.h>

#include "module_state_event.h"
#include "fs_event.h"
#include "power_event.h"

#include <zephyr/logging/log.h>
#include <stdio.h>
#include <assert.h>

#include <fs_event.h>
#include <zephyr/fs/fs.h>
#define FILE_CONTENTS     file_contents
#define FILE_CONTENTS_LEN strlen(file_contents)
#define FILE_NAME         "TEST.TXT"
static const char file_contents[] = 
	"Test.\r\n"
	;
#define FATFS_MNTP	"/" CONFIG_MASS_STORAGE_DISK_NAME ":"

static FATFS fat_fs;

static struct fs_mount_t fatfs_mnt = {
	.type = FS_FATFS,
	.mnt_point = FATFS_MNTP,
	.fs_data = &fat_fs,
};
// End

#define USB_SERIALNUMBER_TEMPLATE "THINGY91_%04X%08X"

static uint8_t usb_serial_str[] = "THINGY91_12PLACEHLDRS";

/* Overriding weak function to set iSerialNumber at runtime. */
uint8_t *usb_update_sn_string_descriptor(void)
{
	snprintk(usb_serial_str, sizeof(usb_serial_str), USB_SERIALNUMBER_TEMPLATE,
				(uint32_t)(NRF_FICR->DEVICEADDR[1] & 0x0000FFFF)|0x0000C000,
				(uint32_t)NRF_FICR->DEVICEADDR[0]);

	return usb_serial_str;
}

/*int write_test_text() {
	int err;

	err = fs_mount(&fatfs_mnt);
	if (err) {
		LOG_ERR("fs_mount: %d", err);
		return false;
	}

	struct fs_file_t file;
	ssize_t bytes_written;
	char fname[128];

	
	err = snprintf(fname, sizeof(fname), "%s/%s", FATFS_MNTP, FILE_NAME);
	if (err <= 0 || err > sizeof(fname)) {
		return -ENOMEM;
	}

	fs_file_t_init(&file);
	err = fs_open(&file, fname, FS_O_CREATE | FS_O_RDWR);
	if (err) {
		return err;
	}

	err = fs_seek(&file, 0, FS_SEEK_END);
	if (err) {
		return err;
	}

	bytes_written = fs_write(&file, FILE_CONTENTS, FILE_CONTENTS_LEN);
	if (bytes_written != FILE_CONTENTS_LEN) {
		return -ENOMEM;
	}

	err = fs_close(&file);
	if (err) {
		return err;
	}
	
	err = fs_unmount(&fatfs_mnt);

	return 0;
}*/

void main(void)
{
	if (app_event_manager_init()) {
		LOG_ERR("Application Event Manager not initialized");
	} else {
		module_set_state(MODULE_STATE_READY);
	}
	
	//write_test_text();
}
