function response = secondOrd(t0,B,peak,period,zeta,t)

psim = atan(sqrt(1-zeta^2)/zeta);
A = (peak - B)/(sqrt(1-zeta^2) * exp(-zeta*psim/sqrt(1-zeta^2)));

omd = 2*pi/period;
omn = omd/sqrt(1-zeta^2);

response = A * exp(-zeta*omn*(t-t0)) .* sin(omd*(t-t0))  +  B;
