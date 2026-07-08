clear; clc;

scriptDir = fileparts(mfilename('fullpath'));
repoRoot = fileparts(scriptDir);
dataDir = fullfile(repoRoot, 'data', 'figure_source');
outDir = fullfile(repoRoot, 'figures');
if ~exist(outDir, 'dir'); mkdir(outDir); end

mapTable = readtable(fullfile(dataDir, 'figure1_threshold_profile.csv'));
aucTable = readtable(fullfile(dataDir, 'figure1_auc_profile.csv'));
threshold = mapTable.threshold_pct';
mapVals = mapTable.mAP_pct';
aucVals = aucTable.AUC_pct';

blue = [0.11 0.39 0.70];
grey = [0.34 0.34 0.34];
guideGrey = [0.60 0.60 0.60];

fig = figure('Color', 'w', 'Units', 'inches', 'Position', [0.8 0.8 6.5 3.35]);
ax = axes(fig, 'Position', [0.10 0.16 0.69 0.70]);
hold(ax, 'on');
plot(ax, threshold, mapVals, '-o', ...
    'Color', blue, 'MarkerFaceColor', blue, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 1.60, 'MarkerSize', 6.0);
grid(ax, 'on');
ax.XLim = [28 104];
ax.YLim = [74 90.5];
ax.XTick = threshold;
ax.YTick = 74:2:90;
xlabel(ax, 'Maximum training-set 3-mer Jaccard threshold (%)');
ylabel(ax, 'mAP (%)');

plot(ax, [30 100], [mapVals(1) mapVals(1)], ':', ...
    'Color', guideGrey, 'LineWidth', 0.9);
plot(ax, [100 100], [mapVals(1) mapVals(end)], ':', ...
    'Color', guideGrey, 'LineWidth', 0.9);
text(ax, 63.0, 77.55, 'Endpoint span = 11.67 pp', ...
    'FontName', 'Arial', 'FontSize', 9.0, 'FontWeight', 'bold', ...
    'Color', blue, 'BackgroundColor', 'w', 'Margin', 2.0);

inset = axes(fig, 'Position', [0.73 0.40 0.23 0.27]);
hold(inset, 'on');
plot(inset, threshold, aucVals, '-s', ...
    'Color', grey, 'MarkerFaceColor', [0.74 0.74 0.74], ...
    'MarkerEdgeColor', 'w', 'LineWidth', 1.35, 'MarkerSize', 4.6);
grid(inset, 'on');
inset.Box = 'on';
inset.LineWidth = 0.75;
inset.XColor = [0.50 0.50 0.50];
inset.YColor = [0.50 0.50 0.50];
inset.XLim = [28 102];
inset.YLim = [96.5 98.8];
inset.XTick = [30 60 100];
inset.YTick = [96.5 97.5 98.5];
ylabel(inset, 'AUC (%)');

apply_jbi_artwork_style(fig);
ax.FontSize = 9;
ax.XLabel.FontSize = 10;
ax.YLabel.FontSize = 10;
inset.FontSize = 8.5;
inset.XLabel.FontSize = 9;
inset.YLabel.FontSize = 9;
inset.Box = 'on';
inset.LineWidth = 0.75;
inset.GridColor = [0.89 0.89 0.89];
inset.GridAlpha = 0.20;

set(fig, 'PaperPositionMode', 'auto');
exportgraphics(fig, fullfile(outDir, 'Figure_1.pdf'), 'ContentType', 'vector', 'BackgroundColor', 'white');
