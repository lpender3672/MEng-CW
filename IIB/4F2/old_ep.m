
Ghat = [tf([50],[1, 20]), tf([1],[1,7,12]) ; tf([-10],[1, 20]), tf([1],[1, 6, 6, 5])]

[inform, at_freq] = norm(Ghat, inf);

om = logspace(-4, 4, 1000);
sigma(Ghat, om)
grid