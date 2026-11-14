/** @file
  Freestanding memory-copy fallback for the host-only EDK2 diagnostic app.

  GCC 13 LTO may emit a libc-style memcpy call while optimizing BasePrintLib.
  EDK2 firmware builds do not link libc. Volatile byte stores deliberately
  prevent the compiler from lowering this loop back into memcpy.
  This is not a bootloader, hardware initialization, or flashing support.
**/
#include <Base.h>

VOID *
memcpy (
  VOID       *Destination,
  CONST VOID *Source,
  UINTN      Length
  )
{
  volatile UINT8 *Dst = (volatile UINT8 *)Destination;
  CONST volatile UINT8 *Src = (CONST volatile UINT8 *)Source;
  UINTN Index;

  for (Index = 0; Index < Length; ++Index) {
    Dst[Index] = Src[Index];
  }

  return Destination;
}
