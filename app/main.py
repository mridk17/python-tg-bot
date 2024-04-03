from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from get_ticker import get_ticker_by_company
from FinamNewsParser import FinamNewsParser
from TextRank import TextRankSummarizer
import logging

logger = logging.getLogger(__name__)

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


class Text(BaseModel):
    message: str



@app.get('/')
def ping():
    # ваш код здесь
    return { "message": "Service is alive" }


@app.post('/textrank')
def textrank(text: Text): 
    text_rank = TextRankSummarizer()
    summary = text_rank(text.message, 3)
   
    return summary

@app.get('/news/')
def news_route():
    raise HTTPException(status_code=404,  detail="Please, specify ticker name: /news/{ticker}")


@app.get('/news/{ticker}')
def news(ticker: str):
    return get_news_helper(ticker)
    

@app.get('/news/{ticker}/last')
def news(ticker: str):
    news = get_news_helper(ticker)
    return news[0].text


def get_news_helper(ticker):
    ticker = get_ticker_by_company(ticker)

    if ticker is None:
        raise HTTPException(status_code=404,  
                            detail="К сожалению, мы не смогли найти вашу компанию. Давайте попробуем другую.")

    logger.info("Ищем новости по тикеру: {ticker}")

    parser = FinamNewsParser()
    news = parser.collect_news(ticker, maxCount=3)


    if len(news) == 0:
        raise HTTPException(status_code=404,  
                    detail="Мы не смогли найти новости по вашей компании. Давайте поробуем другую.")


    for article in news:
        text_rank = TextRankSummarizer()
        summary = text_rank(article.text, 3)
        article.text = summary

    return news