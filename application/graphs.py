#Project Jan Kardaszewicz 

#import libraries
from data_prep import *
import plotly.express as px


"""Graph functions"""
class Display_Graph(Display_Data):
    """
    Class managing Display Application Graphs.
    """
    def __init__(self, price_range: list[float], area_range:list[float]) -> None:
        """
        Function initalize Display Data.

        Args:
            price_range (list[float]): chosen price range
            area_range (list[float]): chosen area range
        """
        super().__init__(price_range, area_range)
        
        
    def initial_display(self, size: str = "Powierzchnia", on_administrative_layer: bool = False):
        """
        Initial graph figure creation for display layout.
        
        :param size: determines what size of points on graph should be set by
        :type size: string, optional
        :param on_administrative_layer: determines if the administrative_layout is displayed or not
        :type on_administrative_layer: bool, optional

        Returns:
            plotly.express: initial figure
        """

        fig = px.scatter_mapbox(self.DF, lat="lat", lon="lon", size=size, color="Dzielnica", color_discrete_map=self.set_colors(), size_max=15, zoom=10.5, hover_name="Dzielnica",
                mapbox_style= self.MAPBOX_STYLE, width=1900, height=775, center = self.CRACOW_CENTER)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(mapbox={
            "layers": [{
            "sourcetype": "geojson",
            "type": "fill",
            "opacity": 0.2,
            "fill":{"outlinecolor":"blue"},
            "color": "royalblue",
            "below": "traces",
            "name": self.GJ["features"][0]["properties"]["nazwa"],
            "source":self.GJ,
            "visible": on_administrative_layer}]
        })
        return fig
    
class Analysis_Graph(Analysis_Data):
    """
    Class managing Analysis Appliaction Graphs.
    """
    
    def __init__(self, city_part: list[str]) -> None:
        """
        Function to initialize Analysis Data.

        Args:
            city_part (list[str]): chosen districts
        """
        super().__init__(city_part)
        self.city_part = city_part
        
    def city_part_graph(self):
        """
        Function displaying chosen cityparts data.
        
        Returns:
            plotly.express: created figure
        """
        
        fig = px.scatter_mapbox(self.DF, lat="lat", lon="lon", size="Cena", color="Dzielnica", color_discrete_map=self.set_colors(), size_max=15, zoom=10.2, hover_name="Dzielnica",
                mapbox_style=self.MAPBOX_STYLE, width=925, height=450, center = self.CRACOW_CENTER)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        fig.update_layout(mapbox={
                    "layers": [{
                    "sourcetype": "geojson",
                    "type": "fill",
                    "opacity": 0.2,
                    "fill":{"outlinecolor":"blue"},
                    "color": "royalblue",
                    "below": "traces",
                    "source": self.GJ,
                    "visible": True}]
                })
        return fig    

    def choropleth_graph(self):
        """Choropleth analysis graph displaying mean price of each district.

        Returns:
            plotly.express: choropleth graph
        """
        df = self.return_mean_df()
        fig = px.choropleth_mapbox(df, geojson=self.GJ, color="srednia_cena",
                            locations="Dzielnica",featureidkey="properties.nazwa",
                            mapbox_style=self.MAPBOX_STYLE, zoom=10,center = self.CRACOW_CENTER, labels={"name": "Dzielnica"}, width=925, height=450)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig    

    def bar_price_graph(self): 
        """
        Function displaying bar graph of mean price for m2 for district.

        :param df: analysis mean DataFrame instance sorted by srednia cena za m2
        :type df: DataFrame

        Returns:
            plotly.express: Bar graph
        """ 
        df = self.return_mean_df().sort_values(by="srednia_cena_za_m2")
        fig = px.bar(df, x="Dzielnica", y="srednia_cena_za_m2", title="Średnia cena za metr kwardatowy względem dzielnic", height=400,width=1250)
        fig.update_traces(marker_color="blue")
        highlighted_color = "blue"
        colors = [highlighted_color if cat in self.city_part else "lightskyblue" for cat in df["Dzielnica"]]
        fig.update_traces(marker_color=colors)    

        return fig
    
    
    def bar_area_graph(self): 
        """
        Function displaying bar graph of mean area for district.

        :param df: analysis mean DataFrame instance sorted by srednia powierzchnia
        :type df: DataFrame

        Returns:
            plotly.express: Bar graph
        """
        df = self.return_mean_df().sort_values(by="srednia_powierzchnia")
        fig = px.bar(df, x="srednia_powierzchnia", y="Dzielnica", title="Średnia powierzchnia mieszkania względem dzielnic", height=450, width=950, orientation="h")
        fig.update_traces(marker_color="indigo")
        highlighted_color = "indigo"
        colors = [highlighted_color if cat in self.city_part else "mediumorchid" for cat in df["Dzielnica"]]
        fig.update_traces(marker_color=colors)
        
        return fig
    
    def bar_mean_graph_area(self):
        """
        Function displaying bar graph of combined mean area for every chosen district.
        
        Returns:
            plotly.express: Bar graphs of mean area for chosen districts
        """
        mean_df, mean_value = self.choose_mean_df("srednia_powierzchnia")
        fig = px.bar(mean_df, x="Wartość", y= "Aktualna średnia",color="Wartość", color_discrete_map={"Wartość": "red"},title=f"Średnia powierzchnia: {mean_value:.2f} [m²]" , height=400,width=310)
        fig.update_layout(showlegend=False)
        fig.update_yaxes(range=[50, 100])
        
        return fig
    
    def bar_mean_graph_price(self):
        """
        Function displaying bar graph of combined mean price for m2 for every chosen district.

        Returns:
            plotly.express: Bar graphs of mean price for chosen districts
        """
        mean_df, mean_value = self.choose_mean_df("srednia_cena_za_m2")
        fig = px.bar(mean_df, x="Wartość", y= "Aktualna średnia", title=f"Średnia cena: {mean_value:.2f} [zł/m²]", height=400,width=310)
        fig.update_yaxes(range=[8000, 25000])
        
        return fig

    
