## @file
# Minimal EDK2 platform description for an AARCH64 UEFI app.
# This does NOT initialize MediaTek hardware or produce device firmware.
[Defines]
  PLATFORM_NAME                  = RmpResearchHost
  PLATFORM_GUID                  = 4f42e938-247c-41fb-9f5a-a6409f98c012
  PLATFORM_VERSION               = 0.1
  DSC_SPECIFICATION              = 0x00010005
  OUTPUT_DIRECTORY               = Build/RmpResearchHost
  SUPPORTED_ARCHITECTURES        = AARCH64
  BUILD_TARGETS                  = DEBUG|RELEASE
  SKUID_IDENTIFIER               = DEFAULT

[LibraryClasses]
  BaseLib|MdePkg/Library/BaseLib/BaseLib.inf
  BaseMemoryLib|MdePkg/Library/BaseMemoryLib/BaseMemoryLib.inf
  DebugLib|MdePkg/Library/BaseDebugLibNull/BaseDebugLibNull.inf
  MemoryAllocationLib|MdePkg/Library/UefiMemoryAllocationLib/UefiMemoryAllocationLib.inf
  PcdLib|MdePkg/Library/BasePcdLibNull/BasePcdLibNull.inf
  PrintLib|MdePkg/Library/BasePrintLib/BasePrintLib.inf
  # Host-only diagnostic build: use EDK2's default null stack-check instance.
  StackCheckLib|MdePkg/Library/StackCheckLibNull/StackCheckLibNull.inf
  UefiApplicationEntryPoint|MdePkg/Library/UefiApplicationEntryPoint/UefiApplicationEntryPoint.inf
  UefiBootServicesTableLib|MdePkg/Library/UefiBootServicesTableLib/UefiBootServicesTableLib.inf
  DevicePathLib|MdePkg/Library/UefiDevicePathLib/UefiDevicePathLib.inf
  UefiLib|MdePkg/Library/UefiLib/UefiLib.inf
  UefiRuntimeServicesTableLib|MdePkg/Library/UefiRuntimeServicesTableLib/UefiRuntimeServicesTableLib.inf

# Disable GCC link-time optimization for this host-only diagnostic build.
# GCC 13 LTO can synthesize an unresolved libc memcpy in EDK2 BasePrintLib;
# the previous loop-pattern flag alone did not prevent it (CI 43531258022).
# This does not change any tablet bootchain or authorize flashing.
[BuildOptions]
  GCC:*_*_AARCH64_CC_FLAGS = -fno-lto -fno-tree-loop-distribute-patterns

[Components]
  uefi/RmpResearchApp/RmpResearchApp.inf
