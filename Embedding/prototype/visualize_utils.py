import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity

from bokeh.io import export_png
from bokeh.plotting import figure
from bokeh.models import Plot, LinearColorMapper, ColumnDataSource, LabelSet, BasicTicker, ColorBar

from selenium import webdriver

def visualize_words(words, vecs, palette="Viridis256", filename="/notebooks/embedding/words.png",
                    use_notebook=False):
    tsne = TSNE(n_components=2)
    tsne_results = tsne.fit_transform(vecs)
    df = pd.DataFrame(columns=['x', 'y', 'word'])
    df['x'], df['y'], df['word'] = tsne_results[:, 0], tsne_results[:, 1], list(words)
    source = ColumnDataSource(ColumnDataSource.from_df(df))
    labels = LabelSet(x="x", y="y", text="word", y_offset=8,
                      text_font_size="15pt", text_color="#555555",
                      source=source, text_align='center')
    color_mapper = LinearColorMapper(palette=palette, low=min(tsne_results[:, 1]), high=max(tsne_results[:, 1]))
    plot = figure(plot_width=900, plot_height=900)
    plot.scatter("x", "y", size=12, source=source, color={'field': 'y', 'transform': color_mapper}, line_color=None,
                 fill_alpha=0.8)
    plot.add_layout(labels)

    driver = webdriver.Chrome('./chromedriver')
    export_png(plot, webdriver=driver)
    print("save @ " + filename)


def visualize_between_words(words, vecs, palette="Viridis256", filename="/notebooks/embedding/between-words.png",
                            use_notebook=False):
    df_list = []
    for word1_idx, word1 in enumerate(words):
        for word2_idx, word2 in enumerate(words):
            vec1 = vecs[word1_idx]
            vec2 = vecs[word2_idx]
            if np.any(vec1) and np.any(vec2):
                score = cosine_similarity(X=[vec1], Y=[vec2])
                df_list.append({'x': word1, 'y': word2, 'similarity': score[0][0]})
    df = pd.DataFrame(df_list)
    color_mapper = LinearColorMapper(palette=palette, low=1, high=0)
    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
    p = figure(x_range=list(words), y_range=list(reversed(list(words))),
               x_axis_location="above", plot_width=900, plot_height=900,
               toolbar_location='below', tools=TOOLS,
               tooltips=[('words', '@x @y'), ('similarity', '@similarity')])
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = 3.14 / 3
    p.rect(x="x", y="y", width=1, height=1,
           source=df,
           fill_color={'field': 'similarity', 'transform': color_mapper},
           line_color=None)
    color_bar = ColorBar(ticker=BasicTicker(desired_num_ticks=5),
                         color_mapper=color_mapper, major_label_text_font_size="7pt",
                         label_standoff=6, border_line_color=None, location=(0, 0))
    p.add_layout(color_bar, 'right')

    driver = webdriver.Chrome('./chromedriver')
    export_png(p, webdriver=driver)
    print("save @ " + filename)
