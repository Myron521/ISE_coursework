# -*- coding: utf-8 -*-
"""tensorflow_improved.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SDBXrhPC3A4fMwb_5dXaJzEUXgbCgSUY
"""

# 克隆整个仓库到Colab环境
!git clone https://github.com/ideas-labo/ISE-solution.git

# 查看克隆下来的lab2文件夹结构，以确认克隆成功
import os
lab1_path = '/content/ISE-solution/lab1'
if os.path.exists(lab1_path):
    print("lab1文件夹克隆成功，文件夹内容如下：")
    for root, dirs, files in os.walk(lab1_path):
        level = root.replace(lab1_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(sub_indent, f))
else:
    print("lab1文件夹克隆失败，请检查网络或仓库地址。")

import pandas as pd
import numpy as np
import re
import math
import os

# Text and feature engineering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc

# Text cleaning & stopwords
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Data balancing
from imblearn.over_sampling import SMOTE

########## 2. Define text preprocessing methods ##########
stemmer = PorterStemmer()

def remove_html(text):
    """Remove HTML tags using a regex."""
    html = re.compile(r'<.*?>')
    return html.sub(r'', text)

def remove_emoji(text):
    """Remove emojis using a regex pattern."""
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"  # enclosed characters
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

NLTK_stop_words_list = stopwords.words('english')
# 根据tensorflow项目特点添加可能的停用词
custom_stop_words_list = ['...', 'tensorflow', 'tensor', 'model', 'layer', 'function']
final_stop_words_list = NLTK_stop_words_list + custom_stop_words_list

def remove_stopwords(text):
    """Remove stopwords and technical terms from the text."""
    return " ".join([word for word in str(text).split() if word not in final_stop_words_list])

def clean_str(string):
    """
    Clean text by removing non-alphanumeric characters,
    handling special cases, and converting to lowercase.
    """
    string = re.sub(r"[^A-Za-z0-9(),.!?\'\`]", " ", string)
    string = re.sub(r"\r\n|\n|\r", " ", string)  # Handle newlines
    string = re.sub(r"\s{2,}", " ", string)       # Collapse multiple spaces
    string = re.sub(r"\\", "", string)            # Remove backslashes
    string = re.sub(r"\'", "", string)            # Remove apostrophes
    string = re.sub(r"\"", "", string)            # Remove quotes
    return string.strip().lower()

########## 3. Download & read data ##########
project = 'tensorflow'
input_path = '/content/ISE-solution/lab1/datasets/tensorflow.csv'
output_dir = '/content/ISE-solution/lab1/results'

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

pd_all = pd.read_csv(input_path)
pd_all = pd_all.sample(frac=1, random_state=999)  # Shuffle

# Merge Title and Body
pd_all['Title+Body'] = pd_all.apply(
    lambda row: row['Title'] + '. ' + row['Body'] if pd.notna(row['Body']) else row['Title'],
    axis=1
)

pd_tplusb = pd_all.rename(columns={
    "Unnamed: 0": "id",
    "class": "sentiment",
    "Title+Body": "text"
})

########## 4. Configure parameters & Start training ##########

# ========== Key Configurations ==========
datafile = 'Title+Body.csv'
REPEAT = 30
out_csv_name = os.path.join(output_dir, f'{project}_improved.csv')

# ========== Read and clean data ==========
data = pd.read_csv(datafile).fillna('')
text_col = 'text'

# Text cleaning pipeline
data[text_col] = data[text_col].apply(remove_html)
data[text_col] = data[text_col].apply(remove_emoji)
data[text_col] = data[text_col].apply(remove_stopwords)
data[text_col] = data[text_col].apply(clean_str)
data[text_col] = data[text_col].apply(lambda x: " ".join([stemmer.stem(word) for word in x.split()]))  # Stemming

# ========== Hyperparameter grid ==========
params = {
    'alpha': [0.01, 0.1, 1, 10],
    'fit_prior': [True, False]
}

# Lists to store metrics
accuracies = []
precisions = []
recalls = []
f1_scores = []
auc_values = []

for repeated_time in range(REPEAT):
    # --- 4.1 Split into train/test ---
    indices = np.arange(data.shape[0])
    train_index, test_index = train_test_split(
        indices, test_size=0.2, random_state=repeated_time
    )

    train_text = data[text_col].iloc[train_index]
    test_text = data[text_col].iloc[test_index]

    y_train = data['sentiment'].iloc[train_index]
    y_test = data['sentiment'].iloc[test_index]

    # --- 4.2 TF-IDF vectorization ---
    tfidf = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=2000,
        min_df=2,
        stop_words=final_stop_words_list
    )
    X_train = tfidf.fit_transform(train_text)
    X_test = tfidf.transform(test_text)

    # --- 4.3 Data balancing with SMOTE ---
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train.toarray(), y_train)

    # --- 4.4 Naive Bayes model & GridSearch ---
    clf = MultinomialNB()
    grid = GridSearchCV(
        clf,
        params,
        cv=5,
        scoring='f1_macro'
    )
    grid.fit(X_train_res, y_train_res)

    best_clf = grid.best_estimator_
    best_clf.fit(X_train_res, y_train_res)

    # --- 4.5 Make predictions & evaluate ---
    y_pred = best_clf.predict(X_test.toarray())

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='macro')
    rec = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    fpr, tpr, _ = roc_curve(y_test, y_pred, pos_label=1)
    auc_val = auc(fpr, tpr)

    accuracies.append(acc)
    precisions.append(prec)
    recalls.append(rec)
    f1_scores.append(f1)
    auc_values.append(auc_val)

# --- 4.6 Aggregate results ---
final_accuracy = np.mean(accuracies)
final_precision = np.mean(precisions)
final_recall = np.mean(recalls)
final_f1 = np.mean(f1_scores)
final_auc = np.mean(auc_values)

print("=== Improved Naive Bayes + TF-IDF Results ===")
print(f"Number of repeats:     {REPEAT}")
print(f"Average Accuracy:      {final_accuracy:.4f}")
print(f"Average Precision:     {final_precision:.4f}")
print(f"Average Recall:        {final_recall:.4f}")
print(f"Average F1 score:      {final_f1:.4f}")
print(f"Average AUC:           {final_auc:.4f}")

# --- 4.7 Save results to CSV ---
df_log = pd.DataFrame({
    'repeated_times': [REPEAT],
    'Accuracy': [final_accuracy],
    'Precision': [final_precision],
    'Recall': [final_recall],
    'F1': [final_f1],
    'AUC': [final_auc],
    'CV_list(AUC)': [str(auc_values)]
})

df_log.to_csv(out_csv_name, mode='a', header=not os.path.exists(out_csv_name), index=False)
print(f"\nResults saved to: {out_csv_name}")