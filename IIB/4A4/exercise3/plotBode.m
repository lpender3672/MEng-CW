function [num,xfeqf] = plotBode(omega, H, den, freq_cutoff, order, yLabelMag, yLabelPhase)

    if nargin < 6 || isempty(yLabelMag)
        yLabelMag = 'Magnitude (dB)';
    end
    if nargin < 7 || isempty(yLabelPhase)
        yLabelPhase = 'Phase (deg)';
    end

    [num,xfeqf] = fitxf(omega, H, den, freq_cutoff, order);

    magnitude_dB = 20*log10(abs(H));
    phase_deg = angle(H) * (180/pi);
    
    fit_magnitude_dB = 20*log10(abs(xfeqf));
    fit_phase_deg = angle(xfeqf) * (180/pi);

    subplot(2,1,1);
    hold on;
    semilogx(omega, magnitude_dB, 'LineWidth', 1);
    semilogx(omega, fit_magnitude_dB, 'LineWidth', 1);
    hold off;
    grid on;
    ylabel(yLabelMag, 'Interpreter', 'latex', 'FontSize', 14);
    %title('Bode Plot - Magnitude');

    subplot(2,1,2);
    hold on;
    semilogx(omega, phase_deg, 'LineWidth', 1);
    semilogx(omega, fit_phase_deg, 'LineWidth', 1);
    hold off;
    grid on;
    xlabel('Frequency (rad/s)', 'Interpreter', 'latex', 'FontSize', 14);
    ylabel(yLabelPhase, 'Interpreter', 'latex', 'FontSize', 14);
    %title('Bode Plot - Phase');
end