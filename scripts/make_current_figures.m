function make_current_figures()
% Reproduce the current manuscript Figures 2 and 3 from packaged CSV data.
clearvars -except varargin;
scriptDir = fileparts(mfilename('fullpath'));
repoRoot = fileparts(scriptDir);
dataDir = fullfile(repoRoot,'data','figure_source');
outDir = fullfile(repoRoot,'figures');
if ~exist(outDir,'dir'), mkdir(outDir); end

T = readtable(fullfile(dataDir,'figure2_primary_endpoint_summary.csv'),'TextType','string');
T = T(T.released == 1, :);
short = {'ESCAPE','TAPE 0','TAPE 1','TAPE 3'};
P = T.profile_span_pp'; R = T.retraining_change_pp'; A = T.geometry_axis'; hub = T.hub_z';
cutoff = 23.7041316734;
blue = [0.08 0.32 0.58]; green = [0.08 0.50 0.37]; grey = [0.55 0.57 0.60]; red = [0.72 0.24 0.20]; black = [0.10 0.10 0.10];
set(groot,'defaultAxesFontName','Times New Roman'); set(groot,'defaultTextFontName','Times New Roman');

%% Figure 2: complete primary screen, with released-case interpretation.
f = figure('Color','w','Units','pixels','Position',[100 100 1600 1200]);
tiledlayout(2,2,'TileSpacing','compact','Padding','compact');
nexttile;
b=bar([P;R]','grouped','BarWidth',0.78); b(1).FaceColor=blue; b(2).FaceColor=green;
set(gca,'XTick',1:4,'XTickLabel',short,'FontSize',10,'LineWidth',1.1); xtickangle(18);
ylabel('Percentage-point change','FontSize',12); title('Profile and held-out retraining','FontSize',14,'FontWeight','bold');
legend({'Profile span P','Retraining change R'},'Location','northwest','Box','off','FontSize',9); ylim([0 14]); grid on; box off;
nexttile;
bars=bar(hub,'FaceColor',green,'BarWidth',0.65); hold on;
yline(cutoff,'--','Color',[0.35 0.37 0.40],'LineWidth',1.2); set(gca,'XTick',1:4,'XTickLabel',short,'FontSize',10,'LineWidth',1.1); xtickangle(18);
ylabel('Maximum hub z','FontSize',12); title('Support gate in released cases','FontSize',14,'FontWeight','bold'); ylim([0 28]); grid on; box off;
nexttile([1 2]);
scatter(P,R,90,'filled','MarkerFaceColor',green,'MarkerEdgeColor','w'); hold on;
plot([-5 70],[-5 70],'--','Color',[0.50 0.52 0.55],'LineWidth',1.1);
text(P(1)-1,R(1)+1,'ESCAPE','FontSize',10,'HorizontalAlignment','right'); text(P(2)+1,R(2)+0.8,'TAPE 0','FontSize',10);
text(P(3)+1,R(3)-0.9,'TAPE 1','FontSize',10); text(P(4)+1,R(4)-1.0,'TAPE 3','FontSize',10);
xlabel('Fixed-profile span P (percentage points)','FontSize',12); ylabel('Held-out retraining change R (percentage points)','FontSize',12);
title('Released endpoints show concordant direction','FontSize',14,'FontWeight','bold'); xlim([0 14]); ylim([0 14]); grid on; box off;
exportgraphics(f,fullfile(outDir,'Figure_2.pdf'),'ContentType','vector','BackgroundColor','white');
exportgraphics(f,fullfile(outDir,'Figure_2.png'),'Resolution',300,'BackgroundColor','white'); close(f);

%% Figure 3: released cases only.
idx=1:numel(P); f=figure('Color','w','Units','pixels','Position',[100 100 1600 900]); tiledlayout(1,2,'TileSpacing','compact','Padding','compact');
nexttile; vals=[P(idx);A(idx)*10;R(idx)]'; b=bar(vals,'grouped','BarWidth',0.75); b(1).FaceColor=blue; b(2).FaceColor=[0.30 0.62 0.45]; b(3).FaceColor=green;
set(gca,'XTick',1:4,'XTickLabel',{'ESCAPE','TAPE 0','TAPE 1','TAPE 3'},'FontSize',10,'LineWidth',1.1); xtickangle(18); ylabel('Standardized evidence value','FontSize',12); title('Released evidence components','FontSize',14,'FontWeight','bold'); legend({'P span (pp)','10 x A axis','R change (pp)'},'Location','northwest','Box','off','FontSize',9); grid on; box off;
nexttile; bar([4 4;4 4]','stacked','BarWidth',0.55); colormap(gca,[green;0.82 0.84 0.87]); set(gca,'XTick',1:2,'XTickLabel',{'Released cases','All primary endpoints'},'FontSize',10,'LineWidth',1.1); ylabel('Number of endpoints','FontSize',12); title('Coverage and directional agreement','FontSize',14,'FontWeight','bold'); ylim([0 9]); grid on; box off; legend({'Directional agreement / released','Abstained or not released'},'Location','northwest','Box','off','FontSize',9); text(1,2,'4/4 agreement','FontSize',10,'FontWeight','bold','HorizontalAlignment','center','Color','w'); text(2,2,'4/8 released','FontSize',10,'FontWeight','bold','HorizontalAlignment','center','Color','w');
exportgraphics(f,fullfile(outDir,'Figure_3.pdf'),'ContentType','vector','BackgroundColor','white');
exportgraphics(f,fullfile(outDir,'Figure_3.png'),'Resolution',300,'BackgroundColor','white'); close(f);
end
