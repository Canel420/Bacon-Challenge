from flask import jsonify, send_file
import string
import requests
import pandas as pd
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from models.metrics import Metrics, MetricsSchema



def process_text(texts):
    """
    process_text function takes a list of texts as input and returns a DataFrame 
    with each word as a token.
    """
    df = pd.concat([pd.DataFrame(word_tokenize("".join([char for char in text.lower() if char not in string.punctuation])), columns=['Tokens']) for text in texts], ignore_index=True)
    return df



def text_analysis(df):
    """
    text_analysis function takes a DataFrame of tokens as input and returns frequency 
    distributions of words, word lengths, bigrams, and trigrams.
    """
    all_words = df['Tokens'].tolist()
    freq_dist = nltk.FreqDist(all_words)

    word_lengths = [len(word) for word in all_words]
    length_dist = nltk.FreqDist(word_lengths)

    bigrams = ngrams(all_words, 2)
    bigrams_freq_dist = nltk.FreqDist(bigrams)

    trigrams = ngrams(all_words, 3)
    trigrams_freq_dist = nltk.FreqDist(trigrams)

    return freq_dist, length_dist, bigrams_freq_dist, trigrams_freq_dist



def generate_graphs(freq_dist, length_dist, bigrams_freq_dist, trigrams_freq_dist):
    """
    generate_graphs function takes frequency distributions of words, word lengths, bigrams, 
    and trigrams as input and generates a plot for each distribution. 
    It saves the plot as 'all_distributions.png' and returns a success message.
    """
    fig, axs = plt.subplots(2, 2, figsize=(5, 5))
    plt.suptitle('Visual Representations', fontsize=14, fontweight='bold')

    words, frequencies = zip(*freq_dist.most_common(10))
    axs[0, 0].bar(words, frequencies)
    axs[0, 0].set_title('Word Frequency Distribution', fontsize=8)
    axs[0, 0].tick_params(axis='x', rotation=90, labelsize=8)

    lengths, frequencies = zip(*length_dist.most_common(20))
    axs[0, 1].bar(lengths, frequencies)
    axs[0, 1].set_title('Word Length Distribution', fontsize=8)
    axs[0, 1].tick_params(axis='x', labelsize=8)

    bigrams, frequencies = zip(*bigrams_freq_dist.most_common(20))
    bigrams = [' '.join(bigram) for bigram in bigrams]
    axs[1, 0].bar(range(len(bigrams)), frequencies, tick_label=bigrams)
    axs[1, 0].set_title('Bigram Frequency Distribution', fontsize=8)
    axs[1, 0].tick_params(axis='x', rotation=90, labelsize=8)

    trigrams, frequencies = zip(*trigrams_freq_dist.most_common(20))
    trigrams = [' '.join(trigram) for trigram in trigrams]
    axs[1, 1].bar(range(len(trigrams)), frequencies, tick_label=trigrams)
    axs[1, 1].set_title('Trigram Frequency Distribution', fontsize=8)
    axs[1, 1].tick_params(axis='x', rotation=90, labelsize=8)

    plt.tight_layout()
    plt.savefig('all_distributions.png')
    plt.close(fig)

    return 'Graphs generated', 200

def create_tables(freq_dist, length_dist, bigrams_freq_dist, trigrams_freq_dist):
    """
    create_tables function takes frequency distributions of words, word lengths, bigrams, 
    and trigrams as input and returns a table for each distribution.
    """
    styles = getSampleStyleSheet()
    header_style = styles['Heading1']

    word_freq_data = [['Word', 'Frequency']] + freq_dist.most_common(5)
    word_freq_table = Table(word_freq_data)
    word_freq_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), header_style.fontName)]))

    word_length_data = [['Word Length', 'Frequency']] + length_dist.most_common(5)
    word_length_table = Table(word_length_data)
    word_length_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), header_style.fontName)]))

    bigram_freq_data = [['Bigram', 'Frequency']] + [(str(bigram), freq) for bigram, freq in bigrams_freq_dist.most_common(5)]
    bigram_freq_table = Table(bigram_freq_data)
    bigram_freq_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), header_style.fontName)]))

    trigram_freq_data = [['Trigram', 'Frequency']] + [(str(trigram), freq) for trigram, freq in trigrams_freq_dist.most_common(5)]
    trigram_freq_table = Table(trigram_freq_data)
    trigram_freq_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), header_style.fontName)]))

    data = [[word_freq_table, word_length_table],
            [bigram_freq_table, trigram_freq_table]]

    return Table(data)


def validate_paragraphs_qty(paragraphs_qty):
    """
    validate_paragraphs_qty function takes a number of paragraphs as input and validates
    that it is an integer.
    """
    if paragraphs_qty is None:
        raise ValueError('paragraphsQty is required')
    if not isinstance(paragraphs_qty, int):
        raise ValueError('paragraphsQty must be an integer')


def generate_pdf(paragraphs_qty):
    """
    generate_pdf function takes a number of paragraphs as input, fetches that many paragraphs of 'meat' 
    text from the Bacon Ipsum API, processes and analyzes the text, generates graphs and tables from the 
    analysis, and compiles everything into a PDF report. It returns the PDF file or an error message.
    """
    validate_paragraphs_qty(paragraphs_qty)
    try:
        response = requests.get(f'https://baconipsum.com/api/?type=all-meat&paras={paragraphs_qty}')
        response.raise_for_status()
        data = response.json()
        if not data:
            return 'Empty response from API', 400
        df = process_text(data)
        freq_dist, length_dist, bigrams_freq_dist, trigrams_freq_dist = text_analysis(df)
        generate_graphs(freq_dist, length_dist, bigrams_freq_dist, trigrams_freq_dist)

        doc = SimpleDocTemplate("report.pdf", pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        story.append(Paragraph("Original Text", styles["Heading1"]))
        for paragraph in data:
            story.append(Paragraph(paragraph, styles["BodyText"]))
            story.append(Spacer(1, 12))

        story.append(Paragraph("Analytical Findings", styles["Heading1"]))
        description = """
        The word analysis made to the original text were: frequently occurring words, the distribution of word lengths, 
        bigrams (two consecutive words) and trigrams (three consecutive words) analysis, and the following tables display 
        the 5 most common of each analysis.
        """
        story.append(Paragraph(description, styles["BodyText"]))
        story.append(Spacer(1, 12))

        tables = create_tables(freq_dist, length_dist, bigrams_freq_dist, trigrams_freq_dist)
        story.append(tables)
        story.append(Spacer(1, 12))

        story.append(Image('all_distributions.png'))

        doc.build(story)

        return send_file('report.pdf', mimetype='application/pdf'), 200
    except requests.exceptions.RequestException as e:
        return f'Error while fetching data: {str(e)}', 500


def get_metrics():
    """
    get_metrics function returns the top 5 most frequently occurring words
    """
    metrics = Metrics.query.order_by(Metrics.frequency.desc()).limit(5).all()
    metrics_schema = MetricsSchema(many=True)
    return jsonify(metrics_schema.dump(metrics)), 200