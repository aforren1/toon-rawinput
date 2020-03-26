int main (void) {
  pinMode(LED_BUILTIN, OUTPUT);
  elapsedMicros t0;
  t0 = 0;
  uint8_t buffer[64] = {0};
  constexpr uint32_t send_period = 1000; // micros until next message
  uint16_t counter1 = 0;
  uint16_t counter2 = 0;
  while(1)
  {
    while (t0 < send_period) {}
    t0 = 0;
    RawHID.send(buffer, 0);
    buffer[counter1] = counter2;
    counter2 += 1;
    if (counter2 >= 256)
    {
      counter2 = 0;
      counter1 += 1;
    }    
    if (counter1 >= 64)
    {
      counter1 = 0;
      memset(buffer, 0, sizeof(buffer));
    }
  }
}
