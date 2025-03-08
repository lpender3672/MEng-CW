function [y] = sat(u)

y = u;

if u >= 1 
    y = 1;
end
if u <= -1
    y = -1;
end

end

