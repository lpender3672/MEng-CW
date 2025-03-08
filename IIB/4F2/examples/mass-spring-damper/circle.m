clear all;
close all;
clc;

%negative integral feedback du/dt = -5 y
 
A = [0 1 0; -1 -4 0; 1 0 0]
B = [0 ; 1 ; 0]
C  = [0 0 100]

rate = 1;

sys = ss(A,B,C,0)
eig(A)

shift_sys = ss(A+rate*eye(3),B,C,0);

figure
w = logspace(-3,1,1024);
nyquistplot(shift_sys,[-flip(w),w],'k');
hold on
plot([-1,-1],[-30,30],'--b')
exportfig(gcf,'circle_shifted_nyquist','FontMode','scaled','FontSize',1.4,'width',12,'height',12,'color','cmyk')

