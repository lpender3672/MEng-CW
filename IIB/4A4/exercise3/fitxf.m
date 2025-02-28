function [numcof,xffit] = fitxf(omega,xfun,dencof,omglim,order)
%
%    [numcof,xffit] = fitxf(omega,xfun,dencof,omglim,order)
%
%  Polynomial fitting routine for transfer function numerator.  Inputs are
%  frequency vector 'omega', transfer function 'xfun', coefficients of the 
%  denominator polynomial, 'dencof', upper limit of the frequency range
%  to be fitted 'omglim', and degree of desired polynomial fit 'order'.
%  Outputs are estimated coefficients of the numerator polynomial, 'numcof',
%  and the corresponding fit to xfun, 'xffit'.  The coefficient vector
%  'numcof' represents the numerator polynomial using the standard Matlab
%  convention, ie
%
%  N(s) = numcof(1)*s^order + numcof(2)*s^(order-1) + ... + numcof(order+1)
%
%  The routine assumes that 'dencof' represents the denominator polynomial
%  with the same convention.

%
%    Calculate no. of coefficients for real and imaginary parts
%
ncr = floor(order/2);
nci = ceil(order/2);
%
%    Find index corresponding to omglim
%
ndat = length(omega);
delomg = omega(ndat)/(ndat - 1);
nfit = floor(omglim/delomg) + 1;
omgfit = omega(1:nfit);
%
%    Transfer function denominator and numerator
%
denom = polyval(dencof,i*omega);
numer = xfun .* denom;
%
%    Estimate coefficients using least squares fit
%
%      LHS matrix
%
for n = 1:order+1
   k = order + 1 - n;
   coln = (i*omgfit).^k ./ denom(1:nfit);
   omgmat(1:nfit,n) = real(coln);
   omgmat(nfit+1:2*nfit,n) = imag(coln);
end
%
%      RHS vector
%
xfvec = real(xfun(1:nfit));
xfvec(nfit+1:2*nfit) = imag(xfun(1:nfit));
%
%      Least squares solution to omgmat*numcof = xfvec
%
numcof(1:order+1) = omgmat\xfvec;
%
%    Fitted transfer function
%
numer = polyval(numcof,i*omega);
xffit = numer ./ denom;
