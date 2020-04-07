To run (not upload), `pio run -e [keyboard/mouse/rawhid]`

To upload, include `-t upload`.

Notes:
 - We do the `int main(void) {...}` rather than the `setup/loop` because we don't need to call `yield`, as far as I can tell-- it seems to just get serial events (which we don't use in this context). It might be a little clearer to non-Arduino folks, too? One (minor) disadvantage is that it's a relatively new construct for the Teensy 4 (https://github.com/PaulStoffregen/cores/pull/397).
 - Look at https://github.com/luni64/TeensyTimerTool for timing vs busy waiting on `elapsedMicros`? Nicer interface, though need to sanity check perf: https://forum.pjrc.com/threads/59112-TeensyTimerTool

