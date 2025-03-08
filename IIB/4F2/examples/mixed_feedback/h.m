function [y] = h(u)

%parameters

%input parsing
k1 = u(1);
k2 = u(2);
x1 = u(3);
x2 = u(4);

%behavior static readout
y = sat(k1*x1 - k2*x2);
end

