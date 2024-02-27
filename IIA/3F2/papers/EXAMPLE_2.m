
%% Q3 (b) Rule 3 - breaking points
clc
clear

syms s
eqn = 3*s^2 + 4*s + 1 == 0;
S = solve(eqn)


%% Q3 (c) Root locus
clc
clear

num = [1 0]; % Here, for pisitive k, use num=[1 0]; For negative k, use num=-[1 0]
den = conv([1 0.5],[1 1]);

sys = tf(num,den)


rlocus(sys)
%% Q3 (c) - negative K  Rule 3 - breaking points
syms s
fx = s / ((s+0.5)*(s+1));
dif_fx = diff(fx)

eqn = dif_fx == 0;

S = double(solve(eqn))
%% Q4 (a) Root locus
clc
clear

syms s
fx = 10*(s^2+25) - 20*s^2;

S = double(solve(fx == 0))


num = [10 0];
den = [1 0 25];

sys = tf(num,den)


rlocus(sys)


%% Q5 (a) Rule 3 - breaking points
clc
clear

syms s
a = -1/3;
fx = ((a)^3 + 2* a^2 + a) +s;

k = (solve(fx == 0))



