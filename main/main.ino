
int motor1speed = 3;
int motor1A = 4;
int motor1B = 5;
int motor2A = 6;
int motor2B = 7;

void motor1forward() {
        digitalWrite(motor1A, LOW);
        digitalWrite(motor1B, HIGH);
}

void motor1back() {
        digitalWrite(motor1A, HIGH);
        digitalWrite(motor1B, LOW);
}

void motor1off() {
        digitalWrite(motor1A, LOW);
        digitalWrite(motor1B, LOW);
}

void brushon() {
        digitalWrite(motor2A, LOW);
        digitalWrite(motor2B, HIGH);
}

void brushoff() {
        digitalWrite(motor2A, LOW);
        digitalWrite(motor2B, LOW);
}

void setup() {
        Serial.begin(9600);
        pinMode(motor1speed, OUTPUT);
        pinMode(motor1A, OUTPUT);
        pinMode(motor1B, OUTPUT);
        pinMode(motor2A, OUTPUT);
        pinMode(motor2B, OUTPUT);
        
        // turn on move motor
        motor1forward();
        // turn on brush
        brushon();

        delay(3);

        // turn all off 
        motor1off();
        brushoff();
        delay(1);

        // move back
        motor1back();
        delay(3);

        //all off
        motor1off();
}


void loop() {
}