clear all
close all
clc


% analysis via circle criterion
circle

% simulation

% initial condition
state0 = [1;0;0];

%feedback gain
k = 100;

% simulation parameters
T = 50;
samples = 1000;
SIM1 = sim('model',linspace(0,T,samples))

figure
plot(SIM1.x.time,SIM1.x.data(:,1),'k','linewidth',1)
grid on
ylabel('y')
xlabel('t')
title('Periodic behavior')
xlim([0 50])
exportfig(gcf,'circle_sim','FontMode','scaled','FontSize',1.4,'width',12,'height',12,'color','cmyk')

figure
plot(SIM1.x.time,SIM1.x.data,'linewidth',1)
grid on
ylabel('x')
xlabel('t')
title('Periodic behavior')
