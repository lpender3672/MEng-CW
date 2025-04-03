
close all;

w1 = 2.8670   
w2 = 42.2303 
w3 = -48.7531

o1 = -404.3271
o2 = 76.9646
o3 = 243.3162

figure;
hold on; 

w = 1.025 * pi/5
phi = pi/4;
A = 3;
simulate_nonlinear_harmonic(w1, w2, w3, A, w, phi)
simulate_nonlinear_step(o1, o2, o3)

xlabel('Time (s)')
ylabel('y(t)')
legend('i) Network with Harmonic Input', 'iii) Network with Step Input')
print(gcf, 'figures/15_matched.png', '-dpng', '-r600');
