clear; clc;

scriptDir = fileparts(mfilename('fullpath'));
repoRoot = fileparts(scriptDir);
dataDir = fullfile(repoRoot, 'data', 'figure_source');
outDir = fullfile(repoRoot, 'figures');
if ~exist(outDir, 'dir'); mkdir(outDir); end

candidatePool = readtable(fullfile(dataDir, 'figure3_candidate_pool_points.csv'), 'TextType', 'string');
rawTop = readtable(fullfile(dataDir, 'figure3_raw_top20.csv'), 'TextType', 'string');
auditedTop = readtable(fullfile(dataDir, 'figure3_audited_top20.csv'), 'TextType', 'string');
composition = readtable(fullfile(dataDir, 'figure3_similarity_composition.csv'), 'TextType', 'string');
scatterData = candidatePool;
shared = scatterData(scatterData.membership == "shared", :);
rawOnly = scatterData(scatterData.membership == "raw_only", :);
auditedOnly = scatterData(scatterData.membership == "audited_only", :);

grey = [0.42 0.44 0.46];
charcoal = [0.16 0.17 0.18];
blue = [0.11 0.39 0.70];
red = [0.78 0.24 0.20];
lowColor = [0.22 0.54 0.76];
mediumColor = [0.86 0.58 0.18];
highColor = [0.72 0.22 0.18];

fig = figure('Color', 'w', 'Units', 'inches', 'Position', [0.8 0.8 6.85 3.92]);
axLegend1 = axes(fig, 'Position', [0.08 0.84 0.57 0.08], 'Visible', 'off');
axLegend2 = axes(fig, 'Position', [0.73 0.84 0.23 0.08], 'Visible', 'off');

ax1 = axes(fig, 'Position', [0.08 0.15 0.57 0.64]);
hold(ax1, 'on');
hAll = scatter(ax1, candidatePool.max_train_jaccard, candidatePool.predicted_score, 15, grey, ...
    'filled', 'MarkerEdgeColor', 'none', 'MarkerFaceAlpha', 0.60);
hShared = scatter(ax1, shared.max_train_jaccard, shared.predicted_score, 46, ...
    'o', 'MarkerFaceColor', 'w', 'MarkerEdgeColor', charcoal, 'LineWidth', 1.10);
hRaw = scatter(ax1, rawOnly.max_train_jaccard, rawOnly.predicted_score, 52, ...
    'o', 'MarkerFaceColor', 'none', 'MarkerEdgeColor', blue, 'LineWidth', 1.45);
hAud = scatter(ax1, auditedOnly.max_train_jaccard, auditedOnly.predicted_score, 52, ...
    'd', 'MarkerFaceColor', 'none', 'MarkerEdgeColor', red, 'LineWidth', 1.45);
xline(ax1, 0.40, '--', 'Color', [0.42 0.42 0.42], 'LineWidth', 0.90, 'HandleVisibility', 'off');
text(ax1, 0.49, 0.11, 'Audit threshold', ...
    'FontName', 'Arial', 'FontSize', 9.0, 'Color', [0.08 0.08 0.08], ...
    'BackgroundColor', 'w', 'Margin', 2.0, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
xlabel(ax1, 'Maximum ESCAPE training-set 3-mer Jaccard');
ylabel(ax1, 'Predicted antibacterial score');
ax1.XLim = [0 1.02];
ax1.YLim = [0 1.02];
ax1.XTick = 0:0.2:1.0;
ax1.YTick = 0:0.1:1.0;
grid(ax1, 'on');
text(ax1, 0.01, 0.965, 'A', 'Units', 'normalized', 'VerticalAlignment', 'top');

lgd1 = legend(ax1, [hAll hShared hRaw hAud], ...
    {'All candidates', 'Shared', 'Raw-only', 'Audited-only'}, ...
    'Location', 'northoutside', 'Orientation', 'horizontal', 'NumColumns', 3, ...
    'Box', 'on', 'Color', 'w');
lgd1.ItemTokenSize = [14, 8];

ax2 = axes(fig, 'Position', [0.73 0.15 0.23 0.64]);
hold(ax2, 'on');
classes = ["low", "medium", "high"];
counts = zeros(2, 3);
for classIndex = 1:numel(classes)
    counts(1, classIndex) = str2double(composition.count(composition.list_name == "Raw top 20" & composition.similarity_class == classes(classIndex)));
    counts(2, classIndex) = str2double(composition.count(composition.list_name == "Audited top 20" & composition.similarity_class == classes(classIndex)));
end
bars = bar(ax2, counts, 'stacked', 'BarWidth', 0.58, 'EdgeColor', [0.16 0.16 0.16], 'LineWidth', 0.70);
bars(1).FaceColor = lowColor;
bars(2).FaceColor = mediumColor;
bars(3).FaceColor = highColor;
for listIndex = 1:2
    running = 0;
    for classIndex = 1:3
        value = counts(listIndex, classIndex);
        if value > 0
            text(ax2, listIndex, running + value/2, num2str(value), ...
                'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
                'Color', [0.08 0.08 0.08], 'FontWeight', 'bold', 'FontSize', 9.0);
        end
        running = running + value;
    end
end
set(ax2, 'XTick', [1 2], 'XTickLabel', {'Raw', 'Audited'});
ylabel(ax2, 'Number of candidates');
ax2.YLim = [0 22];
ax2.XLim = [0.45 2.65];
grid(ax2, 'on');
text(ax2, 0.04, 0.965, 'B', 'Units', 'normalized', 'VerticalAlignment', 'top');
lgd2 = legend(ax2, {'Low', 'Med', 'High'}, ...
    'Location', 'northoutside', 'Orientation', 'horizontal', 'NumColumns', 3, ...
    'Box', 'on', 'Color', 'w');
lgd2.ItemTokenSize = [13, 8];

apply_jbi_artwork_style(fig);
ax1.FontSize = 9; ax1.XLabel.FontSize = 10; ax1.YLabel.FontSize = 10;
ax2.FontSize = 9; ax2.YLabel.FontSize = 10;
lgd1.FontSize = 8.5;
lgd2.FontSize = 8.7;
lgd1.LineWidth = 0.75;
lgd2.LineWidth = 0.75;

drawnow;
lgd1.Position(1) = axLegend1.Position(1) + 0.005;
lgd1.Position(2) = axLegend1.Position(2) + 0.002;
lgd1.Position(3) = axLegend1.Position(3) - 0.01;
lgd2.Position(1) = axLegend2.Position(1) + 0.005;
lgd2.Position(2) = axLegend2.Position(2) + 0.002;
lgd2.Position(3) = axLegend2.Position(3) - 0.01;

set(fig, 'PaperPositionMode', 'auto');
savefig(fig, fullfile(outDir, 'Figure_3.fig'));
exportgraphics(fig, fullfile(outDir, 'Figure_3.pdf'), 'ContentType', 'vector', 'BackgroundColor', 'white');
exportgraphics(fig, fullfile(outDir, 'Figure_3.png'), 'Resolution', 600, 'BackgroundColor', 'white');
