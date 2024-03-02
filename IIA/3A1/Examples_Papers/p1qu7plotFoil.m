clear
close all

T = 0.75  % constant controlling overall thickness
nx = 100;  % no. of points for plot

lonc = linspace(0,1,nx);  % horizontal coordinate, normalised on chord
phi = acos(2*lonc - 1);  % angle variable associated with horizontal coord.

tonc = T * sqrt(lonc) .* (1 - lonc);  % exact thickness values

%  Calculation for Fourier-series representation, toncfs
toncfs = zeros(size(phi));  % initialises
for n = 1:5
  taun = (2*T/pi) * n * (1/(4*n^2 - 1) - 1/(4*n^2 - 9));
  toncfs = toncfs + taun*sin(n*phi);
end

plot(lonc,tonc/2,'-k',lonc,-tonc/2,'-k',...
  lonc,toncfs/2,'-r',lonc,-toncfs/2,'-r')
xlabel('l/c')
ylabel('y/c')
title('Aerofoil section')

