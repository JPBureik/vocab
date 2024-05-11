def create_radial_chart(df, figsize, fontsize, color_theme = 'Purple'):
    #######################################################################
    ###                                                        LIBRARIES                                                            ###
    #######################################################################
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    #######################################################################
    ###                                                    HELPER FUNCTIONS                                                ###
    #######################################################################

    #USE: Create an array structure for rings.
    #INPUT: a df of row length 1 with the first column as the current metric value and the second colum is the target metric value
    #OUTPUT: an aray of arrays representing each ring
    def calculate_rings(df):
      if df.iloc[0,0] < df.iloc[0,1]:
        rings=[[df.iloc[0,0],df.iloc[0,1]-df.iloc[0,0]],[0,0]]
      elif df.iloc[0,0] / df.iloc[0,1] < 2:
        rings=[[df.iloc[0,0],0],[df.iloc[0,0] % df.iloc[0,1], df.iloc[0,1]-df.iloc[0,0] % df.iloc[0,1]]]
      else:
        rings = [[0,0],[0,0]]
      return rings

    #USE: Determine if the label for the rotating number label should be left/center/right
    #INPUT: a df of row length 1 with the first column as the current metric value and the second colum is the target metric value
    #OUTPUT: the proper text alignment
    def horizontal_aligner(df):
      metric = 1.0 * df.iloc[0,0] % df.iloc[0,1] / df.iloc[0,1]
      if metric in (0, 0.5):
        align = 'center'
      elif metric < 0.5:
        align = 'left'
      else:
        align = 'right'
      return align

    def vertical_aligner(df):
      metric = 1.0 * df.iloc[0,0] % df.iloc[0,1] / df.iloc[0,1]
      if metric < 0.25:
        align = 'bottom'
      elif metric < 0.75:
        align = 'top'
      elif metric > 0.75:
        align = 'bottom'
      else:
        align = 'center'
      return align

    #USE: Create a center label in the middle of the radial chart.
    #INPUT: a df of row length 1 with the first column as the current metric value and the second column is the target metric value
    #OUTPUT: the proper text label
    def add_center_label(df):
        if df.iloc[0, 0] < df.iloc[0, 1]:
            phase_label = str(int(df.iloc[0, 0]))
        else:
            phase_label = 'LTM'
        return plt.text(0,
               -0.02,
               phase_label,
               horizontalalignment='center',
               verticalalignment='center',
               fontsize = fontsize,
               family = 'sans-serif', color=neongreen)

    #USE: Formats a number with the apropiate currency tags.
    #INPUT: a currency number
    #OUTPUT: the properly formmated currency string
    def get_currency_label(num):
      currency = ''
      if num < 6:
        currency = 'Phase ' + str(num)

      return currency

    #USE: Create a dynamic outer label that servers a pointer on the ring.
    #INPUT: a df of row length 1 with the first column as the current metric value and the second column is the target metric value
    #OUTPUT: the proper text label at the apropiate position
    def add_current_label(df):
      currency = get_currency_label(df.iloc[0,0])
      print('vertical: ' + vertical_aligner(df))
      print('horizontal: ' + horizontal_aligner(df))
      return plt.text(1.5 * np.cos(0.5 *np.pi - 2 * np.pi * (float(df.iloc[0,0]) % df.iloc[0,1] /df.iloc[0,1])),
               1.5 * np.sin(0.5 *np.pi - 2 * np.pi * (float(df.iloc[0,0]) % df.iloc[0,1] / df.iloc[0,1])),
                      currency,
                      horizontalalignment=horizontal_aligner(df),
                      verticalalignment=vertical_aligner(df),
                      fontsize = 20,
                      family = 'sans-serif', color=neongreen)

    def add_sub_center_label(df):
        amount = 'Goal: ' + get_currency_label(df.iloc[0,1])
        return plt.text(0,
                -.1,
                amount,
                horizontalalignment='center',
                verticalalignment='top',
                fontsize = 22,family = 'sans-serif', color=neongreen)

    #######################################################################
    ###                                                    MAIN FUNCTION                                                        ###
    #######################################################################


    # base styling logic
    color = plt.get_cmap(color_theme + 's')
    ring_width = 0.06
    outer_radius = 0.2
    inner_radius = outer_radius - ring_width
    
    # set up plot
    ring_arrays = calculate_rings(df)
    fig, ax = plt.subplots(figsize=figsize)
    
    if df.iloc[0, 0] > df.iloc[0, 1]:
        ring_to_label = 0
        outer_edge_color = None
        inner_edge_color = 'darkslategrey'
    else:
        ring_to_label = 1
        outer_edge_color, inner_edge_color = ['darkslategrey', None]
        
    neongreen = tuple(i / 255 for i in (11, 225, 110, 255))
    
    # plot logic
    outer_ring, _ = ax.pie(ring_arrays[0],radius=outer_radius,
                        colors=[neongreen, 'darkslategrey'],
                        startangle = 90,
                        counterclock = False)
    plt.setp( outer_ring, width=ring_width, edgecolor=outer_edge_color)
    
    inner_ring, _ = ax.pie(ring_arrays[1],
                             radius=inner_radius,
                             colors=['k', 'k'],
                             startangle = 90,
                             counterclock = False)
    plt.setp(inner_ring, width=ring_width, edgecolor=inner_edge_color)
    
    # add labels and format plots
    add_center_label(df)
#    add_current_label(df)
#    add_sub_center_label(df)
    ax.axis('equal')
    plt.margins(0,0)
#    plt.autoscale('enable')
    plt.show()
    return fig