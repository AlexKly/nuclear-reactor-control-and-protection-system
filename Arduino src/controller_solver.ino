// Assignments ports:
#define TBS6600_ENA         10
#define TBD6600_DIR         9
#define TBS6600_PUL         8
// Sync bytes:
#define SYNC_BYTE_RECEIVE   0xAA
#define SYNC_BYTE_TRANSMITE 0x55
#define TYPE_SIZE           4
// States of FM:
#define IDLE_START_BYTE     0
#define RECEIVE_DATA        1

// Global vars:
int statesFSM = 0;
int cntBytes  = 0;
bool motor_direction = true;
//bool motor_enable = true;
bool motor_enable = false;
bool motor_step = false;
int cnt = 0;

void setup() {
  // UART initialization:
  Serial.begin(115200);   // Opens serial port, sets data rate to 115200 bps
  // Initialization ports:
  pinMode(TBS6600_ENA, OUTPUT);
  pinMode(TBD6600_DIR, OUTPUT);
  pinMode(TBS6600_PUL, OUTPUT);
}

union {
  byte hexByte[TYPE_SIZE];
  float floatingPoint;
} binaryFloatingInput;

union {
   byte hexByte[TYPE_SIZE];
   float floatingPoint;
} binaryFloatingOutput;

void loop() {
  // Motor clock:
  cnt = cnt + 1;
  if (cnt > 25) {
    motor_step = !motor_step;
    cnt = 0;
  }
  moveMotor(motor_direction, motor_enable, motor_step);
  if (Serial.available() > 0) {
    switch(statesFSM) {
      case IDLE_START_BYTE:
        if (Serial.read() == SYNC_BYTE_RECEIVE) {
          Serial.write(SYNC_BYTE_TRANSMITE);
          statesFSM = RECEIVE_DATA;
        }
        break;
      case RECEIVE_DATA:
        binaryFloatingInput.hexByte[cntBytes] = Serial.read();
        
        Serial.write(binaryFloatingOutput.hexByte[cntBytes]);
        cntBytes++;
        if (cntBytes == TYPE_SIZE) {
          //motor_enable
          cntBytes = 0;
          binaryFloatingOutput.floatingPoint = binaryFloatingInput.floatingPoint;

          // Logic of processing step motor:
          if (binaryFloatingInput.floatingPoint == 1) {
            motor_enable = true;
            motor_direction = true;
          }
          else if (binaryFloatingInput.floatingPoint == -1) {
            motor_enable = true;
            motor_direction = false;
          }
          else {
            motor_enable = false;
          }
          
          statesFSM = IDLE_START_BYTE;
        }
        break;
      default:
        statesFSM = IDLE_START_BYTE;
        break;
    }
  }
}

// Start move step-motor:
void moveMotor(bool motor_dir, bool motor_enable, bool motor_step) {
  if (motor_dir)
    digitalWrite(TBD6600_DIR, HIGH);
  else
    digitalWrite(TBD6600_DIR, LOW);
  
  if (motor_enable) {
    digitalWrite(TBS6600_ENA, LOW);
    if (motor_step)
      digitalWrite(TBS6600_PUL, HIGH);
    else
      digitalWrite(TBS6600_PUL, LOW);
  }
  else {
    digitalWrite(TBS6600_ENA, HIGH);
    digitalWrite(TBS6600_PUL, LOW);
  }
}
