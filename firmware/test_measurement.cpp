#include "RiceSapFlow/measurement.h"
#include <assert.h>
#include <stdio.h>
static void baseline(Measurement &m,uint32_t start=0) {
  for(unsigned i=0;i<30;++i) assert(m.sample(start+i*100,25,25.01f));
}
int main() {
  Measurement m; assert(!m.heat && !m.armed); assert(!m.start(0,200));
  baseline(m); assert(m.arm(2900)); assert(!m.start(2900,3001)); assert(m.start(2900,200));
  m.tick(3099); assert(m.heat); m.tick(3100); assert(!m.heat && m.phase==Measurement::OBSERVING);
  m.sample(3200,25.1,25.2); assert(m.ratio()>1);
  m.tick(3551); assert(m.phase==Measurement::FAULT && !m.heat);
  m.reset(); baseline(m,4000); assert(m.arm(6900)); assert(!m.start(6900,200));
  m.cancel(); baseline(m,130000); assert(m.arm(132900)); assert(m.start(132900,3000));
  m.sample(133000,27.1,25); assert(m.phase==Measurement::FAULT && !m.heat);
  Measurement hot; baseline(hot); assert(!hot.sample(3000,40.1,25)); assert(!hot.arm(3000));
  Measurement rollover; baseline(rollover,UINT32_MAX-1000);
  uint32_t n=uint32_t(UINT32_MAX-1000+2900); assert(rollover.arm(n)); assert(rollover.start(n,200));
  rollover.tick(n+200); assert(!rollover.heat);
  Measurement unstable; for(int i=0;i<30;++i)unstable.sample(i*100,i%2?25.2f:25,25);
  assert(!unstable.arm(2900));
  Measurement expired; baseline(expired); assert(expired.arm(2900));
  expired.sample(63001,25,25); assert(!expired.start(63001,200));
  expired.tick(63001); assert(!expired.armed && !expired.heat);
  Measurement invalid; baseline(invalid); assert(invalid.arm(2900));
  assert(!invalid.start(2900,99)); assert(!invalid.start(2900,0));
  assert(!invalid.sample(3000,NAN,25)); assert(!invalid.heat && !invalid.armed);
  Measurement completed; baseline(completed); assert(completed.arm(2900));
  assert(completed.start(2900,100));
  for (uint32_t t=3000;t<=92900;t+=100){completed.sample(t,25,25);completed.tick(t);}
  assert(completed.phase==Measurement::IDLE && !completed.heat);
  puts("PASS: boot off, arming, duration, exact cutoff, stale sensor, cooldown, thermal fault, millis wrap and baseline stability");
}
