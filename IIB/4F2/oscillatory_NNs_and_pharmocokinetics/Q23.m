close all

figure;

hold on;
for k = [0.5, 1.0, 1.5, 2.0]

    Pharmacokinetic_sim(k, 0.1)
end

legend('k=')