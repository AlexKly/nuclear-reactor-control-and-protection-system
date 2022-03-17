// Assignments ports:
#define TBS6600_ENA  10
#define TBD6600_DIR  9
#define TBS6600_PUL  8

// Global vars:
bool motor_direction = true;
bool motor_enable = true;
bool motor_step = false;
int cnt = 0;

void setup() {
  // Initialization ports:
  pinMode(TBS6600_ENA, OUTPUT);
  pinMode(TBD6600_DIR, OUTPUT);
  pinMode(TBS6600_PUL, OUTPUT);
}

void loop() {
  moveMotor(motor_direction, motor_enable, motor_step);
  delay(1);
  motor_step = !motor_step;
  //cnt += 1;
  //if (cnt > 500) {
  //  cnt = 0;
  //  motor_direction = !motor_direction;
  //} 
}

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


