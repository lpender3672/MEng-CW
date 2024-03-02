function velhs = hsv(r1,r2,ro)
%
%  velhs = hsv(r1,r2,ro)
%
%  Routine to return vector velocity velhs associated with horseshoe vortex
%  with head between r1 and r2, legs going to infinity in +x direction, and
%  unit circulation.  Vectors are 1x3, i.e. r1 = [x1 y1 z1] etc.  ro
%  specifies the position where the velocity is evaluated.
%

% leg from infinity to r1; use seminfv with -ve circulation
vleg1 = -seminfv(r1,ro);

% head
vhead = linev(r1,r2,ro);

% leg from r2 to infinity
vleg2 = seminfv(r2,ro);

% sum contributions
velhs = vleg1 + vhead + vleg2;
