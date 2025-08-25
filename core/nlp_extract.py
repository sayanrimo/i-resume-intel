import spacy
import re
from typing import Dict, Any, Optional, List

# This will now work because the model is installed from requirements.txt
nlp = spacy.load("en_core_web_sm")

# --- Comprehensive Skills Database for Data Roles ---

# 1. Programming, Databases, and Core Tools
programming_skills = [
    'python', 'r', 'sql', 'java', 'scala', 'c++', 'matlab', 'sas', 'bash', 'shell scripting'
]
database_skills = [
    'mysql', 'postgresql', 'sqlite', 'mssql', 'sql server', 'oracle', 'mongodb', 'cassandra',
    'redis', 'nosql', 't-sql', 'pl/sql'
]
tools_skills = [
    'git', 'github', 'gitlab', 'jupyter', 'jupyter notebook', 'rstudio', 'docker', 'kubernetes',
    'jira', 'confluence'
]

# 2. Data Science, Machine Learning & Analytics Libraries
python_ds_libs = [
    'pandas', 'numpy', 'scipy', 'scikit-learn', 'statsmodels', 'matplotlib', 'seaborn',
    'plotly', 'bokeh', 'dash', 'streamlit'
]
python_ml_dl_libs = [
    'tensorflow', 'keras', 'pytorch', 'theano', 'caffe', 'mxnet', 'fastai', 'xgboost',
    'lightgbm', 'catboost', 'opencv'
]
python_nlp_libs = [
    'nltk', 'spacy', 'gensim', 'textblob', 'transformers', 'hugging face'
]
python_big_data_libs = [
    'pyspark', 'dask', 'ray'
]
r_libs = [
    'dplyr', 'ggplot2', 'tidyr', 'shiny', 'caret'
]

# 3. Cloud Platforms & Big Data Technologies
cloud_platforms = [
    'aws', 'azure', 'gcp', 'google cloud', 'amazon web services'
]
aws_services = [
    's3', 'ec2', 'redshift', 'emr', 'sagemaker', 'glue', 'lambda', 'rds', 'athena', 'kinesis'
]
azure_services = [
    'blob storage', 'synapse analytics', 'data factory', 'databricks', 'azure ml'
]
gcp_services = [
    'bigquery', 'cloud storage', 'dataflow', 'dataproc', 'vertex ai', 'pub/sub'
]
big_data_tech = [
    'hadoop', 'hdfs', 'mapreduce', 'spark', 'kafka', 'flink', 'hive', 'presto', 'airflow',
    'snowflake', 'teradata'
]

# 4. BI, Visualization & Reporting
bi_tools = [
    'tableau', 'power bi', 'looker', 'qlik', 'spotfire', 'sisense', 'superset',
    'google data studio', 'excel'
]

# 5. Core Concepts and Methodologies
ml_concepts = [
    'machine learning', 'deep learning', 'supervised learning', 'unsupervised learning',
    'reinforcement learning', 'natural language processing', 'nlp', 'computer vision', 'cv',
    'regression', 'classification', 'clustering', 'time series analysis', 'forecasting'
]
stats_concepts = [
    'statistics', 'statistical analysis', 'hypothesis testing', 'a/b testing',
    'experimental design', 'bayesian statistics'
]
dev_concepts = [
    'agile', 'scrum', 'ci/cd', 'mlops'
]

# Combine all lists into the final SKILLS_DB
SKILLS_DB = (
    programming_skills + database_skills + tools_skills +
    python_ds_libs + python_ml_dl_libs + python_nlp_libs + python_big_data_libs + r_libs +
    cloud_platforms + aws_services + azure_services + gcp_services + big_data_tech +
    bi_tools + ml_concepts + stats_concepts + dev_concepts
)

def extract_name(doc: spacy.tokens.Doc) -> Optional[str]:
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return None

def extract_email(text: str) -> Optional[str]:
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else None

def extract_skills(text: str) -> List[str]:
    found_skills = set()
    unique_skills = set(skill.lower() for skill in SKILLS_DB) # Use a set for faster lookups

    for skill in unique_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.add(skill.title())
    return sorted(list(found_skills))

def extract_entities(raw_text: str) -> Dict[str, Any]:
    doc = nlp(raw_text)
    return {
        "name": extract_name(doc),
        "email": extract_email(raw_text),
        "skills": [{"name": skill} for skill in extract_skills(raw_text)],
    }