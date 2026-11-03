/** @file
  Read-only ARM64 UEFI environment probe. Runs under an existing UEFI firmware.
  NOT a MediaTek bootloader, Windows driver, or tablet firmware.
**/
#include <Uefi.h>
#include <Library/UefiLib.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/MemoryAllocationLib.h>
#include <Guid/Acpi.h>

EFI_STATUS
EFIAPI
UefiMain (
  IN EFI_HANDLE ImageHandle,
  IN EFI_SYSTEM_TABLE *SystemTable
  )
{
  EFI_STATUS Status;
  UINTN MapSize = 0;
  UINTN MapKey = 0;
  UINTN DescriptorSize = 0;
  UINT32 DescriptorVersion = 0;
  EFI_MEMORY_DESCRIPTOR *Map = NULL;

  Print(L"RMP6768 research: UEFI environment probe (READ ONLY)\r\n");
  Print(L"Firmware vendor: %s\r\n", SystemTable->FirmwareVendor);
  Print(L"Firmware revision: 0x%x\r\n", SystemTable->FirmwareRevision);
  Print(L"UEFI revision: 0x%x\r\n", SystemTable->Hdr.Revision);

  Status = gBS->GetMemoryMap(&MapSize, Map, &MapKey,
                              &DescriptorSize, &DescriptorVersion);
  if (Status != EFI_BUFFER_TOO_SMALL || MapSize == 0) {
    Print(L"GetMemoryMap sizing failed: %r\r\n", Status);
    return EFI_DEVICE_ERROR;
  }

  // Firmware may add descriptors when allocating; leave headroom.
  MapSize += 2 * sizeof(EFI_MEMORY_DESCRIPTOR) + 2 * DescriptorSize;
  Map = AllocatePool(MapSize);
  if (Map == NULL) {
    Print(L"Memory allocation failed\r\n");
    return EFI_OUT_OF_RESOURCES;
  }
  Status = gBS->GetMemoryMap(&MapSize, Map, &MapKey,
                              &DescriptorSize, &DescriptorVersion);
  if (!EFI_ERROR(Status) && DescriptorSize != 0) {
    Print(L"Memory descriptors: %u, descriptor version: %u\r\n",
          (UINT32)(MapSize / DescriptorSize), DescriptorVersion);
  } else {
    Print(L"GetMemoryMap failed: %r\r\n", Status);
  }
  FreePool(Map);
  {
    UINTN Index;
    BOOLEAN HasAcpi20 = FALSE;
    BOOLEAN HasAcpi10 = FALSE;
    for (Index = 0; Index < SystemTable->NumberOfTableEntries; ++Index) {
      EFI_CONFIGURATION_TABLE *Entry = &SystemTable->ConfigurationTable[Index];
      if (CompareGuid(&Entry->VendorGuid, &gEfiAcpi20TableGuid)) {
        HasAcpi20 = TRUE;
      }
      if (CompareGuid(&Entry->VendorGuid, &gEfiAcpi10TableGuid)) {
        HasAcpi10 = TRUE;
      }
    }
    Print(L"ACPI 2.0+ table pointer present: %s\\r\\n", HasAcpi20 ? L"yes" : L"no");
    Print(L"ACPI 1.0 table pointer present: %s\\r\\n", HasAcpi10 ? L"yes" : L"no");
    Print(L"ACPI presence does NOT imply Windows driver compatibility.\\r\\n");
  }
  Print(L"No storage writes or firmware changes performed.\\r\\n");
  Print(L"This does NOT initialize Helio G80 hardware.\r\n");
  return Status;
}
