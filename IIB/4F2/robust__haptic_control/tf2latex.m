function latex_str = tf2latex_approx(sys, precision)

    if nargin < 2
        precision = 3;
    end

    [num, den] = tfdata(sys, 'v');

    syms s;
    numerator = poly2sym(num, s);
    denominator = poly2sym(den, s);

    sym_tf = vpa(numerator / denominator, precision);

    latex_str = ['\\frac{' char(vpa(numerator, precision)) '}{' char(vpa(denominator, precision)) '}'];
end
