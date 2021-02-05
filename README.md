# Zhihu Spider

A web spider catching zhihu answer and saving as PDF file.

Sometimes I browse zhihu and always find something valuable. I want to save it as a pdf of markdown file so that I can read it offline in my Kindle. That is what this project does.

## Installation

Pdfkit is required to wkhtmltopdf, so you need to download and install [wkhtmltopdf](https://wkhtmltopdf.org/).

### Linux 

```shell
git clone https://github.com/CAIMEOX/zhihu_spider.git
cd zhihu_spider
pip install -r requirements.txt
python GUI.py
```

## Usage

The spider can catch the following three types of articles:

- column

  Download the column articles and save them as pdf file.

- question

  Download the entire answers of a question and save them. 

- answers

  Download a single answer.

## Contributors

- [CAIMEO](https://github.com/300Little-fish) : Spider
- [300Little-fish](https://github.com/300Little-fish) : GUI
