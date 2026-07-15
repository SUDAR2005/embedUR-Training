# PII Redaction using Multilingual BERT

This project builds an AI-powered Named Entity Recognition (NER) model to automatically detect and redact Personally Identifiable Information (PII) from text. The model is fine-tuned on the **AI4Privacy/OpenPII** dataset using **Multilingual BERT (mBERT)**.

## Features

* Detects and masks sensitive information from text
* Supports **56 PII entity types** (113 BIO labels)
* Fine-tuned using **Multilingual BERT**
* Evaluated using **Precision, Recall, and F1-score**

## Dataset

* **Dataset:** [AI4Privacy /PII-masking-200k](https://huggingface.co/datasets/ai4privacy/pii-masking-200k/blob/main/english_pii_43k.jsonl)
* **Samples:** 43,501 (but used only 25K for training due to memory constraints)
* **Annotation Format:** BIO Tags

## Tech Stack

* Python
* PyTorch
* Hugging Face Transformers
* Hugging Face Datasets
* SeqEval
* Matplotlib

## Model Performance

| Metric    |  Score |
| --------- | -----  |
| Precision | 87.26% |
| Recall    | 90.01% |
| F1 Score  | 88.62% |

## Scope

Before sending data to AI models, sensitive information should be protected. This project helps automatically identify and mask personal information such as names, email addresses, phone numbers, account numbers, passwords, and other PII, making text safer to share with AI systems.

## Space for Improvements

* Train on the complete dataset
* Improve performance on rare entity types
* Develop as a web-extension or plug-in for real-time PII redaction
