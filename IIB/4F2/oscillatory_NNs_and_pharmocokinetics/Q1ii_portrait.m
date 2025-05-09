
% phase portrait
close all;

w1 = 100;
figure;
phi = @(u) tanh(u);

[y, z1] = meshgrid(linspace(-2, 2, 20), linspace(-2, 2, 20));

dy = -y + phi(w1 .* z1 + 25 .* y);
dz1 = (-z1 + y) / 0.1;

quiver(y, z1, dy, dz1, 1)

hold on
for y0 = -1:1:1
    for z10 = 1:1:1
        [t, z] = ode45(@(t,z) dynamics(t, z, w1), [0 10], [y0; z10]);
        plot(z(:,1), z(:,2))
    end
end
[t, z] = ode45(@(t,z) dynamics(t, z, w1), [0 10], [1e-9; 1e-9]);
plot(z(:,1), z(:,2))
hold off

xlabel('y'), ylabel('z_1')
title(['Phase Portrait for w1 = ', num2str(w1)])
axis tight
print(gcf, 'figures/oscillator_phase_portrait_w100.png', '-dpng', '-r600');


w1 = -25;
figure;
phi = @(u) tanh(u);

[y, z1] = meshgrid(linspace(-2, 2, 20), linspace(-2, 2, 20));

dy = -y + phi(w1 .* z1 + 25 .* y);
dz1 = (-z1 + y) / 0.1;

quiver(y, z1, dy, dz1, 1)

% trajectories arent very easy to see because they just loop back over
% eachother
hold on
for y0 = -1:1:1
    for z10 = 1:1:1
        [t, z] = ode45(@(t,z) dynamics(t, z, w1), [0 10], [y0; z10]);
        plot(z(:,1), z(:,2))
    end
end
[t, z] = ode45(@(t,z) dynamics(t, z, w1), [0 10], [1e-9; 1e-9]);
plot(z(:,1), z(:,2))

hold off

xlabel('y'), ylabel('z_1')
title(['Phase Portrait for w1 = ', num2str(w1)])
axis tight
print(gcf, 'figures/oscillator_phase_portrait_w-25.png', '-dpng', '-r600');


function dzdt = dynamics(t, z, w1)
    y = z(1);
    z1 = z(2);
    
    phi = @(u) tanh(u);
    
    dy = -y + phi(w1*z1 + 25*y);
    dz1 = (-z1 + y) / 0.1;
    
    dzdt = [dy; dz1];
end