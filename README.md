# Stochastic Simulation of Gene Expression

A [Bokeh](https://bokeh.pydata.org/en/1.0.3/) dashboard for simulating gene expression with the [Gillespie Algorithm](https://en.wikipedia.org/wiki/Gillespie_algorithm)

![Screenshot](screenshot.png)

## How to use the dashboard

To launch the dashboard, open a command line interface, navigate to the directory containing the project's `SSgene.py` file, and run the command 

```
bokeh serve --show SSgene.py
```

The dashboard will automatically open in your browser at the address `http://localhost:5006/SSgene`

You can use the dashboard's interactive controls to tune reaction paramaters and visualize protein and mRNA behavior over time.

The **RESILMULATE** button will generate new data using the exisitng set of reaction parameters. 
* Simulation Length
* mRNA Synthesis Rate
* Protein Synthesis Rate
* mRNA Degradation Rate
* Protein Degradation Rate
* Initial DNA Count
* Initial mRNA Count
* Initial Proteim Count

These paramaters can be adjusted by clicking along their respective slider. (I would advise against dragging the slider, since this will run a string of new simulations.) 
