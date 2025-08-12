import requests
from bs4 import BeautifulSoup
from langsmith import traceable
from backend.settings import settings
import stripe
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@traceable
def fetch_news_api(country: str):
    """
    Tool that fetches news articles from News API
    """
    match country:
        case "US":
            country = "us"
        case "Brazil":
            country = "br"
        case "Japan":
            country = "jp"
    url =  f"https://api.webz.io/newsApiLite?token={settings.NEWS_API_KEY}&q=published%3A%3Enow-24h%20site_category%3Atop_news_{country}%20performance_score%3A%3E0%20country%3A{country}%20language%3Aenglish"
    
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        articles = data["posts"]
        output = []
        for article in articles:
            source_url = article["url"]
            title = article["title"]
            content = get_text_content(source_url)
            if content !="":
                output.append({
                    "title": title,
                    "content": content,
                    })
        return {"trending_news": output}
    else:
        return {"error": f"Error fetching news: {response.status_code}"}
        
@traceable
def get_text_content(url: str) -> str:
    """
    Fetches the HTML content of a given URL.
    """
    try: 
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "footer", "nav", "aside", "noscript"]):
            tag.decompose()
        article = soup.find("article")
        if article:
            out_text = article.get_text(" ", strip=True)
        else: 
            out_text = soup.get_text(" ", strip=True)
        return out_text
    else:
        return ""

def create_stripe_customer(user_email: str):
    """
    Creates new Stripe customer object.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    new_customer = stripe.Customer.create(
        email=user_email
    )
    return new_customer

# doc https://docs.stripe.com/api/checkout/sessions/create
def create_stripe_subscription_session(customer_id: str):
    """
    Creates new Stripe checkout session.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode='subscription',
        line_items=[{
            'price': settings.STRIPE_SUBSCRIPTION_PRICE_KEY,
            'quantity': 1
        }],
        success_url="https://www.google.com/",        
        )
    return session

def send_email(email: str, subject: str, html_content: str):
    message = MIMEMultipart("alternative")
    message["From"] = settings.EMAIL_ADDRESS
    message["To"] = email
    message["Subject"] = subject
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    with SMTP_SSL('smtp.gmail.com', 465) as server:
        server.ehlo()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(message)
