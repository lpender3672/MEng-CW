
% want to know what the inverse of a cardioid looks like

phi = linspace(-pi, pi, 2000);
beta = 1.0;
z = beta * cos(phi / 2).^2 .* exp(-1j .* phi);


x1 = real(z);
y1 = imag(z);
x2 = real(0.5*z);
y2 = imag(0.5*z);
figure;
plot(x1, y1, 'b', 'LineWidth', 1); hold on;
plot(x2, y2, 'r', 'LineWidth', 1);

X = [x1, fliplr(x2)];
Y = [y1, fliplr(y2)];

fill(X, Y, [0.8 0.8 0.8], 'FaceAlpha', 0.5, 'EdgeColor', 'none');
%patchHandle = patch([x1, fliplr(x2)], [y1, fliplr(y2)], 'white');
%set(patchHandle, 'FaceColor', [0.7, 0.7, 0.7], 'EdgeColor', 'none');
%hatchfill2(patchHandle, 'HatchStyle', 'single', 'HatchColor', [0.2, 0.2, 0.2], 'HatchLineWidth', 1);


plot(0.5, 0, 'r-o')
plot(1.0, 0, 'b-o')

text(1.05, 0.05, '$\frac{k}{\lambda_1+\alpha_{12}}$', 'Interpreter', 'latex', 'FontSize', 12);
text(0.2, 0.05, '$k(\mu_1+\alpha_{12}-\frac{\alpha_{12}\alpha_{21}}{\lambda_2+\alpha_{21}})$', 'Interpreter', 'latex', 'FontSize', 12);
grid on;
hold off;
xlim([-0.5, 1.5])
ax = gca;  % Get current axes handle
ax.XAxisLocation = 'origin';
ax.YAxisLocation = 'origin';
set(gca, 'XTick', [], 'YTick', []);

print(gcf, 'figures/closed_loop_return_ratio.png', '-dpng', '-r600');


