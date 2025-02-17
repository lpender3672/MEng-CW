function G_dashed = Hinfty(G)

% Hinfty go br

% physical parameters


Wunc = makeweight(0.40,15,3);
unc = ultidyn('unc',[1 1],'SampleStateDim',2);

G_dashed = G * (1 + Wunc * unc);

end