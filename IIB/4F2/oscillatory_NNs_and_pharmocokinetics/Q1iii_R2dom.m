
close all;

w1_values = -100:1:100;  % adjust range and resolution as needed
w2_values = -100:1:100;  % adjust range and resolution as needed
[w1Grid, w2Grid] = meshgrid(w1_values, w2_values);

is2dominantGrid = zeros(size(w1Grid));

w3 = 0;
lamda = 20;

w = logspace(-2, 4, 1000);
theta = linspace(-pi,pi,100);
z = -0.5 + 0.5 * exp(1j*theta);

s = tf('s');

%% Loop over all (w1, w2) pairs
for idx = 1:numel(w1Grid)

    current_w1 = w1Grid(idx);
    current_w2 = w2Grid(idx);
    
    sd = s - lamda;
    
    % this is to y
    %G = (current_w1/(0.1*s + 1) + current_w2/(0.01*s + 1) + w3) / (s+1);
    %Gl = (current_w1/(0.1*sd + 1) + current_w2/(0.01*sd + 1) + w3) / (sd+1);
    
    % this is to -z
    G = -(current_w1/(0.1*s + 1) + current_w2/(0.01*s + 1) + w3);
    Gl = -(current_w1/(0.1*sd + 1) + current_w2/(0.01*sd + 1) + w3);

    %{
    nyquist(Gl)
    hold on;
    zplot = 0.5 + 0.5 * exp(1j * linspace(-pi, pi, 100));
    plot(real(zplot), imag(zplot));
    hold off;
    %break
    pause(1);
    %}
    
    resp = freqresp(Gl, w);
    resp = squeeze(resp);
    
    entersDisc = any(real(resp) < -1);
    
    argArray = unwrap(angle(resp + 0.5));
    totalArgChange = argArray(end) - argArray(1);
    encirclementCount = round(totalArgChange/(pi));
    
    p_vals = pole(G);
    q = sum(real(p_vals) > 0); % num unstable open loop
        
    resp = freqresp(G, w);
    resp = squeeze(resp);
    
    argArray = unwrap(angle(resp + 1));
    totalArgChange = argArray(end) - argArray(1);
    
    nyquistEncirclementCount = -round(totalArgChange / (pi));
    Z = q + nyquistEncirclementCount;
    
    %fprintf('num of unstable open loop poles: %i \n', q);
    %fprintf('num of encirclements: %i \n', nyquistEncirclementCount); 

    if ~entersDisc 
        if (Z ~= 0)
            is2dominantGrid(idx) = 2;
        else
            is2dominantGrid(idx) = 1;
        end
    end

end

%% plot

figure;

contourf(w1Grid, w2Grid, is2dominantGrid, [0, 1, 2], 'LineColor', 'none');
xlabel('w1');
ylabel('w2');
title('2-Dominance Regions (1 = 2-dominant, 0 = not 2-dominant)');
colorbar;

