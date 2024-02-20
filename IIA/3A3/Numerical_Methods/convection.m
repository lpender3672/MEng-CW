clear;
nx=101;
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
c = 0.5;
a = c^2/4;
dt = 0.1;
dx = 2/nx;
tf = 1;
offset = 0;
nt = tf/dt;
nplot=5;
for n=1:nt
    for i=2:nx-1
        un(i) = u(i)-u(i)*(dt/dx)*(u(i)-u(i-1));
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