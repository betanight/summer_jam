import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_usa_heatmap():
    df = pd.read_csv("processed_roadside_attractions.csv")
    
    state_counts = df['state'].value_counts()
    
    state_data = []
    for state_abbr, count in state_counts.items():
        state_data.append({
            'state': state_abbr,
            'attractions': count,
            'density': count
        })
    
    state_df = pd.DataFrame(state_data)
    
    print(f"Creating heatmap for {len(state_df)} states...")
    print(f"Attraction range: {state_df['attractions'].min()} - {state_df['attractions'].max()}")
    
    fig = px.choropleth(
        state_df,
        locations='state',
        locationmode='USA-states',
        color='attractions',
        hover_data=['attractions'],
        color_continuous_scale='Reds',
        title='USA Roadside Attractions Heatmap',
        labels={'attractions': 'Number of Attractions'},
        range_color=[0, state_df['attractions'].max()]
    )
    
    fig.update_layout(
        title={
            'text': 'USA Roadside Attractions Heatmap<br><sub>Darker red = More attractions</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24}
        },
        geo=dict(
            scope='usa',
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showcoastlines=True,
            coastlinecolor='rgb(204, 204, 204)',
            projection_type='albers usa'
        ),
        height=600,
        margin=dict(l=0, r=0, t=80, b=0)
    )
    
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>" +
                     "Attractions: %{z}<br>" +
                     "<extra></extra>"
    )
    
    fig.write_html("usa_attractions_heatmap.html")
    print("Heatmap saved as: usa_attractions_heatmap.html")
    
    print("\n" + "="*50)
    print("USA ATTRACTIONS HEATMAP SUMMARY")
    print("="*50)
    
    print(f"\nTotal States: {len(state_df)}")
    print(f"Total Attractions: {state_df['attractions'].sum():,}")
    print(f"Average per State: {state_df['attractions'].mean():.1f}")
    print(f"Median per State: {state_df['attractions'].median():.1f}")
    
    print(f"\nTop 10 States (Hottest):")
    top_states = state_df.nlargest(10, 'attractions')
    for _, row in top_states.iterrows():
        print(f"  {row['state']}: {row['attractions']:,} attractions")
    
    print(f"\nBottom 10 States (Coolest):")
    bottom_states = state_df.nsmallest(10, 'attractions')
    for _, row in bottom_states.iterrows():
        print(f"  {row['state']}: {row['attractions']:,} attractions")
    
    print("="*50)
    
    return fig

def create_detailed_analysis():
    df = pd.read_csv("processed_roadside_attractions.csv")
    
    category_counts = df['category'].value_counts()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Attractions by Category', 'Top 15 States'),
        specs=[[{"type": "pie"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            name="Categories"
        ),
        row=1, col=1
    )
    
    top_states = df['state'].value_counts().head(15)
    fig.add_trace(
        go.Bar(
            x=top_states.index,
            y=top_states.values,
            name="States",
            marker_color='red'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Roadside Attractions Analysis",
        title_x=0.5,
        title_font_size=20,
        showlegend=False,
        height=500
    )
    
    fig.write_html("attractions_analysis.html")
    print("Analysis saved as: attractions_analysis.html")

def main():
    print("Creating USA Attractions Heatmap...")
    
    heatmap_fig = create_usa_heatmap()
    create_detailed_analysis()
    
    print("\n✅ Complete! You now have:")
    print("  • usa_attractions_heatmap.html - Single USA heatmap")
    print("  • attractions_analysis.html - Category breakdown")
    print("  • processed_roadside_attractions.csv - Clean data")

if __name__ == "__main__":
    main() 