// Definição dos pinos dos motores
int IN1 = 6;
int IN2 = 7;

int FIM_DE_CURSO_SUPERIOR = 5;
int FIM_DE_CURSO_INFERIOR = 3;

void setup() {
  Serial.begin(9600);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(FIM_DE_CURSO_SUPERIOR, INPUT_PULLUP);
  pinMode(FIM_DE_CURSO_INFERIOR, INPUT_PULLUP); 

}

void loop() {
  
  bool fimDeCursoSuperiorAtivado = digitalRead(FIM_DE_CURSO_SUPERIOR);
  bool fimDeCursoInferiorAtivado = digitalRead(FIM_DE_CURSO_INFERIOR);

 
  if (Serial.available() > 0) {
    
    char comando = Serial.read();

    
    switch (comando) {
      case 'U': 

        if(fimDeCursoSuperiorAtivado == 0)
        {
         
          digitalWrite(IN1, LOW);
          digitalWrite(IN2, LOW);
        }
        else
        {
          digitalWrite(IN1, LOW);
          digitalWrite(IN2, HIGH);
          }
       
        break;

      case 'D':

        if(fimDeCursoInferiorAtivado == 0)
        {
          digitalWrite(IN1, LOW);
          digitalWrite(IN2, LOW);
        }

        else
        {
          digitalWrite(IN1, HIGH);
          digitalWrite(IN2, LOW);
        }
          
        break;

      case 'H': 
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        break;

      default:
        // Caso não reconheça o comando, não faz nada
        break;
    }
  }
}
