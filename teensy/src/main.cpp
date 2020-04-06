#include "Arduino.h"

#ifdef USB_KEYBOARDONLY
int main (void) {
  pinMode(LED_BUILTIN, OUTPUT);
  elapsedMicros t0;
  elapsedMicros t1;
  t0 = 0;
  t1 = 0;
  constexpr uint32_t press_period = 200000; // press every 200ms
  constexpr uint32_t hold_time = 50000; // hold 50ms
  while(1) {
    while(t0 < press_period) {}
    t0 = 0;
    t1 = 0;
    Keyboard.set_key1(KEY_A);
    Keyboard.send_now();
    while (t1 < hold_time) {}
    Keyboard.set_key1(0);
    Keyboard.send_now();
    digitalWriteFast(LED_BUILTIN, !digitalReadFast(LED_BUILTIN));
  }
}
#endif

#ifdef USB_HID
int main(void) 
{
  pinMode(LED_BUILTIN, OUTPUT);
  elapsedMicros t0;
  t0 = 0;
  constexpr uint32_t move_period = 8000; // move every 8ms
  int32_t sign = 1;
  uint16_t counter = 0;
  while (1)
  {
      // busy wait until next move time
      while(t0 < move_period) {}
      t0 = 0;
      Mouse.move(sign, sign);
      sign = sign * -1;
      counter += 1;
      if (counter >= 100)
      {
          counter = 0;
          digitalWriteFast(LED_BUILTIN, !digitalReadFast(LED_BUILTIN));
      }
  }
}
#endif

#ifdef USB_RAWHID
int main (void) {
  pinMode(LED_BUILTIN, OUTPUT);
  elapsedMicros t0;
  t0 = 0;
  uint8_t buffer[64] = {0};
  constexpr uint32_t send_period = 1000; // micros until next message
  uint16_t counter2 = 0;
  while(1)
  {
    while (t0 < send_period) {}
    t0 = 0;
    RawHID.send(buffer, 0);
    buffer[0] = counter2;
    counter2 += 1;
    if (counter2 >= 256)
    {
      counter2 = 0;
    }
  }
}
#endif
