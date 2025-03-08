function [y] = h(u)

%parameters

%input parsing
x = u(1);

y = -20*x;

if x > 5    
    y = 20*x-200;
end
if x < -5
    y = 20*x+200;
end


end

