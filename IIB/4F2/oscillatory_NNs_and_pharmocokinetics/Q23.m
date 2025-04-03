close all

figure;
figureLegends = {};

hold on;
for k = [0.5, 1.0, 1.5, 2.0]

    Pharmacokinetic_sim(k, 0.1)

    figureLegends{end+1} = ['k = ', num2str(k)];
end

xlabel('t')
ylabel('c_1')
legend(figureLegends)
print(gcf, 'figures/23_pharmacokinetic_sim', '-dpng', '-r600');
