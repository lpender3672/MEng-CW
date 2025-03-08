function [y] = h(u)

y = u(1);

if y > 1   
    y = 1;
end
if y < -1
    y = -1;
end


end

