%% saloon car
m = 2050;
I = 5430;
a = 1.49;
b = 1.71;
Cf = 77900;
Cr = 76500;
U = 30;
om = logspace(-2, 2, 100);

C = Cf + Cr;
afbr = (a*Cf - b*Cr);

A = zeros(2,2,length(om));
A(1,1,:) = 1j * om * m + C/U;
A(1,2,:) = m * U + afbr/U;
A(2,1,:) = afbr/U;
A(2,2,:) = 1j * om * I + (a^2*Cf + b^2*Cr);

B = [Cf; a*Cf];

Ainv = zeros(2,2,length(om));
saloon_tfs = zeros(2, length(om));

for k = 1:length(om)
    Ainv(:,:,k) = inv(A(:,:,k));
    saloon_tfs(:,k) = Ainv(:,:,k) * B;
end

%% Sport car

m = 1010;
I = 1030;
a = 1.23;
b = 1.02;
Cf = 117000;
Cr = 145000;
U = 30;
C = Cf + Cr;
afbr = (a*Cf - b*Cr);

A = zeros(2,2,length(om));
A(1,1,:) = 1j * om * m + C/U;
A(1,2,:) = m * U + afbr/U;
A(2,1,:) = afbr/U;
A(2,2,:) = 1j * om * I + (a^2*Cf + b^2*Cr);

B = [Cf; a*Cf];

Ainv = zeros(2,2,length(om));
sport_tfs = zeros(2, length(om));

for k = 1:length(om)
    Ainv(:,:,k) = inv(A(:,:,k));
    sport_tfs(:,k) = Ainv(:,:,k) * B;
end

%% Plot

subplot(2,1,1);
hold on;
semilogx(om, saloon_tfs(1, :), 'LineWidth',1.5);
semilogx(om, sport_tfs(1, :), 'LineWidth',1.5);
xlabel('\omega');
ylabel('TF_{1}');
title('First Transfer Function Comparison');
legend('Saloon', 'Sport');
grid on;
hold off;

% Plot second transfer function (second row)
subplot(2,1,2);
hold on;
semilogx(om, saloon_tfs(2, :), 'LineWidth',1.5);
semilogx(om, sport_tfs(2, :), 'LineWidth',1.5);
xlabel('\omega');
ylabel('TF_{2}');
title('Second Transfer Function Comparison');
legend('Saloon', 'Sport');
grid on;
hold off;

