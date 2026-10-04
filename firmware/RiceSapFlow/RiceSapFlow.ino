#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <WebServer.h>
#include <esp_timer.h>
#include <esp_random.h>
#include <driver/gpio.h>
#include "measurement.h"

// Matches existing header networks on a standard SuperMini pinout:
// J2.4 = GPIO4 (SDA), J2.5 = GPIO3 (SCL), J2.7 = GPIO1 (heater).
// The actual module variant must be checked before arming the prototype.
constexpr int PIN_SDA = 4, PIN_SCL = 3, PIN_HEATER = 1;
constexpr uint8_t SENSOR_UP = 0x48, SENSOR_DOWN = 0x49;
constexpr uint16_t REG_TEMP = 0, REG_CONFIG = 1, REG_ID = 0x0F;
constexpr uint16_t CFG_SHUTDOWN = 0x0400, CFG_ONE_SHOT = 0x0C00;
constexpr uint16_t DATA_READY = 0x2000;
constexpr unsigned LOG_SIZE = 1200;
Measurement measurement;
WebServer server(80);
esp_timer_handle_t offTimer = nullptr;
volatile bool timerExpired = false;
portMUX_TYPE heaterMux = portMUX_INITIALIZER_UNLOCKED;
bool converting = false, readyUp = false, readyDown = false;
uint32_t conversionStart = 0, nextConversion = 0;
String accessPassword;
struct Record { uint32_t time, pulse; float up, down, riseUp, riseDown; uint8_t phase; };
Record records[LOG_SIZE];
unsigned recordCount = 0, recordNext = 0;

