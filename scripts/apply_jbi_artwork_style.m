function apply_jbi_artwork_style(fig)
fontName = 'Arial';
tickSize = 9;
labelSize = 10;
legendSize = 9;
panelSize = 11;

set(fig, 'Color', 'w');
set(findall(fig, '-property', 'FontName'), 'FontName', fontName);

axesList = findall(fig, 'Type', 'axes');
for i = 1:numel(axesList)
    ax = axesList(i);
    ax.FontName = fontName;
    ax.FontSize = tickSize;
    ax.LineWidth = 0.85;
    ax.Box = 'off';
    ax.Layer = 'top';
    ax.GridColor = [0.90 0.90 0.90];
    ax.GridAlpha = 0.18;
    ax.MinorGridColor = [0.95 0.95 0.95];
    ax.XGrid = 'off';
    ax.YGrid = 'on';
    ax.XMinorGrid = 'off';
    ax.YMinorGrid = 'off';
    ax.XLabel.FontName = fontName;
    ax.YLabel.FontName = fontName;
    ax.XLabel.FontSize = labelSize;
    ax.YLabel.FontSize = labelSize;
    if isprop(ax, 'Title') && ~isempty(ax.Title)
        ax.Title.String = '';
    end
end

legendList = findall(fig, 'Type', 'legend');
for i = 1:numel(legendList)
    lgd = legendList(i);
    lgd.FontName = fontName;
    lgd.FontSize = legendSize;
    lgd.Box = 'off';
    lgd.Color = 'none';
end

textList = findall(fig, 'Type', 'text');
for i = 1:numel(textList)
    txt = textList(i);
    s = string(txt.String);
    if isscalar(s) && any(s == ["A","B","C"])
        txt.FontName = fontName;
        txt.FontWeight = 'bold';
        txt.FontSize = panelSize;
        txt.Color = [0 0 0];
    end
end
end
