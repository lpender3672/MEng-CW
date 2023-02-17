#include "mbed.h"
#include "stdint.h" //This allow the use of integers of a known width
#define LM75_REG_TEMP (0x00) // Temperature Register
#define LM75_REG_CONF (0x01) // Configuration Register
#define LM75_ADDR     (0x90) // LM75 address

#define LM75_REG_TOS (0x03) // TOS Register
#define LM75_REG_THYST (0x02) // THYST Register



I2C i2c(I2C_SDA, I2C_SCL);

DigitalOut led1(LED1);
DigitalOut red(LED3);

InterruptIn lm75_int(D7); // Make sure you have the OS line connected to D7
Ticker reading_event;
Serial pc(SERIAL_TX, SERIAL_RX);

bool interrupted;
bool take_reading;
int16_t i16; // This variable needs to be 16 bits wide for the TOS and THYST conversion to work - can you see why?
int N = 60;
float *stored = (float *)malloc(sizeof(float) * N);


void temp_warning()
{
        interrupted = true;
        // The instruction below may create problems on the latest mbed compilers.
        // Avoid using printf in interrupts anyway as it takes too long to execute.
        // pc.printf("Interrupt triggered!\r\n");
}

void read_temp()
{
    take_reading = true;
}

int main()
{
        char data_write[3];
        char data_read[3];

        /* Configure the Temperature sensor device STLM75:
           - Thermostat mode Interrupt
           - Fault tolerance: 0
           - Interrupt mode means that the line will trigger when you exceed TOS and stay triggered until a register is read - see data sheet
        */
        data_write[0] = LM75_REG_CONF;
        data_write[1] = 0x02;
        int status = i2c.write(LM75_ADDR, data_write, 2, 0);
        if (status != 0)
        { // Error
                while (1)
                {
                        led1 = !led1;
                        wait(0.2);
                }
        }

        float tos=28; // TOS temperature
        float thyst=26; // THYST tempertuare

        // This section of code sets the TOS register
        data_write[0]=LM75_REG_TOS;
        i16 = (int16_t)(tos*256) & 0xFF80;
        data_write[1]=(i16 >> 8) & 0xff;
        data_write[2]=i16 & 0xff;
        i2c.write(LM75_ADDR, data_write, 3, 0);

        //This section of codes set the THYST register
        data_write[0]=LM75_REG_THYST;
        i16 = (int16_t)(thyst*256) & 0xFF80;
        data_write[1]=(i16 >> 8) & 0xff;
        data_write[2]=i16 & 0xff;
        i2c.write(LM75_ADDR, data_write, 3, 0);

        // This line attaches the interrupt.
        // The interrupt line is active low so we trigger on a falling edge
        lm75_int.fall(&temp_warning);
        reading_event.attach(&read_temp, 1.0);

        while (1)
        {
                if (take_reading)
                {
                    // Read temperature register
                    data_write[0] = LM75_REG_TEMP;
                    i2c.write(LM75_ADDR, data_write, 1, 1); // no stop
                    i2c.read(LM75_ADDR, data_read, 2, 0);

                    // Calculate temperature value in Celcius
                    int16_t i16 = (data_read[0] << 8) | data_read[1];
                    // Read data as twos complement integer so sign is correct
                    float temp = i16 / 256.0;

                    for (int i = 0; i < N - 1; i++) {
                        *(stored + i) = *(stored + i + 1);
                    }
                    *(stored + N - 1) = temp;
                    
                    //red = !red;
                    take_reading = false;
                }

                if (interrupted) {
                    // send data
                    for (int i=0; i < N; i++)
                    {
                        pc.printf("%.3f\r\n", *(stored + i));
                    }
                    // flash led
                    while (interrupted) {
                        red = !red;
                        wait(0.2);
                    }
                }
        }

}