void timerOff(void *) {
  portENTER_CRITICAL(&heaterMux);
  gpio_set_level(static_cast<gpio_num_t>(PIN_HEATER), 0);
  timerExpired = true;
  portEXIT_CRITICAL(&heaterMux);
}
void heaterOff() {
  gpio_set_level(static_cast<gpio_num_t>(PIN_HEATER), 0);
  if (offTimer) esp_timer_stop(offTimer);
}
bool writeReg(uint8_t address, uint8_t reg, uint16_t value) {
  Wire.beginTransmission(address); Wire.write(reg);
  Wire.write(uint8_t(value >> 8)); Wire.write(uint8_t(value));
  return Wire.endTransmission() == 0;
}
bool readReg(uint8_t address, uint8_t reg, uint16_t &value) {
  Wire.beginTransmission(address); Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(address, uint8_t(2)) != 2) return false;
  value = (uint16_t(Wire.read()) << 8) | uint8_t(Wire.read()); return true;
}
void fail(const char *reason) { heaterOff(); measurement.trip(reason); converting = false; }
bool identifySensors() {
  heaterOff();
  for (uint8_t a : {SENSOR_UP, SENSOR_DOWN}) {
    uint16_t id = 0;
    if (!readReg(a, REG_ID, id) || (id & 0x0FFF) != 0x0117 ||
        !writeReg(a, REG_CONFIG, CFG_SHUTDOWN)) return false;
  }
  return true;
}
void logSample(uint32_t now) {
  records[recordNext] = {now, measurement.everPulsed ? measurement.pulseStartMs : 0,
    measurement.up, measurement.down, measurement.riseUp(), measurement.riseDown(),
    uint8_t(measurement.phase)};
  recordNext = (recordNext + 1) % LOG_SIZE;
  if (recordCount < LOG_SIZE) ++recordCount;
  Serial.printf("%lu,%.5f,%.5f,%s,%.5f,%.5f\n", (unsigned long)now,
    measurement.up, measurement.down, measurement.phaseName(),
    measurement.riseUp(), measurement.riseDown());
}
void acquire(uint32_t now) {
  if (measurement.phase == Measurement::FAULT) return;
  if (!converting && int32_t(now - nextConversion) >= 0) {
    if (!writeReg(SENSOR_UP, REG_CONFIG, CFG_ONE_SHOT) ||
        !writeReg(SENSOR_DOWN, REG_CONFIG, CFG_ONE_SHOT)) { fail("i2c_start_failed"); return; }
    converting = true; readyUp = readyDown = false; conversionStart = now;
    nextConversion = now + 100;
  }
  if (!converting || uint32_t(now - conversionStart) < 20) return;
  uint16_t cfg = 0;
  if (!readyUp) {
    if (!readReg(SENSOR_UP, REG_CONFIG, cfg)) { fail("up_sensor_missing"); return; }
    readyUp = (cfg & DATA_READY) != 0;
  }
  if (!readyDown) {
    if (!readReg(SENSOR_DOWN, REG_CONFIG, cfg)) { fail("down_sensor_missing"); return; }
    readyDown = (cfg & DATA_READY) != 0;
  }
  if (readyUp && readyDown) {
    uint16_t u, d;
    if (!readReg(SENSOR_UP, REG_TEMP, u) || !readReg(SENSOR_DOWN, REG_TEMP, d)) {
      fail("temperature_read_failed"); return;
    }
    converting = false;
    if (!measurement.sample(now, int16_t(u) / 128.0f, int16_t(d) / 128.0f)) {
      heaterOff(); return;
    }
    logSample(now);
  } else if (uint32_t(now - conversionStart) > 150) fail("conversion_timeout");
}
bool authenticate() {
  if (server.authenticate("admin", accessPassword.c_str())) return true;
  server.requestAuthentication(); return false;
}
String numberOrNull(float value) { return isfinite(value) ? String(value, 5) : "null"; }
void status() {
  if (!authenticate()) return;
  String j = "{\"phase\":\"" + String(measurement.phaseName()) + "\",\"armed\":";
  j += measurement.armed ? "true" : "false";
  j += ",\"valid\":"; j += measurement.fresh(millis()) ? "true" : "false";
  j += ",\"up_c\":" + numberOrNull(measurement.up);
  j += ",\"down_c\":" + numberOrNull(measurement.down);
  j += ",\"rise_up_c\":" + numberOrNull(measurement.riseUp());
  j += ",\"rise_down_c\":" + numberOrNull(measurement.riseDown());
  j += ",\"heat_ratio\":" + numberOrNull(measurement.ratio());
  j += ",\"sap_flow\":null,\"calibrated\":false,\"heater_nominal_v\":3.0";
  j += ",\"fault\":\"" + String(measurement.fault) + "\"}";
  server.send(200, "application/json", j);
}
const char PAGE[] PROGMEM = R"HTML(<!doctype html><html lang="zh"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>水稻热脉冲测量</title>
<style>body{font:16px system-ui;max-width:760px;margin:30px auto;padding:16px;color:#18352b;background:#f5faf7}button,input{font:inherit;padding:10px;margin:6px}pre{white-space:pre-wrap}canvas{width:100%;background:white;border:1px solid #bed3c8}</style>
<h1>水稻热脉冲测量</h1><p>双温度采集与加热响应记录。茎流量需要实物标定后计算。</p>
<p id="state">正在读取</p><canvas id="plot" width="700" height="220"></canvas>
<p><label><input id="checked" type="checkbox">已核对模块针脚、3.0V 输出和探针连接</label></p>
<button onclick="arm()">准备一次加热</button><label>脉冲毫秒<input id="duration" type="number" min="100" max="3000" value="200"></label>
<button onclick="pulse()">开始记录与加热</button><button onclick="action('stop')">关断</button>
<button onclick="action('reset')">重新检测传感器</button><a href="/data.csv">下载最近温度记录</a><pre id="msg"></pre>
<script>const history=[];async function action(p,data={}){try{const r=await fetch('/api/'+p,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data)});document.getElementById('msg').textContent=await r.text()}catch(e){document.getElementById('msg').textContent='连接中断；加热由设备定时关断'}}
function arm(){if(!document.getElementById('checked').checked){document.getElementById('msg').textContent='请先完成接线检查';return}action('arm',{confirm:1})}
function pulse(){action('pulse',{ms:document.getElementById('duration').value})}
function draw(){const c=document.getElementById('plot'),ctx=c.getContext('2d');ctx.clearRect(0,0,700,220);if(!history.length)return;const vals=history.flat();let lo=Math.min(...vals)-.1,hi=Math.max(...vals)+.1;ctx.fillStyle='#18352b';ctx.fillText(lo.toFixed(2)+' 至 '+hi.toFixed(2)+' ℃',10,15);['#167d59','#bd642e'].forEach((color,j)=>{ctx.strokeStyle=color;ctx.beginPath();history.forEach((v,i)=>{let x=20+i*660/Math.max(1,history.length-1),y=200-(v[j]-lo)*170/(hi-lo);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke()})}
setInterval(async()=>{try{const r=await fetch('/api/status');if(!r.ok)return;const s=await r.json();document.getElementById('state').textContent=`状态：${s.phase}；上游 ${s.up_c??'--'} ℃；下游 ${s.down_c??'--'} ℃；故障：${s.fault||'无'}`;if(s.valid){history.push([s.up_c,s.down_c]);if(history.length>120)history.shift();draw()}}catch(e){document.getElementById('state').textContent='连接中断'}},1000);</script></html>)HTML";
void csv() {
  if (!authenticate()) return;
  if (measurement.phase == Measurement::HEATING || measurement.phase == Measurement::OBSERVING) {
    server.send(409,"text/plain","Wait until measurement ends; serial logging remains available"); return;
  }
  server.setContentLength(CONTENT_LENGTH_UNKNOWN);
  server.sendHeader("Content-Disposition", "attachment; filename=temperature.csv");
  server.send(200, "text/csv", "");
  server.sendContent("time_ms,pulse_start_ms,up_c,down_c,rise_up_c,rise_down_c,phase\n");
  unsigned start = (recordNext + LOG_SIZE - recordCount) % LOG_SIZE;
  for (unsigned i = 0; i < recordCount; ++i) {
    const Record &r = records[(start + i) % LOG_SIZE]; char line[170];
    snprintf(line, sizeof(line), "%lu,%lu,%.5f,%.5f,%.5f,%.5f,%u\n", (unsigned long)r.time,
      (unsigned long)r.pulse,r.up,r.down,r.riseUp,r.riseDown,unsigned(r.phase));
    server.sendContent(line);
    if (i % 10 == 0) yield();
  }
  server.sendContent("");
}
void setup() {
  pinMode(PIN_HEATER, OUTPUT); digitalWrite(PIN_HEATER, LOW);
  Serial.begin(115200);
  esp_timer_create_args_t args = {}; args.callback = timerOff; args.name = "heater-off";
  if (esp_timer_create(&args, &offTimer) != ESP_OK) measurement.trip("heater_timer_failed");
  Wire.begin(PIN_SDA, PIN_SCL, 100000); Wire.setTimeOut(25);
  if (measurement.phase != Measurement::FAULT && !identifySensors()) fail("tmp117_identity_failed");
  char password[17]; snprintf(password,sizeof(password),"%08lx%08lx",(unsigned long)esp_random(),(unsigned long)esp_random());
  accessPassword = password;
  WiFi.mode(WIFI_AP); String ssid = "RiceSapFlow-" + WiFi.macAddress().substring(12); ssid.replace(":", "");
  WiFi.softAP(ssid.c_str(), accessPassword.c_str());
  Serial.printf("AP: %s\nPassword: %s\nBrowser: http://192.168.4.1 user=admin\n", ssid.c_str(),accessPassword.c_str());
  Serial.println("time_ms,up_c,down_c,phase,rise_up_c,rise_down_c");
  server.on("/",HTTP_GET,[]{if(authenticate())server.send_P(200,"text/html",PAGE);});
  server.on("/api/status",HTTP_GET,status);
  server.on("/data.csv",HTTP_GET,csv);
  server.on("/api/arm",HTTP_POST,[]{
    if (!authenticate()) return;
    bool ok=server.arg("confirm")=="1" && measurement.arm(millis());
    server.send(ok?200:409,"text/plain",ok?"已准备一次加热":"需要新鲜、稳定的双温度读数和接线确认");
  });
  server.on("/api/pulse",HTTP_POST,[]{
    if (!authenticate()) return;
    String ms=server.arg("ms"); bool numeric=ms.length()>0 && ms.length()<=4;
    for(unsigned i=0;i<ms.length();++i)numeric=numeric && isDigit(ms[i]);
    uint32_t duration=numeric?uint32_t(ms.toInt()):0;
    if (!offTimer || !measurement.start(millis(),duration)) {server.send(409,"text/plain","尚未准备、脉冲长度无效或冷却时间不足");return;}
    timerExpired=false;
    if (esp_timer_start_once(offTimer,uint64_t(duration)*1000)!=ESP_OK) {fail("timer_start_failed");server.send(500,"text/plain","定时器故障，已关断");return;}
    // The timer may expire if this task is delayed after starting it. Serialize
    // enabling with its callback so an expired pulse cannot turn back on.
    portENTER_CRITICAL(&heaterMux);
    bool expiredBeforeEnable = timerExpired;
    if (!expiredBeforeEnable) gpio_set_level(static_cast<gpio_num_t>(PIN_HEATER),1);
    portEXIT_CRITICAL(&heaterMux);
    if (expiredBeforeEnable) {fail("timer_deadline_missed");server.send(409,"text/plain","加热时限已过，保持关断");return;}
    server.send(200,"text/plain","开始记录加热响应");
  });
  server.on("/api/stop",HTTP_POST,[]{if(authenticate()){heaterOff();measurement.cancel();server.send(200,"text/plain","已关断");}});
  server.on("/api/reset",HTTP_POST,[]{
    if(!authenticate())return; heaterOff();
    if(measurement.phase==Measurement::HEATING || measurement.phase==Measurement::OBSERVING){measurement.cancel();}
    bool ok=offTimer && identifySensors(); measurement.reset(); converting=false; nextConversion=millis();
    if(!ok)fail("tmp117_identity_failed");server.send(ok?200:409,"text/plain",ok?"传感器已重新检测；加热保持关闭":"检测失败；加热保持关闭");
  });
  server.begin();
}
void loop() {
  uint32_t now=millis();
  measurement.tick(now);
  if(timerExpired && measurement.phase==Measurement::HEATING){measurement.heat=false;measurement.phase=Measurement::OBSERVING;measurement.observedMs=now;}
  if(!measurement.heat)gpio_set_level(static_cast<gpio_num_t>(PIN_HEATER),0);
  acquire(now); server.handleClient(); delay(2);
}
