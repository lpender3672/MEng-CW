function [cst,cslo,csup] = csenv(scale)
%
%  function [cst,cslo,csup] = csenv(scale)
%
%  Function to return points on C-star envelope.  Variables:
%
%    scale	input scale factor; scale = 1 is normalised envelope
%    cst	vector of time (x) values
%    cslo	vector of C* (y) values for lower curve of envelope
%    csup	vector of C* (y) values for upper curve of envelope


cst = [0 4 8 12 16 20 24 28 32 36 45 54 63 72 90 108]/36;

cslo = [0 0 2 6 18 23 25 26.2 27.4 28.4 30.5 31.8 33 33.7 34.4 34.8]/37;
cslo = scale * cslo;

csup = [0 52.2 62.2 63.2 62 58.3 54.2 50 47.1 44.9 41.8 40.3 39.6 39 38 37]/37;
csup = scale * csup;
