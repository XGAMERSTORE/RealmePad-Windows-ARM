/** @file
  Minimal, non-destructive UEFI application for emulated ARM64 environments.
  This is NOT RMP6768 platform firmware and does not access tablet hardware.
**/
#include <Uefi.h>
#include <Library/UefiLib.h>
#include <Library/UefiBootServicesTableLib.h>

EFI_STATUS
EFIAPI
UefiMain (
  IN EFI_HANDLE ImageHandle,
  IN EFI_SYSTEM_TABLE *SystemTable
  )
{
  Print(L"RMP6768 research: ARM64 UEFI application launched.\r\n");
  Print(L"QEMU/EDK2 validation only; NOT compatible tablet firmware.\r\n");
  return EFI_SUCCESS;
}
