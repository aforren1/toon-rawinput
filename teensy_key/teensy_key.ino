
// Make sure to set the USB type!

int main (void) {
  pinMode(LED_BUILTIN, OUTPUT);
  elapsedMicros t0;
  elapsedMicros t1;
  t0 = 0;
  t1 = 0;
  constexpr uint32_t press_period = 250000; // press every 250ms
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
