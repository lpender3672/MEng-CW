clear
close all
clc

%% Data
gamma = 5;
k = 20;

A = [0 1 0; 0 -10 1; -gamma 0 0]
B = [0 ; -1 ; 0]
C  = [1 0 0]


A1 = A + k*B*C
A2 = A - k*B*C

sys = ss(A,B,C,0)

figure
rlocus(sys)

figure
nyquist(sys)

figure
bode(sys)

lambda = 4


%% LMI gain design

epsilon = 10^-6

cvx_begin sdp

%cvx_solver sedumi
cvx_solver SDPT3
% cvx_precision high

n = length(A);
variable P(n,n) symmetric
% state feedback gain K=Z/Q, to be determined
%variable gain(1) nonnegative
%minimise gain

% gain LMI
LMI1 = A1'*P+ P*A1 + 2*lambda*P;      
LMI1 <= -epsilon*eye(n)
LMI2 = A2'*P+ P*A2 + 2*lambda*P;      
LMI2 <= -epsilon*eye(n)

cvx_end

P
eig(P)

