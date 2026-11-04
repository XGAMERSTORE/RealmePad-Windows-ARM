/** @file
  ARM64 UEFI Windows Boot Manager chainloader.

  Runs only AFTER compatible UEFI firmware has initialized the device.
  It does not implement MediaTek boot ROM handoff, memory training,
  storage drivers, or a UEFI firmware port for Realme Pad.
**/
#include <Uefi.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/UefiLib.h>
#include <Library/DevicePathLib.h>
#include <Library/MemoryAllocationLib.h>
#include <Protocol/LoadedImage.h>
#include <Protocol/SimpleFileSystem.h>
#include <Guid/FileInfo.h>

EFI_STATUS EFIAPI UefiMain(IN EFI_HANDLE ImageHandle, IN EFI_SYSTEM_TABLE *SystemTable) {
  EFI_STATUS Status;
  EFI_LOADED_IMAGE_PROTOCOL *Loaded = NULL;
  EFI_HANDLE Child = NULL;
  EFI_DEVICE_PATH_PROTOCOL *Path = NULL;
  EFI_HANDLE Device;
  // The standard Windows ARM64 removable-media loader path.
  CONST CHAR16 *WindowsLoader = L"\\EFI\\BOOT\\BOOTAA64.EFI";

  Status = gBS->HandleProtocol(ImageHandle, &gEfiLoadedImageProtocolGuid, (VOID **)&Loaded);
  if (EFI_ERROR(Status) || Loaded == NULL) {
    Print(L"Cannot identify current EFI image: %r\n", Status);
    return EFI_NOT_FOUND;
  }
  Device = Loaded->DeviceHandle;
  Path = FileDevicePath(Device, (CHAR16 *)WindowsLoader);
  if (Path == NULL) {
    Print(L"Cannot construct Windows EFI device path.\n");
    return EFI_OUT_OF_RESOURCES;
  }
  Status = gBS->LoadImage(FALSE, ImageHandle, Path, NULL, 0, &Child);
  FreePool(Path);
  if (EFI_ERROR(Status)) {
    Print(L"Windows ARM64 boot loader not found or invalid: %r\n", Status);
    return Status;
  }
  Print(L"Starting Windows ARM64 boot manager...\n");
  Status = gBS->StartImage(Child, NULL, NULL);
  if (EFI_ERROR(Status)) {
    Print(L"Windows boot manager returned an error: %r\n", Status);
  }
  return Status;
}
