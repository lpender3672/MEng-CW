clear;
nx=201;
for i=1:nx
    x(i) = (i-1)*1./(nx-1);
    if i < nx/20.
        u(i) = 1.;
    else
        u(i) = 0.;
    end
%    u(i) = exp(-((x(i)-0.2)/0.05)^2);
end
newplot;
hold on;
plot(x,u,'r','LineWidth',1);
c = 1.005;
offset = 0;
nt = 100;
nplot=10;
for n=1:nt
    for i=2:nx-1
        un(i) = u(i)-c*(u(i)-u(i-1));
    end
    un(1) = 1;
    un(nx) = 0;
    if rem(n,nplot)==0
        offset = offset + .02;
        for i=1:nx
            up(i) = un(i)+offset;
        end
        plot(x,up,'b','Linewidth',1.5);
    end
    u = un;
end
hold off;