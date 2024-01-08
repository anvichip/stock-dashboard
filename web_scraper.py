def scrape_web_main(tickerMain: str) -> list:

    from transformers import PegasusTokenizer, PegasusForConditionalGeneration, AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
    # sentencepiece, torch is also needed
    from bs4 import BeautifulSoup
    import requests
    import re

    tokenizer = AutoTokenizer.from_pretrained(
        "human-centered-summarization/financial-summarization-pegasus")
    model = AutoModelForSeq2SeqLM.from_pretrained(
        "human-centered-summarization/financial-summarization-pegasus")

    # Sending the requests over to the web pages
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'close'
    }

    def search_for_stock_news_urls(ticker):
        search_url = "https://www.google.com/search?q=yahoo+finance+{}&tbm=nws".format(
            ticker)
        r = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        atags = soup.find_all('a')
        hrefs = [link['href'] for link in atags]
        # time.sleep(delay)  # Simple rate limiting
        return hrefs

    # print("Searching Done")

    # Making a list out of the URL's along with the name of the ticker (just to be sure)
    raw_urls = {tickerMain: search_for_stock_news_urls(tickerMain)}
    # print(raw_urls)

    # Cleaning URL's
    exclude_list = ['maps', 'policies', 'preferences', 'accounts', 'support']

    def strip_unwanted_urls(urls, exclude_list):
        val = []
        for url in urls:
            if 'https://' in url and not any(exclude_word in url for exclude_word in exclude_list):
                res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
                val.append(res)
        return list(set(val))
    cleaned_urls = {tickerMain: strip_unwanted_urls(
        raw_urls[tickerMain], exclude_list)}
    # print(cleaned_urls)

    def scrape_and_process(urls):
        articles = []
        for url in urls:
            no = ["© 2024 - Privacy - Terms", "privacy terms", "Please enable JS and disable any ad blocker",
                  "please enable JS and disable any ad blocker",
                  "Thank you for your patience. Our engineers are working quickly to resolve the issue.",
                  "thank you for your patience our engineers are working quickly to resolve the issue"]
            # no = "Thank you for your patience. Our engineers are working quickly to resolve the issue."
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = [paragraph.text for paragraph in paragraphs]
            words = ' '.join(text).split(' ')[:510]
            article = ' '.join(words)
            # print(article, "\nAHA\n")
            if article not in no:
                articles.append(article)
        return articles

    articles = {}
    articles[tickerMain] = scrape_and_process(cleaned_urls[tickerMain])
    # articles

    # print("Scraping Done")

    def summarize(articles):
        summaries = []
        for i in range(len(articles)):
            article = articles[i]
            # print(article)
            input_ids = tokenizer.encode(
                article, return_tensors='pt', max_length=512, truncation=True)
            output = model.generate(
                input_ids, max_length=55, num_beams=5, early_stopping=True)
            summary = tokenizer.decode(output[0], skip_special_tokens=True)
            summaries.append(summary)
        return summaries

    summaries = {tickerMain: summarize(articles[tickerMain])}
    # print(summaries)

    # print("Summarization done")

    sentiment = pipeline('sentiment-analysis')

    scores = {tickerMain: sentiment(summaries[tickerMain])}

    # TODO Not sure if this works correctly, need to make sure once
    def create_output_array(ticker, summaries, scores, urls):
        output = []
        for counter in range(len(summaries[ticker])):
            output_this = [
                ticker,
                summaries[ticker][counter],
                scores[ticker][counter]['label'],
                scores[ticker][counter]['score'],
                urls[ticker][counter]
            ]
            output.append(output_this)
        return output

    final_output = create_output_array(
        tickerMain, summaries, scores, cleaned_urls)
    final_output.insert(0, ['Ticker', 'Summary', 'Label', 'Confidence', 'URL'])
    # final_output

    # print("Almost done")

    import pandas as pd
    df = pd.DataFrame(final_output)
    df.to_csv('file2.csv', header=False)

    # print(final_output)
    return final_output


# final_test = scrape_web_main("GME")
# print(final_test)
