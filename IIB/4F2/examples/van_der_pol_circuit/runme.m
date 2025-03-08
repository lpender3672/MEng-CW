clear all
close all
clc

k = 1;
state0 = [1;1];

T = 10;
samples = 1000;
SIM1 = sim('model',linspace(0,T,samples))

figure
plot(SIM1.voltage.time,SIM1.voltage.data,'k','linewidth',2)
grid on
ylabel('V')
xlabel('t')
title('Van der Pol circuit')
exportfig(gcf,'VP_circuit','FontMode','scaled','FontSize',1,'width',10,'height',10,'color','cmyk')