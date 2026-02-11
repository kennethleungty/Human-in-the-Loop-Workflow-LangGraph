"""Utility functions for the workflow"""

from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def save_mermaid_diagram(graph, output_path: str = "assets/graph_setup.png"):
    """Save the workflow graph visualization to a file.

    Args:
        graph: The compiled LangGraph to visualize
        output_path: Path to save the visualization PNG
    """
    try:
        # Create directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Generate visualization using LangGraph's built-in method
        graph_png = graph.get_graph(xray=True).draw_mermaid_png()
        with open(output_path, "wb") as f:
            f.write(graph_png)
        logger.info(f"Mermaid diagram saved to: {output_path}")
        print(f"Graph visualization saved to: {output_path}")
    except Exception as e:
        logger.error(f"Could not generate diagram: {e}")
        print(f"Warning: Could not generate diagram: {e}")
