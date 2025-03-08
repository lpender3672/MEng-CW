clear all
close all
clc

k1 = 2;
k2 = 2;
state0 = [1;0];

T = 10;
samples = 1000;
SIM1 = sim('model',linspace(0,T,samples))

figure
plot(SIM1.state.data(:,1),SIM1.state.data(:,2),'k','linewidth',2)
grid on
ylabel('x2')
xlabel('x1')
title('Mixed feedback')
exportfig(gcf,'mixed','FontMode','scaled','FontSize',1,'width',10,'height',10,'color','cmyk')
