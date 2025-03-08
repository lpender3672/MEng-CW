clear all
close all
clc


% for dominance analysis, run the file "dominance"

% for simulations, run this file.

state0 = [1;0;0];

T = 100;
samples = 1000;
SIM1 = sim('model',linspace(0,T,samples))

figure
plot(SIM1.x.time,SIM1.x.data(:,1),'k','linewidth',2)
grid on
ylabel('y')
xlabel('t')
title('Snap locomotion')
exportfig(gcf,'snap_locomotion','FontMode','scaled','FontSize',1,'width',10,'height',10,'color','cmyk')

figure
plot(SIM1.x.time,SIM1.x.data,'linewidth',1)
grid on
ylabel('x')
xlabel('t')
title('Snap locomotion')
