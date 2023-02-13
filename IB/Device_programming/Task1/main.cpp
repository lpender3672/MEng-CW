/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "platform/mbed_thread.h"


// Blinking rate in milliseconds
#define BLINKING_RATE_MS                                                    1000


int N = 4;

InterruptIn button(USER_BUTTON);
bool interrupted;
int times_interrupted;
unsigned long t;
int *pressed = (int *)malloc(sizeof(int)*N);

DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);

void button_down()
{
        interrupted = true;
        wait_us(300000);
}

int main()
{
    // Initialise the digital pin LED1 as an output

    button.rise(button_down);
    DigitalOut *leds[3] = {&led1, &led2, &led3};

    t = 0;
    interrupted = false;
    times_interrupted = 0;

    
    while (true) 
    {
        // turn LED on
        if (times_interrupted < N) 
        {
            *leds[t % 3] = 1;
        }
        else
        {
            *leds[*(pressed + sizeof(int)*(t % N))] = 1; // led number pressed[t % N] should be turned on
        }
        
        // sleep
        thread_sleep_for(BLINKING_RATE_MS);

        // turn LED off
        if (times_interrupted < N) 
        {
            *leds[t % 3] = 0;
        }
        else
        {
            *leds[*(pressed + sizeof(int)*(t % N))] = 0; // led number pressed[t % N] should be turned off
        }

        if (interrupted) 
        {

            *(pressed + sizeof(int)*times_interrupted) = t % 3;
            times_interrupted++;
            interrupted = false;

            if (times_interrupted == N)
            {
                t = 0; // reset t so that sequence starts from beginning
            }
        }

        // increment t
        t++;
    }
}
