from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load and preprocess data
def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath)
    df['salary_in_usd'] = pd.to_numeric(df['salary_in_usd'], errors='coerce')
    df = df.dropna()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    categorical_cols = ['experience_level', 'employment_type', 'job_title', 'employee_residence', 'work_setting', 'company_location', 'company_size', 'job_category']
    df[categorical_cols] = df[categorical_cols].astype('category')
    experience_order = ['Entry-level', 'Mid-level', 'Senior', 'Executive']
    df['experience_level'] = pd.Categorical(df['experience_level'], categories=experience_order, ordered=True)
    return df

# Load your data
df = load_and_preprocess_data('data.csv')

# Utility function to encode plots as base64
def encode_plot(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

@app.route('/basic_statistics', methods=['GET'])
def basic_statistics():
    stats = df.describe(include='all').to_dict()
    return jsonify(stats)

@app.route('/job_counts_by_experience_level', methods=['GET'])
def job_counts_by_experience_level():
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='experience_level')
    plt.title('Job Counts by Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/average_salary_by_experience_level', methods=['GET'])
def average_salary_by_experience_level():
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='experience_level', y='salary_in_usd', estimator='mean')
    plt.title('Average Salary by Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})



@app.route('/average_salary_by_work_setting', methods=['GET'])
def average_salary_by_work_setting():
    avg_salary_by_setting = df.groupby('work_setting')['salary_in_usd'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_salary_by_setting.index, y=avg_salary_by_setting.values)
    plt.title('Average Salary by Work Setting')
    plt.xticks(rotation=45)
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/salary_distribution_by_job_category', methods=['GET'])
def salary_distribution_by_job_category():
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x='job_category', y='salary_in_usd')
    plt.xticks(rotation=90)
    plt.title('Salary Distribution by Job Category')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/pie_chart_experience_level', methods=['GET'])
def pie_chart_experience_level():
    experience_counts = df['experience_level'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(experience_counts, labels=experience_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title('Job Distribution by Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/heatmap_salary_by_job_category', methods=['GET'])
def heatmap_salary_by_job_category():
    pivot_table = df.pivot_table(values='salary_in_usd', index='job_category', columns='experience_level', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, cmap='coolwarm', fmt='.0f')
    plt.title('Heatmap of Average Salary by Job Category and Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})



if __name__ == '__main__':
    app.run(debug=True)

