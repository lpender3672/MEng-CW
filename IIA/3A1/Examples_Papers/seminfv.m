function vel = seminfv(r1,ro)
%
%  function vel = seminfv(r1,ro)
%
%  Calculates the vector velocity at ro due to the semi-infinite vortex
%  with one end at r1.  The vortex is taken to go to infinity in the +ve 
%  x direction, and to have circulation positive from r1 to infinity
%  according to the RH screw rule.  Velocity is for unit circulation.
%
ra = r1-ro;

rahat = ra/norm(ra);
rbhat = [1 0 0];
rvhat = [1 0 0];

raxrvh = cross(ra,rvhat);

vel = (0.25/pi) * dot(rvhat,rbhat-rahat) * raxrvh/(norm(raxrvh))^2;

