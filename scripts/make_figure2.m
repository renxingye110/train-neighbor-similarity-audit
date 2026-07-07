clear; clc;

scriptDir = fileparts(mfilename('fullpath'));
repoRoot = fileparts(scriptDir);
dataDir = fullfile(repoRoot, 'data', 'figure_source');
outDir = fullfile(repoRoot, 'figures');
if ~exist(outDir, 'dir'); mkdir(outDir); end

curves = readtable(fullfile(dataDir, 'figure2_source_heldout_profiles.csv'), 'TextType', 'string');
summary = readtable(fullfile(dataDir, 'figure2_endpoint_spans.csv'), 'TextType', 'string');
retraining = readtable(fullfile(dataDir, 'figure2_retraining_changes.csv'), 'TextType', 'string');

datasets = ["ESCAPE_ESM2", "DRAMP_antibacterial", "APD6", "DBAASP"];
shortLabels = ["ESCAPE", "DRAMP", "APD6", "DBAASP"];
colors = [
    0.11 0.39 0.70
    0.02 0.46 0.40
    0.69 0.36 0.09
    0.41 0.30 0.60
];
markers = {'o', 's', 'd', '^'};

fig = figure('Color', 'w', 'Units', 'inches', 'Position', [0.8 0.8 6.8 4.95]);
layout = tiledlayout(fig, 2, 2, 'TileSpacing', 'compact', 'Padding', 'compact');

ax1 = nexttile(layout, [1 2]);
hold(ax1, 'on');
lineHandles = gobjects(numel(datasets), 1);
for i = 1:numel(datasets)
    rows = curves(curves.dataset == datasets(i), :);
    [~, order] = sort(rows.threshold);
    rows = rows(order, :);
    if datasets(i) == "ESCAPE_ESM2"
        lineHandles(i) = plot(ax1, rows.threshold, rows.mAP_mean * 100, ['-' markers{i}], ...
            'Color', colors(i, :), 'MarkerFaceColor', colors(i, :), ...
            'MarkerEdgeColor', 'w', 'LineWidth', 1.50, 'MarkerSize', 5.2);
    else
        lineHandles(i) = errorbar(ax1, rows.threshold, rows.mAP_mean * 100, rows.mAP_sd * 100, ['-' markers{i}], ...
            'Color', colors(i, :), 'MarkerFaceColor', colors(i, :), ...
            'MarkerEdgeColor', 'w', 'LineWidth', 1.25, 'MarkerSize', 4.9, 'CapSize', 3);
    end
end
xlabel(ax1, 'Maximum training-set 3-mer Jaccard threshold');
ylabel(ax1, 'mAP (%)');
ax1.XLim = [0.29 1.01];
ax1.YLim = [74 96];
ax1.XTick = 0.3:0.1:1.0;
ax1.YTick = 74:2:96;
grid(ax1, 'on');
text(ax1, 0.01, 0.98, 'A', 'Units', 'normalized', 'VerticalAlignment', 'top');
lgd1 = legend(ax1, lineHandles, cellstr(shortLabels), ...
    'Location', 'southeast', 'Orientation', 'horizontal', ...
    'NumColumns', 2, 'Box', 'off');
lgd1.ItemTokenSize = [16, 8];

ax2 = nexttile(layout);
hold(ax2, 'on');
span = zeros(numel(datasets), 1);
spanSd = zeros(numel(datasets), 1);
for i = 1:numel(datasets)
    row = summary(summary.dataset == datasets(i), :);
    span(i) = row.span_pp_mean;
    spanSd(i) = row.span_pp_sd;
end
b2 = bar(ax2, span, 0.60, 'FaceColor', 'flat', 'EdgeColor', [0.18 0.18 0.18], 'LineWidth', 0.70);
for i = 1:numel(datasets)
    b2.CData(i, :) = colors(i, :);
end
errorbar(ax2, 1:numel(datasets), span, spanSd, 'k.', 'LineWidth', 0.85, 'CapSize', 3);
for i = 1:numel(datasets)
    text(ax2, i, span(i) + spanSd(i) + 0.55, sprintf('%.1f', span(i)), ...
        'HorizontalAlignment', 'center', 'FontSize', 9.0, 'FontWeight', 'bold', ...
        'Color', [0.08 0.08 0.08]);
end
set(ax2, 'XTick', 1:numel(datasets), 'XTickLabel', cellstr(shortLabels));
xtickangle(ax2, 16);
ylabel(ax2, 'Endpoint span (pp)');
ax2.YLim = [0 13.6];
ax2.XLim = [0.42 4.58];
ax2.TickLabelInterpreter = 'none';
grid(ax2, 'on');
text(ax2, 0.03, 0.96, 'B', 'Units', 'normalized', 'VerticalAlignment', 'top');

ax3 = nexttile(layout);
hold(ax3, 'on');
drop = zeros(numel(datasets), 1);
dropSd = zeros(numel(datasets), 1);
for i = 1:numel(datasets)
    row = retraining(retraining.dataset == datasets(i), :);
    drop(i) = row.mAP_drop_pp_mean;
    dropSd(i) = row.mAP_drop_pp_sd;
end
b3 = bar(ax3, drop, 0.60, 'FaceColor', 'flat', 'EdgeColor', [0.18 0.18 0.18], 'LineWidth', 0.70);
for i = 1:numel(datasets)
    b3.CData(i, :) = colors(i, :);
end
errorbar(ax3, 1:numel(datasets), drop, dropSd, 'k.', 'LineWidth', 0.85, 'CapSize', 3);
yline(ax3, 0, '-', 'Color', [0.45 0.45 0.45], 'LineWidth', 0.80);
for i = 1:numel(datasets)
    xPos = i + (i == 1) * 0.06;
    if drop(i) >= 0
        yVal = drop(i) + dropSd(i) + 0.42;
        va = 'bottom';
    else
        yVal = drop(i) - dropSd(i) - 0.40;
        va = 'top';
    end
    text(ax3, xPos, yVal, sprintf('%+.2f', drop(i)), ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', va, ...
        'FontSize', 9.0, 'FontWeight', 'bold', 'Color', [0.08 0.08 0.08]);
end
set(ax3, 'XTick', 1:numel(datasets), 'XTickLabel', cellstr(shortLabels));
xtickangle(ax3, 16);
ylabel(ax3, 'mAP change after removal (pp)');
ax3.YLim = [-2.4 14.2];
ax3.XLim = [0.42 4.58];
ax3.TickLabelInterpreter = 'none';
grid(ax3, 'on');
text(ax3, -0.06, 0.98, 'C', 'Units', 'normalized', 'VerticalAlignment', 'top', 'HorizontalAlignment', 'left', 'Clipping', 'off');

apply_jbi_artwork_style(fig);
ax1.FontSize = 9; ax1.XLabel.FontSize = 10; ax1.YLabel.FontSize = 10;
ax2.FontSize = 9; ax2.YLabel.FontSize = 10;
ax3.FontSize = 9; ax3.YLabel.FontSize = 10;
lgd1.FontSize = 9;

set(fig, 'PaperPositionMode', 'auto');
savefig(fig, fullfile(outDir, 'Figure_2.fig'));
exportgraphics(fig, fullfile(outDir, 'Figure_2.pdf'), 'ContentType', 'vector', 'BackgroundColor', 'white');
exportgraphics(fig, fullfile(outDir, 'Figure_2.png'), 'Resolution', 600, 'BackgroundColor', 'white');
