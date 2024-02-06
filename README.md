# Webpage Translator with NLP Models

### Overview
Webpage Translator is a versatile Python tool designed for translating webpages seamlessly using advanced Natural Language Processing (NLP) models. This project supports multiple languages, including English, Portuguese, Spanish, French, German, Dutch, Italian, Korean, Chinese, and Russian. Users can choose between the MBart (Multilingual Bart) and TowerBase models for translation, depending on their preferences and resource constraints.

### Key Features
- **Multilingual Support:** Translate web content across various languages effortlessly.

- **Model Options:**
  - **MBart:** Offers accurate translations with moderate resource requirements.
  - **TowerBase:** Provides enhanced accuracy, demanding a more substantial GPU or RAM.
  - **HTML Content Translation:** Preserves the structure and attributes of HTML tags during the translation process.

- **File and URL Input:** Supports both local HTML files and webpages accessed via URLs for translation.

### Usage
1. **Installation:**
    - Install the necessary libraries: **bs4** and **transformers**.
    - Ensure that the **transformers** library is the correct version, including the specified models.
2. **Configuration:**
    - Set the input and output languages in the **language** and **input_language** variables.
    - Specify the output directory, model name (**MBart** or **TowerBase**), and other options.
3. **Run the Translation:**
    - Execute the main script, providing either a directory containing HTML files (**dir_path**) or a file with URLs (**url_file**).
4. **Output:**
    - Translated webpages will be saved in the specified output directory.
