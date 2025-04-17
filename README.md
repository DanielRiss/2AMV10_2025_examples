# 2AMV10 Example Code Tutorials
This repository provides examples for setting up your front-end visualization dashboard and the back-end logic to support it. You'll find code snippets for creating visualizations, running machine learning models, and structuring your project using recommended libraries and tools.

## Repository Structure

### `dashboards/`
Examples of interactive dashboard implementations.

- `dash_python/`: A simpler dashboard built with Plotly Dash in Python. Using Dash is perfectly fine and will work fine with almost all visualizations you want to include in your final project. However, if you would like to try your hand on a more advanced tool for creating dashboards, with a little more utility:
- `react_d3_flask/`: A more complex setup using a React + Vite + TypeScript front-end with D3.js for visualizations, and a Flask back-end.

### `eda/`
Data Cleaning and Exploratory Data Analysis examples using:
- `pandas` and `numpy` for data manipulation
- `matplotlib` and `seaborn` for visualization
This part is essential for cleaning your dataset and finding out interesting patterns in the data to visualize in your dashboard. It could also give you a good idea of machine learning methods from variables you want to explore further or predict.

### `machine_learning/`
Machine learning pipelines and interpretability tools:
- `torch_model.py`: A basic model implementation using PyTorch
- `train_pipeline.py`: Example of a simple training loop and evaluation
- `shap_explanation.ipynb`: Model explanation using SHAP (SHapley Additive exPlanations). Machine Learning visualizations are hard to come by, because most processes are so-called "black boxes". SHAP helps with this, and is a great tool to consider when trying to visualize *how* your machine learning implementation got to certain results.

### `assets/`
Images and visual assets used throughout the README files (e.g., charts, dashboard previews, SHAP plots).


## How to Use

Each section includes:
- A dedicated `README.md` explaining the purpose and setup
- Code files or notebooks you can run directly
- Tips for extensions or variations

To get started, clone this repo and explore the folders that interest you:
```bash
git clone https://github.com/yourusername/dashboard-tutorials.git
cd dashboard-tutorials
```

## Requirements

Most examples use common Python libraries like:
- `pandas`, `numpy`, `matplotlib`, `seaborn`
- `torch`, `shap`, `dash`, `flask`
- `node`, `vite`, `react`, `typescript` (for advanced front-end examples)

See individual folders for setup instructions and `requirements.txt` files.

---

## Contributions

Feel free to email us (Nora Bouwman, Daniël Ris) with any examples that you might want explained further. Also, if you do find problems with the code, let us know!
