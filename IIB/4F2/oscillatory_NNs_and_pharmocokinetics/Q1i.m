
A = [-10, 0; 0, -100];
B = [10; 100];
C = [1, 0; 0, 1; 0, 0];
D = [0; 0; 1];

Gsubs = ss(A, B, C, D);
s = tf('s');

G = Gsubs * 1/(s+1);


w1 = 1.0;
w2 = 2.0;
w3 = 0.5;

simulate_nonlinear_system(w1, w2, w3);