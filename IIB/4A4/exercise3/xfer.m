function [omega,xfun] = xfer(time,input,output)
%
%    [omega,xfun] = xfer(time,input,output)
%
%  Returns transfer function xfun(i*omega) between 'input' and 'output', and
%  associated vector 'omega' of frequency values for each member of xfun.
%  Vector time should contain time values for members of 'input' and 'output'.
%  NB!!  Frequencies in 'omega' are in rad/s.
%

%
%    Derive sample time and check for uniformity
%
ndat = length(time);
delt = (time(ndat)-time(1))/(ndat-1);
dterrs = diff(time)/delt - 1;
%if max(abs(dterrs)) > 0.001
%  error('Signals must be sampled at uniform rate!')
%end
%
%    Weight the data with a Hanning window
%
x = input(:).*hann(ndat);
y = output(:).*hann(ndat);
%
%    Calculate required length for FFT (first power of 2 > ndat)
%
power = ceil( log(ndat)/log(2) );
nfft = 2^power;
%
%    Form transfer function from ffts
%
xft = fft(x,nfft);
yft = fft(y,nfft);
xfun = yft(2:nfft/2+1) ./ xft(2:nfft/2+1);  % DC discarded
%
%    Frequency vector
%
omsamp = 2*pi/delt;
omega = (omsamp/nfft) * (1:nfft/2)';
