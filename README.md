# E-Commerce Data Analysis Dashboard

This repository contains a **Streamlit** application for analyzing e-commerce data. The dashboard provides insights into customer distribution, geographical patterns, and product category analysis.

## Features

- **Top Cities**: Displays the top cities with the highest concentration of customers.
- **Top States**: Highlights the states with the most customers.
- **Geographical Map**: Visualizes customer distribution across cities on an interactive map using Folium.
- **Product Category Analysis**: Analyzes and visualizes product categories by count and percentage.

## Live Demo

You can access the live application [here](https://ecommerce-customer-insights.streamlit.app/).

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/MushlihNur/ecommerce-data-analyst.git
   cd ecommerce-data-analyst
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   streamlit run dashboard/dashboard.py
   ```

## File Structure

```
├── dashboard
│   ├── dashboard.py
│   ├── all_data.csv
├── data
│   ├── all_data.csv
│   ├── customer_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
├── requirements.txt
├── notebook.ipynb
├── README.md
```

## Deployment

The application is deployed using **Streamlit Community Cloud**. Follow these steps to deploy your own version:

1. Push your repository to GitHub.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign in.
3. Create a new app and link it to your GitHub repository.
4. Specify the main file path as `dashboard/dashboard.py`.

## Example Visualizations

### 1. Top Cities
Bar chart showing cities with the highest customer counts.

### 2. Top States
Bar chart highlighting states with the highest customer counts.

### 3. Geographical Map
Interactive map visualizing customer distribution by city.

### 4. Product Categories
Pie and bar charts illustrating product category distribution.

## Contributions

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or suggestions, please contact [your email or GitHub profile].