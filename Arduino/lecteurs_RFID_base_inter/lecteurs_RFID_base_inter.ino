// Using SeeedStudio GROVE RFID READER SEN11425P
// link between the computer and the SoftSerial Shield
//at 9600 bps 8-N-1
//Computer is connected to Hardware UART
//SoftSerial Shield is connected to the Software UART:D2&D3 

//link to catalog
//http://www.seeedstudio.com/wiki/Grove_-_125KHz_RFID_Reader
//link to datasheet
//http://www.seeedstudio.com/wiki/index.php?title=Electronic_brick_-_125Khz_RFID_Card_Reader#Block_Diagram
//
//http://www.priority1design.com.au/em4100_protocol.html

//ASTUCE: pour forcer une relecture alors que le TAG est toujours présent, couper puis remettre l'alim par le 0V
// (ne marche pas avec le +, peut être a cause d'une alim indirecte via UART ?)

//cablage du module RFID GROVE (SeedStudio)
//Arduino=>RFID
//Rouge=>5V
//Noir=>13
//Blanc=>3
//Jaune=>2


#include <SoftwareSerial.h>
#define START 0x02
#define END 0x03
#define TIMEOUT 180

enum STATES {VOID, PRESENT, CHECK };

SoftwareSerial SoftSerial(2, 3);
String ReceivedCode = "";
String LastCode="";
int count=0;     
int State=VOID;
bool Flag_ID=false;
bool Flag_absence=true;
bool Flag_presence=false;

void setup()
{
  SoftSerial.begin(9600);              
  Serial.begin(9600);             
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  pinMode(9, INPUT_PULLUP);
  State=CHECK;
  Flag_ID=false;
}
 
void loop()
{
  static int Tempo=0;
  static int Counter=0;
  char RecievedChar;
  delay(10); 
  
  switch(State)
  {
    case CHECK:
              digitalWrite(LED_BUILTIN, LOW); //alimente le module RFID
              if(Tempo<TIMEOUT) Tempo++;
              if(Tempo==TIMEOUT-1 and LastCode!="")
              {
                Serial.println("<VOID>");
                LastCode="";
                
                }
              if(Flag_ID) 
              {
                State=PRESENT;
                Tempo=0;
                Flag_ID=false;
                }
    break;
    
    case PRESENT:
              Tempo++;
              if (Tempo==1)
              {
              Flag_presence = false;
              Flag_absence = false;
              }
              else if (Tempo==5) Flag_presence = digitalRead(9)==LOW;
              else if (Tempo>7) Flag_absence = digitalRead(9)==HIGH;

              if (Flag_presence)
              {
                if(Flag_absence or Tempo>200)
                {
                  Tempo=0;
                  if (Flag_absence and LastCode!="")
                  {
                    Serial.println("<VOID>");
                    LastCode="";
                  }
                  digitalWrite(LED_BUILTIN, HIGH);
                  delay(100);
                  State=CHECK;
                  //Serial.println("<CHECK>");
                  }
                }
              else if (Tempo>15)
              {
                Tempo=0;
                digitalWrite(LED_BUILTIN, HIGH);
                delay(100);
                State=CHECK;
                //Serial.println("<CHECK>");
                }
                
    break; 
  }
  
  if (SoftSerial.available())             
  {
      RecievedChar=SoftSerial.read();  
      if(isprint(RecievedChar)) ReceivedCode+=RecievedChar; 
      if(RecievedChar==START) Counter=0;
      else Counter++;
      if(RecievedChar==END) 
        {
          ReceivedCode.remove(10, 2); // Remove 2 characters starting at index=10
          if(ReceivedCode != LastCode) 
          {
            Serial.print("<TAG:");
            Serial.print(ReceivedCode);
            Serial.println(">");
          }
          LastCode=ReceivedCode;
          ReceivedCode=""; 
          Flag_ID=true;
        }
  }
}
