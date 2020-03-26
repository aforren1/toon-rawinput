// Make sure to set the USB type!

int main (void) {
  pinMode(LED_BUILTIN, OUTPUT);
  elapsedMicros t0;
  t0 = 0;
  constexpr uint32_t move_period = 8000; // move every 8ms
  uint32_t counter = 0;
  int16_t sign = 1;
  while(1) {
    while(t0 < move_period) {}
    t0 = 0;
    counter += 1;
    Mouse.move(sign * 1, sign * 1);
    if (counter >= 25)
    {
      counter = 0;
      sign *= -1;
      digitalWriteFast(LED_BUILTIN, !digitalReadFast(LED_BUILTIN));
    }
  }
}
