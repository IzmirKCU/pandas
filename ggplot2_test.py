import plotnine as p9
import pandas as pd

surveys_complete = pd.read_csv('data/surveys.csv')
surveys_complete = surveys_complete.dropna()

p = (p9.ggplot(data=surveys_complete,
           mapping=p9.aes(x='weight',
                          y='hindfoot_length',
                          color='species_id'))
    + p9.geom_point(alpha=0.1) + p9.labs(title= "bunny")
)


p.save(filename = 'test3.png', height=5, width=5, units = 'in', dpi=1000)