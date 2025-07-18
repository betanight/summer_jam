"""
Visualization utilities for route optimization results.
Creates interactive plots using plotly for web integration.
"""

import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class RouteVisualizer:
    """
    Visualization class for route optimization results.
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        self.colors = {
            'baseline': '#FF6B6B',
            'optimized': '#4ECDC4',
            'locations': '#45B7D1',
            'route_line': '#2C3E50'
        }
    
    def create_route_map(self, coordinates: np.ndarray, location_names: List[str],
                        baseline_route: List[int], optimized_route: List[int],
                        baseline_distance: float, optimized_distance: float) -> go.Figure:
        """
        Create an interactive map showing both baseline and optimized routes.
        
        Args:
            coordinates (np.ndarray): Location coordinates
            location_names (List[str]): Names of locations
            baseline_route (List[int]): Baseline route indices
            optimized_route (List[int]): Optimized route indices
            baseline_distance (float): Baseline route distance
            optimized_distance (float): Optimized route distance
            
        Returns:
            go.Figure: Interactive map figure
        """
        # Create base map
        fig = go.Figure()
        
        # Add location markers
        fig.add_trace(go.Scattergeo(
            lon=coordinates[:, 1],
            lat=coordinates[:, 0],
            mode='markers+text',
            text=location_names,
            textposition="top center",
            marker=dict(
                size=10,
                color=self.colors['locations'],
                line=dict(width=2, color='white')
            ),
            name='Locations',
            showlegend=True
        ))
        
        # Add baseline route
        baseline_coords = coordinates[baseline_route]
        fig.add_trace(go.Scattergeo(
            lon=baseline_coords[:, 1],
            lat=baseline_coords[:, 0],
            mode='lines+markers',
            line=dict(width=3, color=self.colors['baseline'], dash='dash'),
            marker=dict(size=8, color=self.colors['baseline']),
            name=f'Baseline Route ({baseline_distance:.1f} km)',
            showlegend=True
        ))
        
        # Add optimized route
        optimized_coords = coordinates[optimized_route]
        fig.add_trace(go.Scattergeo(
            lon=optimized_coords[:, 1],
            lat=optimized_coords[:, 0],
            mode='lines+markers',
            line=dict(width=3, color=self.colors['optimized']),
            marker=dict(size=8, color=self.colors['optimized']),
            name=f'Optimized Route ({optimized_distance:.1f} km)',
            showlegend=True
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Summer Activity Route Optimization',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            geo=dict(
                scope='europe',
                projection_type='equirectangular',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(204, 229, 255)',
                showcountries=True,
                countrycolor='rgb(255, 255, 255)',
                showframe=False
            ),
            height=600,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        return fig
    
    def create_distance_comparison(self, baseline_distance: float, optimized_distance: float) -> go.Figure:
        """
        Create a bar chart comparing baseline and optimized distances.
        
        Args:
            baseline_distance (float): Baseline route distance
            optimized_distance (float): Optimized route distance
            
        Returns:
            go.Figure: Bar chart figure
        """
        routes = ['Baseline (Random)', 'Optimized (GA)']
        distances = [baseline_distance, optimized_distance]
        colors = [self.colors['baseline'], self.colors['optimized']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=routes,
                y=distances,
                marker_color=colors,
                text=[f'{d:.1f} km' for d in distances],
                textposition='auto',
            )
        ])
        
        improvement = ((baseline_distance - optimized_distance) / baseline_distance) * 100
        
        fig.update_layout(
            title={
                'text': f'Route Distance Comparison (Improvement: {improvement:.1f}%)',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='Route Type',
            yaxis_title='Total Distance (km)',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_optimization_progress(self, progress_data: List[float]) -> go.Figure:
        """
        Create a line chart showing optimization progress over generations.
        
        Args:
            progress_data (List[float]): List of best distances per generation
            
        Returns:
            go.Figure: Line chart figure
        """
        generations = list(range(len(progress_data)))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=generations,
            y=progress_data,
            mode='lines',
            line=dict(color=self.colors['optimized'], width=3),
            name='Best Distance'
        ))
        
        fig.update_layout(
            title='Optimization Progress Over Generations',
            xaxis_title='Generation',
            yaxis_title='Best Distance (km)',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_route_statistics(self, baseline_stats: Dict, optimized_stats: Dict) -> go.Figure:
        """
        Create a comprehensive statistics dashboard.
        
        Args:
            baseline_stats (Dict): Baseline route statistics
            optimized_stats (Dict): Optimized route statistics
            
        Returns:
            go.Figure: Subplot figure with multiple charts
        """
        # Create subplots
        fig = sp.make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distance Comparison', 'Segment Analysis', 
                          'Improvement Metrics', 'Route Efficiency'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "indicator"}, {"type": "pie"}]]
        )
        
        # Distance comparison
        routes = ['Baseline', 'Optimized']
        distances = [baseline_stats['total_distance'], optimized_stats['total_distance']]
        colors = [self.colors['baseline'], self.colors['optimized']]
        
        fig.add_trace(
            go.Bar(x=routes, y=distances, marker_color=colors, name='Distance'),
            row=1, col=1
        )
        
        # Segment analysis
        baseline_segments = baseline_stats.get('segment_distances', [])
        optimized_segments = optimized_stats.get('segment_distances', [])
        
        fig.add_trace(
            go.Scatter(x=list(range(len(baseline_segments))), y=baseline_segments,
                      mode='lines+markers', name='Baseline Segments', line=dict(color=self.colors['baseline'])),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=list(range(len(optimized_segments))), y=optimized_segments,
                      mode='lines+markers', name='Optimized Segments', line=dict(color=self.colors['optimized'])),
            row=1, col=2
        )
        
        # Improvement indicator
        improvement = ((baseline_stats['total_distance'] - optimized_stats['total_distance']) / 
                     baseline_stats['total_distance']) * 100
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=optimized_stats['total_distance'],
                delta={'reference': baseline_stats['total_distance']},
                gauge={'axis': {'range': [None, baseline_stats['total_distance']]},
                       'bar': {'color': self.colors['optimized']},
                       'steps': [{'range': [0, baseline_stats['total_distance']], 'color': "lightgray"}]},
                title={'text': f"Distance Improvement ({improvement:.1f}%)"}
            ),
            row=2, col=1
        )
        
        # Route efficiency pie chart
        efficiency_data = [optimized_stats['total_distance'], 
                         baseline_stats['total_distance'] - optimized_stats['total_distance']]
        efficiency_labels = ['Optimized Distance', 'Distance Saved']
        efficiency_colors = [self.colors['optimized'], self.colors['baseline']]
        
        fig.add_trace(
            go.Pie(labels=efficiency_labels, values=efficiency_data, 
                   marker_colors=efficiency_colors, name='Efficiency'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Route Optimization Statistics")
        
        return fig
    
    def create_interactive_dashboard(self, coordinates: np.ndarray, location_names: List[str],
                                   baseline_results: Dict, optimized_results: Dict) -> go.Figure:
        """
        Create a comprehensive interactive dashboard.
        
        Args:
            coordinates (np.ndarray): Location coordinates
            location_names (List[str]): Location names
            baseline_results (Dict): Baseline experiment results
            optimized_results (Dict): Optimization results
            
        Returns:
            go.Figure: Complete dashboard
        """
        # Create subplots
        fig = sp.make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "scattergeo"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "indicator"}]],
            subplot_titles=('Route Map', 'Distance Comparison', 
                          'Optimization Progress', 'Performance Metrics')
        )
        
        # Route map
        baseline_route = baseline_results['best_route']
        optimized_route = optimized_results['best_route']
        baseline_distance = baseline_results['best_distance']
        optimized_distance = optimized_results['best_distance']
        
        # Add locations
        fig.add_trace(
            go.Scattergeo(
                lon=coordinates[:, 1],
                lat=coordinates[:, 0],
                mode='markers+text',
                text=location_names,
                textposition="top center",
                marker=dict(size=8, color=self.colors['locations']),
                name='Locations',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Add routes
        baseline_coords = coordinates[baseline_route]
        optimized_coords = coordinates[optimized_route]
        
        fig.add_trace(
            go.Scattergeo(
                lon=baseline_coords[:, 1],
                lat=baseline_coords[:, 0],
                mode='lines',
                line=dict(width=2, color=self.colors['baseline'], dash='dash'),
                name='Baseline',
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scattergeo(
                lon=optimized_coords[:, 1],
                lat=optimized_coords[:, 0],
                mode='lines',
                line=dict(width=2, color=self.colors['optimized']),
                name='Optimized',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Distance comparison
        routes = ['Baseline', 'Optimized']
        distances = [baseline_distance, optimized_distance]
        colors = [self.colors['baseline'], self.colors['optimized']]
        
        fig.add_trace(
            go.Bar(x=routes, y=distances, marker_color=colors, name='Distance'),
            row=1, col=2
        )
        
        # Optimization progress
        progress = optimized_results.get('best_distances', [])
        generations = list(range(len(progress)))
        
        fig.add_trace(
            go.Scatter(x=generations, y=progress, mode='lines',
                      line=dict(color=self.colors['optimized']), name='Progress'),
            row=2, col=1
        )
        
        # Performance indicator
        improvement = ((baseline_distance - optimized_distance) / baseline_distance) * 100
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=optimized_distance,
                delta={'reference': baseline_distance},
                gauge={'axis': {'range': [None, baseline_distance]},
                       'bar': {'color': self.colors['optimized']},
                       'steps': [{'range': [0, baseline_distance], 'color': "lightgray"}]},
                title={'text': f"Improvement: {improvement:.1f}%"}
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title='Summer Activity Route Optimization Dashboard',
            height=800,
            geo=dict(
                scope='europe',
                projection_type='equirectangular',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(204, 229, 255)',
                showcountries=True,
                countrycolor='rgb(255, 255, 255)',
                showframe=False
            )
        )
        
        return fig

def save_interactive_plots(visualizer: RouteVisualizer, coordinates: np.ndarray, 
                          location_names: List[str], baseline_results: Dict, 
                          optimized_results: Dict, output_dir: str = "outputs"):
    """
    Save all interactive plots as HTML files for web integration.
    
    Args:
        visualizer (RouteVisualizer): Visualizer instance
        coordinates (np.ndarray): Location coordinates
        location_names (List[str]): Location names
        baseline_results (Dict): Baseline results
        optimized_results (Dict): Optimization results
        output_dir (str): Output directory for HTML files
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Create route map
    route_map = visualizer.create_route_map(
        coordinates, location_names,
        baseline_results['best_route'], optimized_results['best_route'],
        baseline_results['best_distance'], optimized_results['best_distance']
    )
    route_map.write_html(f"{output_dir}/route_map.html")
    
    # Create distance comparison
    distance_chart = visualizer.create_distance_comparison(
        baseline_results['best_distance'], optimized_results['best_distance']
    )
    distance_chart.write_html(f"{output_dir}/distance_comparison.html")
    
    # Create optimization progress
    if 'best_distances' in optimized_results:
        progress_chart = visualizer.create_optimization_progress(
            optimized_results['best_distances']
        )
        progress_chart.write_html(f"{output_dir}/optimization_progress.html")
    
    # Create statistics dashboard
    stats_dashboard = visualizer.create_route_statistics(
        baseline_results, optimized_results
    )
    stats_dashboard.write_html(f"{output_dir}/statistics_dashboard.html")
    
    # Create comprehensive dashboard
    main_dashboard = visualizer.create_interactive_dashboard(
        coordinates, location_names, baseline_results, optimized_results
    )
    main_dashboard.write_html(f"{output_dir}/main_dashboard.html")
    
    logger.info(f"All interactive plots saved to {output_dir}/") 