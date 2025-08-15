import pytest 
from  unittest.mock import patch, Mock, AsyncMock, MagicMock
import stripe
from backend.tools import fetch_news_api, create_stripe_customer, update_user_subscription, send_email
from datetime import datetime
from backend.db import get_pg_async_session
from backend.models.user import User
from contextlib import asynccontextmanager


def test_fetch_news_api_success(mocker):
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "posts": [
            {
                "thread": {
                    "uuid": "1802de2eba1a23927ab3293df8270fb93cd6cbdb",
                    "url": "https://www.cbsnews.com/video/sneak-peek-unmasking-the-zombie-hunter-phoenix-canal-murders/",
                    "site_full": "www.cbsnews.com",
                    "site": "cbsnews.com",
                    "site_section": "https://www.kfmosports.phizcentral.com/national-news",
                    "site_categories": [
                        "media",
                        "television",
                        "entertainment",
                        "top_news_ca",
                        "top_news_ph",
                        "top_news_iq",
                        "top_news_nz",
                        "top_news_au",
                        "top_news_us",
                        "top_news_za",
                        "top_news_sg",
                        "top_news_kw",
                        "top_news"
                    ],
                    "section_title": "National News",
                    "title": "Sneak peek: Unmasking the Zombie Hunter - CBS News",
                    "title_full": "Sneak peek: Unmasking the Zombie Hunter - CBS News",
                    "published": "2025-08-13T17:30:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://assets3.cbsnewsstatic.com/hub/i/r/2023/10/19/528314c5-6edc-40eb-ab6d-d8fa1b98f5a0/thumbnail/1200x630/05876f9b2526b32b649844dd11f8549b/zombie-hunter-sneakpeek-2381835-640x360.jpg",
                    "performance_score": 6,
                    "domain_rank": 216,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T16:03:33.000+00:00",
                        "facebook": {
                            "likes": 101,
                            "comments": 38,
                            "shares": 4
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "1802de2eba1a23927ab3293df8270fb93cd6cbdb",
                "url": "https://www.cbsnews.com/video/sneak-peek-unmasking-the-zombie-hunter-phoenix-canal-murders/",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "CBS News",
                "published": "2025-08-13T17:30:00.000+03:00",
                "title": "Sneak peek: Unmasking the Zombie Hunter - CBS News",
                "text": "ENCORE: How police connected the murders of two young women to a man known as a zombie-fighting comic book hero. \"48 Hours\" correspondent Peter Van Sant reports Saturday, Aug. 16 at 10/9c on CBS and s...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "neutral",
                "categories": [
                    "Crime, Law and Justice"
                ],
                "external_links": [],
                "external_images": [],
                "entities": {
                    "persons": [
                        {
                            "name": "Peter Van Sant",
                            "sentiment": "none"
                        }
                    ],
                    "organizations": [
                        {
                            "name": "CBS News",
                            "sentiment": "neutral"
                        }
                    ],
                    "locations": []
                },
                "rating": None,
                "crawled": "2025-08-13T19:02:00.825+03:00",
                "updated": "2025-08-13T16:05:50.000+00:00"
            },
            {
                "thread": {
                    "uuid": "1cb5cb0a46d0d8ade50f91e60a41e74196fe0d53",
                    "url": "https://sports.yahoo.com/mma/article/dana-white-says-ufcs-white-house-fight-card-on-july-4-will-absolutely-take-place-154446345.html",
                    "site_full": "sports.yahoo.com",
                    "site": "yahoo.com",
                    "site_section": "https://www.thewhodatdaily.com",
                    "site_categories": [
                        "sports",
                        "top_news_ru",
                        "top_news_ar",
                        "top_news_cz",
                        "top_news_nz",
                        "top_news_au",
                        "top_news_jp",
                        "top_news_ae",
                        "top_news_ua",
                        "top_news_tr",
                        "top_news_us",
                        "top_news_at",
                        "top_news_tw",
                        "top_news_pt",
                        "top_news_pl",
                        "top_news_gb",
                        "top_news_th",
                        "top_news_kr",
                        "top_news_sa",
                        "top_news_co",
                        "top_news_vn",
                        "top_news_hu",
                        "top_news_sg",
                        "top_news_ph",
                        "top_news_rs",
                        "top_news_bg",
                        "top_news_br",
                        "top_news_hk",
                        "top_news_nl",
                        "top_news_qa",
                        "top_news_hr",
                        "top_news_ie",
                        "top_news_ro",
                        "top_news_pk",
                        "top_news_se",
                        "top_news_id",
                        "top_news_dk",
                        "top_news_de",
                        "top_news_eg",
                        "top_news_it",
                        "top_news_pe",
                        "top_news_sk",
                        "top_news_ch",
                        "top_news_za",
                        "top_news_ma",
                        "top_news_my",
                        "top_news_il",
                        "top_news_kw",
                        "top_news_in",
                        "top_news_fr",
                        "top_news_ve",
                        "top_news_fi",
                        "top_news_be",
                        "top_news_mx",
                        "top_news_no",
                        "top_news_ca",
                        "top_news_cl",
                        "top_news_iq",
                        "top_news_gr",
                        "top_news_es",
                        "top_news"
                    ],
                    "section_title": "Who Dat Daily – New Orleans Saints, Pelicans &amp; LSU News",
                    "title": "Dana White says UFC's White House fight card on July 4 will 'absolutely' take place",
                    "title_full": "Dana White says UFC's White House fight card on July 4 will 'absolutely' take place",
                    "published": "2025-08-13T23:04:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "",
                    "performance_score": 5,
                    "domain_rank": 48,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T20:57:46.000+00:00",
                        "facebook": {
                            "likes": 53,
                            "comments": 64,
                            "shares": 51
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "1cb5cb0a46d0d8ade50f91e60a41e74196fe0d53",
                "url": "https://sports.yahoo.com/mma/article/dana-white-says-ufcs-white-house-fight-card-on-july-4-will-absolutely-take-place-154446345.html",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "News PRO",
                "published": "2025-08-13T23:04:00.000+03:00",
                "title": "Dana White says UFC's White House fight card on July 4 will 'absolutely' take place",
                "text": "White said the event will take place on the South Lawn and air on CBS. Read More",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "positive",
                "categories": [
                    "Sport",
                    "Human Interest"
                ],
                "external_links": [],
                "external_images": [],
                "entities": {
                    "persons": [
                        {
                            "name": "Dana White",
                            "sentiment": "neutral"
                        }
                    ],
                    "organizations": [
                        {
                            "name": "UFC",
                            "sentiment": "neutral"
                        },
                        {
                            "name": "White House",
                            "sentiment": "neutral"
                        },
                        {
                            "name": "CBS",
                            "sentiment": "neutral"
                        }
                    ],
                    "locations": [
                        {
                            "name": "South Lawn",
                            "sentiment": "none"
                        }
                    ]
                },
                "rating": None,
                "crawled": "2025-08-13T23:55:15.474+03:00",
                "updated": "2025-08-13T20:59:18.000+00:00"
            },
            {
                "thread": {
                    "uuid": "3f87631a28ed6e5c9e53b4d09ef0698e1a826009",
                    "url": "https://www.washingtonpost.com/business/2025/08/13/tiktok-skilled-trades-workers/",
                    "site_full": "www.washingtonpost.com",
                    "site": "washingtonpost.com",
                    "site_section": "https://news.google.com/search?q=a%20when%3a1h&hl=en-us&gl=us&ceid=us%3aen",
                    "site_categories": [
                        "media",
                        "law_government_and_politics",
                        "politics",
                        "top_news_pk",
                        "top_news_gb",
                        "top_news_il",
                        "top_news_dk",
                        "top_news_se",
                        "top_news_nz",
                        "top_news_au",
                        "top_news_sg",
                        "top_news_za",
                        "top_news_ph",
                        "top_news_us",
                        "top_news_ca",
                        "top_news_iq",
                        "top_news_ie",
                        "top_news_pt",
                        "top_news"
                    ],
                    "section_title": "Google News - Search",
                    "title": "Social media opens a window to traditional trades for young workers",
                    "title_full": "Social media opens a window to traditional trades for young workers",
                    "published": "2025-08-13T14:00:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://www.washingtonpost.com/wp-apps/imrs.php?src=https://d1i4t8bqe7zgj6.cloudfront.net/08-07-2025/t_0d1d09fead164c17bbe40e61959ae4da_name_TIKTOKTRADES_THUMB_2.jpg&amp;w=1440",
                    "performance_score": 5,
                    "domain_rank": 121,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T16:21:43.000+00:00",
                        "facebook": {
                            "likes": 78,
                            "comments": 37,
                            "shares": 19
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "3f87631a28ed6e5c9e53b4d09ef0698e1a826009",
                "url": "https://www.washingtonpost.com/business/2025/08/13/tiktok-skilled-trades-workers/",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "Taylor Telford",
                "published": "2025-08-13T14:00:00.000+03:00",
                "title": "Social media opens a window to traditional trades for young workers",
                "text": "In 2023, after he was captivated by a video showing a day in the life of a group of trainees scaling a lattice tower for the first time, Dylan Healy moved from New York to Georgia with some friends to...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "positive",
                "categories": [
                    "Politics"
                ],
                "external_links": [
                    "http://www.youtube.com/watch?v=E6g9P3U-ie0",
                    "http://www.youtube.com/watch",
                    "http://youtube.com/watch?v=E6g9P3U-ie0"
                ],
                "external_images": [],
                "entities": {
                    "persons": [
                        {
                            "name": "Dylan Healy",
                            "sentiment": "none"
                        }
                    ],
                    "organizations": [],
                    "locations": [
                        {
                            "name": "Training Center",
                            "sentiment": "none"
                        },
                        {
                            "name": "Southeast",
                            "sentiment": "none"
                        }
                    ]
                },
                "rating": None,
                "crawled": "2025-08-13T19:19:53.416+03:00",
                "updated": "2025-08-13T16:23:46.000+00:00"
            },
            {
                "thread": {
                    "uuid": "60aaf0cefda91bb490e70ebf12fa66777d99f14b",
                    "url": "https://www.forbes.com/sites/forbes-personal-shopper/article/the-best-emergency-food-supplies/",
                    "site_full": "www.forbes.com",
                    "site": "forbes.com",
                    "site_section": "http://www.forbes.com/europe_news/index.xml",
                    "site_categories": [
                        "media",
                        "top_news_cz",
                        "top_news_nz",
                        "top_news_au",
                        "top_news_ae",
                        "top_news_us",
                        "top_news_pt",
                        "top_news_gb",
                        "top_news_th",
                        "top_news_sa",
                        "top_news_sg",
                        "top_news_ph",
                        "top_news_rs",
                        "top_news_hk",
                        "top_news_nl",
                        "top_news_qa",
                        "top_news_ie",
                        "top_news_pk",
                        "top_news_se",
                        "top_news_id",
                        "top_news_dk",
                        "top_news_eg",
                        "top_news_sk",
                        "top_news_ch",
                        "top_news_za",
                        "top_news_ma",
                        "top_news_my",
                        "top_news_il",
                        "top_news_kw",
                        "top_news_fi",
                        "top_news_be",
                        "top_news_in",
                        "top_news_ca",
                        "top_news_iq",
                        "top_news"
                    ],
                    "section_title": "Latest from Forbes",
                    "title": "Best Emergency Food Supplies 2025 - Forbes Vetted",
                    "title_full": "Best Emergency Food Supplies 2025 - Forbes Vetted",
                    "published": "2025-08-13T18:09:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://imageio.forbes.com/specials-images/imageserve/689a4374ff4b6e27e6bc1d6c/0x0.jpg?format=jpg&amp;height=900&amp;width=1600&amp;fit=bounds",
                    "performance_score": 6,
                    "domain_rank": 74,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T15:22:44.000+00:00",
                        "facebook": {
                            "likes": 135,
                            "comments": 7,
                            "shares": 13
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "60aaf0cefda91bb490e70ebf12fa66777d99f14b",
                "url": "https://www.forbes.com/sites/forbes-personal-shopper/article/the-best-emergency-food-supplies/",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "Lee Cutlip",
                "published": "2025-08-13T18:09:00.000+03:00",
                "title": "Best Emergency Food Supplies 2025 - Forbes Vetted",
                "text": "From natural disasters to uncertain economic climates and even the once-in-a-lifetime pandemic, it’s difficult to predict the seemingly unpredictable. Maybe you can’t foresee every hurricane or wildfi...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "positive",
                "categories": [
                    "Economy, Business and Finance",
                    "Lifestyle and Leisure",
                    "Human Interest"
                ],
                "external_links": [
                    "http://www.amazon.com/exec/obidos/ASIN/B08C9JZYPG",
                    "https://clicks.trx-hub.com/xid/forbes_ghj568dre?q=https%253A%252F%252Fbackpackerspantry.com%252Fcollections%252Fvegetarian%252Fproducts%252F7-day-emergency-survival-kit-vegetarian&ref=http%3A%2F%2Fwww.forbes.com%2Fsites%2Fforbes-personal-shopper%2Farticle%2Fthe-best-emergency-food-supplies%2F&event_type=click&utm_source=&linkRanId=933222cd-210e-492f-98c3-7e5e8cd1055d",
                    "https://clicks.trx-hub.com/xid/forbes_ghj568dre?q=https%253A%252F%252Fgo.skimresources.com%253Fid%253D106821X1564016%2526xs%253D1%2526xcust%253D67d87913bf4eb66ce54284f9%2526url%253Dhttps%25253A%25252F%25252Fgoodto-go.com%25252Fcollections%25252Fall-multi-packs%25252Fproducts%25252F5-day-emergency-food-kit-variety-1-vegan&ref=http%3A%2F%2Fwww.forbes.com%2Fsites%2Fforbes-personal-shopper%2Farticle%2Fthe-best-emergency-food-supplies%2F&event_type=click&utm_source=&linkRanId=933222cd-210e-492f-98c3-7e5e8cd1055",
                    "http://www.amazon.com/exec/obidos/ASIN/B004JT7F8I",
                    "http://www.amazon.com/exec/obidos/ASIN/B00GDGGR4S",
                    "https://clicks.trx-hub.com/xid/forbes_ghj568dre?q=https%253A%252F%252Fgoto.walmart.com%252Fc%252F1201867%252F565706%252F9383%253Fveh%253Daff%2526sourceid%253Dimp_000011112222333344%2526u%253Dhttps%25253A%25252F%25252Fwww.walmart.com%25252Fip%25252FAugason-Farms-1-Person-30-Day-Emergency-Food-Supply-QSS-Certified%25252F55292819%2526subId1%253D67dc121a6e35680847e4a269&ref=http%3A%2F%2Fwww.forbes.com%2Fsites%2Fforbes-personal-shopper%2Farticle%2Fthe-best-emergency-food-supplies%2F&event_type=click&utm_source=&amp",
                    "http://amazon.com/exec/obidos/ASIN/B004JT7F8I",
                    "https://www.clicks.trx-hub.com/xid/forbes_ghj568dre?q=https%253A%252F%252Fgo.skimresources.com%253Fid%253D106821X1564016%2526xs%253D1%2526xcust%253D67d87913bf4eb66ce54284f9%2526url%253Dhttps%25253A%25252F%25252Fgoodto-go.com%25252Fcollections%25252Fall-multi-packs%25252Fproducts%25252F5-day-emergency-food-kit-variety-1-vegan&ref=http%3A%2F%2Fwww.forbes.com%2Fsites%2Fforbes-personal-shopper%2Farticle%2Fthe-best-emergency-food-supplies%2F&event_type=click&utm_source=&linkRanId=933222cd-210e-492f-98c3-7e5e8cd1055",
                    "http://amazon.com/exec/obidos/ASIN/B08C9JZYPG",
                    "https://clicks.trx-hub.com/xid/forbes_ghj568dre",
                    "https://www.clicks.trx-hub.com/xid/forbes_ghj568dre?q=https%253A%252F%252Fgoto.walmart.com%252Fc%252F1201867%252F565706%252F9383%253Fveh%253Daff%2526sourceid%253Dimp_000011112222333344%2526u%253Dhttps%25253A%25252F%25252Fwww.walmart.com%25252Fip%25252FAugason-Farms-1-Person-30-Day-Emergency-Food-Supply-QSS-Certified%25252F55292819%2526subId1%253D67dc121a6e35680847e4a269&ref=http%3A%2F%2Fwww.forbes.com%2Fsites%2Fforbes-personal-shopper%2Farticle%2Fthe-best-emergency-food-supplies%2F&event_type=click&utm_source=&amp",
                    "http://amazon.com/exec/obidos/ASIN/B00GDGGR4S",
                    "https://www.clicks.trx-hub.com/xid/forbes_ghj568dre?q=https%253A%252F%252Fbackpackerspantry.com%252Fcollections%252Fvegetarian%252Fproducts%252F7-day-emergency-survival-kit-vegetarian&ref=http%3A%2F%2Fwww.forbes.com%2Fsites%2Fforbes-personal-shopper%2Farticle%2Fthe-best-emergency-food-supplies%2F&event_type=click&utm_source=&linkRanId=933222cd-210e-492f-98c3-7e5e8cd1055d"
                ],
                "external_images": [],
                "entities": {
                    "persons": [],
                    "organizations": [],
                    "locations": []
                },
                "rating": None,
                "crawled": "2025-08-13T18:22:14.841+03:00",
                "updated": "2025-08-13T15:26:41.000+00:00"
            },
            {
                "thread": {
                    "uuid": "db0a4de1617727b794a85be729997aa656ea5f5d",
                    "url": "https://www.today.com/life/holidays/best-friend-halloween-costumes-rcna35039",
                    "site_full": "www.today.com",
                    "site": "today.com",
                    "site_section": "https://www.today.com/life/quotes",
                    "site_categories": [
                        "media",
                        "top_news_ca",
                        "top_news_ph",
                        "top_news_au",
                        "top_news_us",
                        "top_news_za",
                        "top_news_ie",
                        "top_news_nz",
                        "top_news"
                    ],
                    "section_title": "Quotes | TODAY",
                    "title": "67 Best Friend Halloween Costumes For Duos, Pairs and Groups",
                    "title_full": "67 Best Friend Halloween Costumes For Duos, Pairs and Groups",
                    "published": "2025-08-13T21:22:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://media-cldnry.s-nbcnews.com/image/upload/t_social_share_1200x630_center,f_auto,q_auto:best/rockcms/2023-08/best-friend-halloween-costumes-zz-230807-c33983.jpg",
                    "performance_score": 9,
                    "domain_rank": 760,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T23:10:39.000+00:00",
                        "facebook": {
                            "likes": 501,
                            "comments": 6,
                            "shares": 20
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "db0a4de1617727b794a85be729997aa656ea5f5d",
                "url": "https://www.today.com/life/holidays/best-friend-halloween-costumes-rcna35039",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "Sarah Lemire",
                "published": "2025-08-13T21:22:00.000+03:00",
                "title": "67 Best Friend Halloween Costumes For Duos, Pairs and Groups",
                "text": "Halloween is on its way! With Oct. 31 just around the corner, there's no time to waste picking out a pumpkin, stocking up on candy for trick-or-treaters and perhaps most important, planning what costu...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "neutral",
                "categories": [
                    "Lifestyle and Leisure",
                    "Human Interest",
                    "Arts, Culture and Entertainment"
                ],
                "external_links": [
                    "https://themerrythought.com/halloween-2/diy-the-birds-the-bees-costume/",
                    "https://lovelyindeed.com/diy-cupid-costume-for-halloween/",
                    "https://themerrythought.com/diy/diy-rock-paper-scissors-costume-printable/",
                    "https://abeautifulmess.com/stranger-things-costume-gift-guide/",
                    "https://ohyaystudio.com/candy-halloween-costumes/",
                    "https://lovelyindeed.com/wreck-it-ralph-costumes-for-halloween",
                    "https://livingaftermidnite.com/10-last-minute-halloween-costumes-you-can-amazon-prime/",
                    "https://www.clubcrafted.com/nintendo-switch-costume-couples/",
                    "https://lovelyindeed.com/make-a-couples-greaser-halloween-costume/",
                    "http://www.tfdiaries.com/2018/10/best-throwback-costume-ideas-for-you-and-your-best-friend.html",
                    "https://livingaftermidnite.com/3-nostalgic-halloween-costumes-you-can-pull-together-quickly/",
                    "https://www.tfdiaries.com/2018/10/best-throwback-costume-ideas-for-you-and-your-best-friend.html",
                    "https://studiodiy.com/diy-90s-toys-costumes/",
                    "https://studiodiy.com/easy-diy-strawberry-shortcake-costume/",
                    "https://www.tfdiaries.com/2022/08/DIY-snl-celebrity-jeopardy-halloween-costume-idea.html",
                    "https://studiodiy.com/diy-troop-beverly-hills-costume/",
                    "https://livingaftermidnite.com/3-halloween-costumes-for-you-and-your-bestie/",
                    "https://studiodiy.com/diy-milkshake-costumes/",
                    "https://abeautifulmess.com/couples-costume-britney-and-justin-the-denim-outfits/",
                    "http://www.tfdiaries.com/2015/10/3-costumes-ideas-for-you-and-your-bestie.html",
                    "https://studiodiy.com/diy-hot-dog-costume/",
                    "https://ohyaystudio.com/easy-married-with-children-halloween-costumes/",
                    "https://keikolynn.com/2020/10/haunted-mansion-the-hitchhiking-ghosts-group-costumes/",
                    "http://www.awwsam.com/2019/10/kikis-delivery-service-costumes.html",
                    "https://livingaftermidnite.com/best-friend-halloween-costumes/",
                    "https://studiodiy.com/diy-palm-tree-beach-ball-costumes/",
                    "https://themerrythought.com/diy/diy-dominos-costume/",
                    "https://studiodiy.com/diy-pool-float-costumes/",
                    "https://abeautifulmess.com/essential-oil-halloween-costume/",
                    "https://studiodiy.com/diy-candy-necklace-costume-sweet-tooth-couples-costume/",
                    "https://keikolynn.com/2016/10/mary-poppins-and-bert-couples-costume/",
                    "https://livingaftermidnite.com/affordable-halloween-costumes-for-you-your-best-friend/",
                    "https://studiodiy.com/diy-school-lunch-costumes/",
                    "https://studiodiy.com/diy-pie-slice-costumes/",
                    "https://studiodiy.com/diy-frosted-animal-cookie-costume/",
                    "https://studiodiy.com/diy-citrus-slice-costumes/",
                    "http://www.tfdiaries.com/2019/10/six-iconic-pop-culture-halloween-costumes-for-couples-and-groups.html",
                    "https://www.colormecourtney.com/broadway-themed-halloween-costumes",
                    "https://studiodiy.com/diy-lock-shock-and-barrel-costumes/",
                    "https://keikolynn.com/2021/10/halloween-couples-costume-idea-beetlejuice-and-lydia-deetz-on-their-wedding-day/",
                    "https://keikolynn.com/2021/10/alice-in-wonderland-group-costume/",
                    "http://www.tfdiaries.com/2016/10/90s-inspired-costume-ideas-from-your.html",
                    "http://www.awwsam.com/2017/10/diy-fuzzy-dice-group-costume.html",
                    "https://www.facebook.com/suncitypinupdolls/about/?ref=page_internal",
                    "https://abeautifulmess.com/dog-family-costumes-chefs-butter-lobster/",
                    "https://www.facebook.com/suncitypinupdolls/",
                    "https://keikolynn.com/2018/10/halloween-up-costume-disney-pixar/",
                    "https://www.tingandthings.com/2017/11/spice-girls-group-halloween-costume.html",
                    "https://abeautifulmess.com/20-halloween-costume-ideas/",
                    "https://livingaftermidnite.com/iconic-halloween-movie-costumes/",
                    "https://themerrythought.com/diy/diy-supermarket-sweep-costume/",
                    "https://www.tfdiaries.com/2022/08/DIY-edward-scissorhands-couples-halloween-costume-.html",
                    "https://keikolynn.com/2016/10/heathers-group-costume-for-halloween/",
                    "http://www.tfdiaries.com/2018/10/fifteen-last-minute-costume-ideas-for-best-friends-and-couples.html",
                    "http://www.tfdiaries.com/2017/09/4-budget-friendly-halloween-costumes-for-you-and-your-best-friend.html",
                    "https://lovelyindeed.com/wheres-waldo-costume-family-halloween/",
                    "https://ohyaystudio.com/candy-halloween-costumes",
                    "https://www.livingaftermidnite.com/3-halloween-costumes-for-you-and-your-bestie/",
                    "https://studiodiy.com/diy-lock-shock-and-barrel-costumes",
                    "http://awwsam.com/2017/10/diy-fuzzy-dice-group-costume.html",
                    "https://www.studiodiy.com/diy-troop-beverly-hills-costume/",
                    "https://themerrythought.com/halloween-2/diy-the-birds-the-bees-costume",
                    "https://lovelyindeed.com/wheres-waldo-costume-family-halloween",
                    "https://themerrythought.com/diy/diy-dominos-costume",
                    "https://www.lovelyindeed.com/make-a-couples-greaser-halloween-costume/",
                    "https://abeautifulmess.com/20-halloween-costume-ideas",
                    "https://www.studiodiy.com/diy-frosted-animal-cookie-costume/",
                    "http://tfdiaries.com/2015/10/3-costumes-ideas-for-you-and-your-bestie.html",
                    "https://keikolynn.com/2018/10/halloween-up-costume-disney-pixar",
                    "https://tingandthings.com/2017/11/spice-girls-group-halloween-costume.html",
                    "https://www.studiodiy.com/diy-citrus-slice-costumes/",
                    "https://www.studiodiy.com/diy-pie-slice-costumes/",
                    "https://lovelyindeed.com/diy-cupid-costume-for-halloween",
                    "https://livingaftermidnite.com/10-last-minute-halloween-costumes-you-can-amazon-prime",
                    "https://studiodiy.com/diy-milkshake-costumes",
                    "https://tfdiaries.com/2022/08/DIY-edward-scissorhands-couples-halloween-costume-.html",
                    "https://livingaftermidnite.com/best-friend-halloween-costumes",
                    "https://www.keikolynn.com/2016/10/mary-poppins-and-bert-couples-costume/",
                    "https://www.livingaftermidnite.com/best-friend-halloween-costumes/",
                    "http://tfdiaries.com/2016/10/90s-inspired-costume-ideas-from-your.html",
                    "https://studiodiy.com/diy-citrus-slice-costumes",
                    "https://studiodiy.com/diy-school-lunch-costumes",
                    "https://www.lovelyindeed.com/diy-cupid-costume-for-halloween/",
                    "https://clubcrafted.com/nintendo-switch-costume-couples/",
                    "https://www.facebook.com/suncitypinupdolls",
                    "https://keikolynn.com/2016/10/heathers-group-costume-for-halloween",
                    "https://facebook.com/suncitypinupdolls/",
                    "http://awwsam.com/2019/10/kikis-delivery-service-costumes.html",
                    "https://www.clubcrafted.com/nintendo-switch-costume-couples",
                    "https://livingaftermidnite.com/affordable-halloween-costumes-for-you-your-best-friend",
                    "https://themerrythought.com/diy/diy-rock-paper-scissors-costume-printable",
                    "https://www.facebook.com/suncitypinupdolls/about/",
                    "https://www.livingaftermidnite.com/10-last-minute-halloween-costumes-you-can-amazon-prime/",
                    "https://abeautifulmess.com/couples-costume-britney-and-justin-the-denim-outfits",
                    "https://keikolynn.com/2021/10/halloween-couples-costume-idea-beetlejuice-and-lydia-deetz-on-their-wedding-day",
                    "https://studiodiy.com/diy-hot-dog-costume",
                    "https://www.studiodiy.com/diy-pool-float-costumes/",
                    "https://ohyaystudio.com/easy-married-with-children-halloween-costumes",
                    "http://tfdiaries.com/2019/10/six-iconic-pop-culture-halloween-costumes-for-couples-and-groups.html",
                    "https://studiodiy.com/diy-pie-slice-costumes"
                ],
                "external_images": [],
                "entities": {
                    "persons": [],
                    "organizations": [],
                    "locations": []
                },
                "rating": None,
                "crawled": "2025-08-14T02:04:06.835+03:00",
                "updated": "2025-08-13T23:10:39.000+00:00"
            },
            {
                "thread": {
                    "uuid": "9a8f844c8ff21b1b314928d06b149923fb9bece9",
                    "url": "https://www.newsmax.com/world/globaltalk/germany-drones-military/2025/08/13/id/1222281/",
                    "site_full": "www.newsmax.com",
                    "site": "newsmax.com",
                    "site_section": "https://newsmax.com/world",
                    "site_categories": [
                        "media",
                        "law_government_and_politics",
                        "politics",
                        "top_news_us",
                        "top_news"
                    ],
                    "section_title": "\r\n\tNewsmax – Breaking News | News Videos | Politics, Health, Finance\r\n",
                    "title": "536 Drones Spotted at German Military Sites | Newsmax.com",
                    "title_full": "536 Drones Spotted at German Military Sites | Newsmax.com",
                    "published": "2025-08-13T14:18:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://www.newsmax.com/CMSPages/GetFile.aspx?guid=196dcbaa-76a3-4805-88cf-5be5b7a6161d&amp;SiteName=Newsmax",
                    "performance_score": 7,
                    "domain_rank": 2621,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T15:02:04.000+00:00",
                        "facebook": {
                            "likes": 224,
                            "comments": 98,
                            "shares": 16
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "9a8f844c8ff21b1b314928d06b149923fb9bece9",
                "url": "https://www.newsmax.com/world/globaltalk/germany-drones-military/2025/08/13/id/1222281/",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "Newsmax Wires",
                "published": "2025-08-13T14:18:00.000+03:00",
                "title": "536 Drones Spotted at German Military Sites | Newsmax.com",
                "text": "By Newsmax Wires | Wednesday, 13 August 2025 07:18 AM EDT\nBetween January and March 2025, German authorities recorded 536 cases of unidentified drones flying over sensitive sites, according to a recen...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "neutral",
                "categories": [
                    "Politics",
                    "War, Conflict and Unrest",
                    "Social Issue"
                ],
                "external_links": [],
                "external_images": [],
                "entities": {
                    "persons": [],
                    "organizations": [
                        {
                            "name": "Federal Criminal Police Office",
                            "sentiment": "none"
                        }
                    ],
                    "locations": [
                        {
                            "name": "Ramstein Air Base",
                            "sentiment": "none"
                        }
                    ]
                },
                "rating": None,
                "crawled": "2025-08-13T18:01:15.829+03:00",
                "updated": "2025-08-13T15:05:53.000+00:00"
            },
            {
                "thread": {
                    "uuid": "ec908666d2bb9b890869d068fc73ae0705daa56c",
                    "url": "https://www.newsmax.com/newsfront/benjamin-netanyahu-israel-hamas/2025/08/13/id/1222395",
                    "site_full": "www.newsmax.com",
                    "site": "newsmax.com",
                    "site_section": "https://www.wgmd.com",
                    "site_categories": [
                        "media",
                        "law_government_and_politics",
                        "politics",
                        "top_news_us",
                        "top_news"
                    ],
                    "section_title": "WGMD &#8211; The Talk of Delmarva",
                    "title": "Netanyahu Speech at Newsmax Celebration Grabs Intl Attention",
                    "title_full": "Netanyahu Speech at Newsmax Celebration Grabs Intl Attention",
                    "published": "2025-08-14T07:21:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "",
                    "performance_score": 6,
                    "domain_rank": 2621,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-14T07:18:05.000+00:00",
                        "facebook": {
                            "likes": 195,
                            "comments": 113,
                            "shares": 13
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "ec908666d2bb9b890869d068fc73ae0705daa56c",
                "url": "https://www.newsmax.com/newsfront/benjamin-netanyahu-israel-hamas/2025/08/13/id/1222395",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "@newsmax",
                "published": "2025-08-14T07:21:00.000+03:00",
                "title": "Netanyahu Speech at Newsmax Celebration Grabs Intl Attention",
                "text": "Y Net called Israeli Prime Minister Benjamin Netanyahu’s speech at Newsmax’s fourth annual Fourth of July celebration Wednesday “fiery.”",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "positive",
                "categories": [
                    "Politics",
                    "Human Interest",
                    "Economy, Business and Finance"
                ],
                "external_links": [],
                "external_images": [],
                "entities": {
                    "persons": [
                        {
                            "name": "Benjamin Netanyahu",
                            "sentiment": "negative"
                        }
                    ],
                    "organizations": [],
                    "locations": []
                },
                "rating": None,
                "crawled": "2025-08-14T10:17:40.279+03:00",
                "updated": "2025-08-14T07:22:29.000+00:00"
            },
            {
                "thread": {
                    "uuid": "b6b0c64df8e377be93126b343afc35772520447e",
                    "url": "https://www.cbsnews.com/miami/news/judge-delays-alligator-alcatraz-ruling-environmental-concerns/",
                    "site_full": "www.cbsnews.com",
                    "site": "cbsnews.com",
                    "site_section": "https://news.google.com/search?q=for%20when%3a1h&hl=en-us&gl=us&ceid=us%3aen",
                    "site_categories": [
                        "media",
                        "television",
                        "entertainment",
                        "top_news_ca",
                        "top_news_ph",
                        "top_news_iq",
                        "top_news_nz",
                        "top_news_au",
                        "top_news_us",
                        "top_news_za",
                        "top_news_sg",
                        "top_news_kw",
                        "top_news"
                    ],
                    "section_title": "Google News - Search",
                    "title": "Judge delays ruling on \"Alligator Alcatraz\" as environmental groups push for shutdown - CBS Miami",
                    "title_full": "Judge delays ruling on \"Alligator Alcatraz\" as environmental groups push for shutdown - CBS Miami",
                    "published": "2025-08-14T01:08:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://assets3.cbsnewsstatic.com/hub/i/r/2025/08/13/0f06d0ce-9776-4f33-96c2-16100a6ac8b6/thumbnail/1200x630/a668cfb05ab4393f58d53549a4b2d86c/ap25225552217917.jpg",
                    "performance_score": 1,
                    "domain_rank": 216,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T22:17:13.000+00:00",
                        "facebook": {
                            "likes": 10,
                            "comments": 1,
                            "shares": 4
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "b6b0c64df8e377be93126b343afc35772520447e",
                "url": "https://www.cbsnews.com/miami/news/judge-delays-alligator-alcatraz-ruling-environmental-concerns/",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": None,
                "published": "2025-08-14T01:08:00.000+03:00",
                "title": "Judge delays ruling on \"Alligator Alcatraz\" as environmental groups push for shutdown - CBS Miami",
                "text": "The fate of \" Alligator Alcatraz ,\" a controversial immigrant detention center deep in the Florida Everglades, remains uncertain after a federal judge said Wednesday she needs more time to decide whet...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "negative",
                "categories": [
                    "Crime, Law and Justice",
                    "Environment",
                    "Politics"
                ],
                "external_links": [
                    "https://apnews.com/article/alligator-alcatraz-immigration-detainees-florida-cc2fb9e34e760a50e97f13fe59cbf075",
                    "https://apnews.com/article/florida-immigration-alligator-alcatraz-detention-lawsuit-5e669dcf98bbc0bd2af1aeb12c9e747c",
                    "https://apnews.com/article/florida-immigration-alligator-alcatraz-940dd5fda8d22f4f385e2c2800fa525a",
                    "https://apnews.com/article/trump-everglades-immigrant-detention-facility-visit-5dc5568ec15534947c29c9149b773d1d",
                    "https://apnews.com/article/florida-detention-alligator-alcatraz-08aac166ad5fa5dfbd33a00f6be2b979",
                    "https://apnews.com/article/trump-congress-medicaid-snap-states-2e6ac67454045ee402f3361f62a5e97b",
                    "https://apnews.com/article/florida-immigration-detention-center-alligator-alcatraz-contracts-af607a50f1e78ad85f6292cbef0adc92",
                    "https://www.apnews.com/article/trump-congress-medicaid-snap-states-2e6ac67454045ee402f3361f62a5e97b",
                    "https://www.apnews.com/article/alligator-alcatraz-immigration-detainees-florida-cc2fb9e34e760a50e97f13fe59cbf075",
                    "https://www.apnews.com/article/trump-everglades-immigrant-detention-facility-visit-5dc5568ec15534947c29c9149b773d1d",
                    "https://www.apnews.com/article/florida-immigration-alligator-alcatraz-detention-lawsuit-5e669dcf98bbc0bd2af1aeb12c9e747c",
                    "https://www.apnews.com/article/florida-immigration-alligator-alcatraz-940dd5fda8d22f4f385e2c2800fa525a",
                    "https://www.apnews.com/article/florida-immigration-detention-center-alligator-alcatraz-contracts-af607a50f1e78ad85f6292cbef0adc92",
                    "https://www.apnews.com/article/florida-detention-alligator-alcatraz-08aac166ad5fa5dfbd33a00f6be2b979"
                ],
                "external_images": [],
                "entities": {
                    "persons": [
                        {
                            "name": "Kathleen Williams",
                            "sentiment": "none"
                        }
                    ],
                    "organizations": [
                        {
                            "name": "CBS",
                            "sentiment": "negative"
                        }
                    ],
                    "locations": [
                        {
                            "name": "Alcatraz",
                            "sentiment": "none"
                        }
                    ]
                },
                "rating": None,
                "crawled": "2025-08-14T01:16:18.101+03:00",
                "updated": "2025-08-13T22:22:39.000+00:00"
            },
            {
                "thread": {
                    "uuid": "4069366a493fc7b7ffcf20c056d8ba04cadebbbf",
                    "url": "https://www.businessinsider.com/vintage-photos-show-life-behind-the-iron-curtain",
                    "site_full": "www.businessinsider.com",
                    "site": "businessinsider.com",
                    "site_section": "https://mediatize.info/stream",
                    "site_categories": [
                        "media",
                        "tech",
                        "top_news_nz",
                        "top_news_au",
                        "top_news_ae",
                        "top_news_us",
                        "top_news_gb",
                        "top_news_th",
                        "top_news_sg",
                        "top_news_rs",
                        "top_news_ph",
                        "top_news_hk",
                        "top_news_qa",
                        "top_news_ie",
                        "top_news_pk",
                        "top_news_se",
                        "top_news_id",
                        "top_news_dk",
                        "top_news_za",
                        "top_news_my",
                        "top_news_il",
                        "top_news_kw",
                        "top_news_fi",
                        "top_news_ca",
                        "top_news"
                    ],
                    "section_title": "stream de noticias",
                    "title": "Russia Before Putin: Vintage Photos Show Life Behind the Iron Curtain - Business Insider",
                    "title_full": "Russia Before Putin: Vintage Photos Show Life Behind the Iron Curtain - Business Insider",
                    "published": "2025-08-13T21:08:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://i.insider.com/689caa25a17a8c5b4052cafc?width=1200&format=jpeg",
                    "performance_score": 5,
                    "domain_rank": 133,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-13T18:29:49.000+00:00",
                        "facebook": {
                            "likes": 58,
                            "comments": 1,
                            "shares": 27
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "4069366a493fc7b7ffcf20c056d8ba04cadebbbf",
                "url": "https://www.businessinsider.com/vintage-photos-show-life-behind-the-iron-curtain",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "Caroline Fox, Kristine Villarroel",
                "published": "2025-08-13T21:08:00.000+03:00",
                "title": "Russia Before Putin: Vintage Photos Show Life Behind the Iron Curtain - Business Insider",
                "text": "Advertisements\nAdvertising Space – “Top”: $100 per month\nChildren admire a painting on a sunny beach day in Russia. Vladimir Bogdanov/FotoSoyuz/Getty Images\nRussia’s war on Ukraine has deepened a divi...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "neutral",
                "categories": [
                    "Arts, Culture and Entertainment",
                    "Politics"
                ],
                "external_links": [
                    "https://www.history.com/news/reflecting-on-the-berlin-wall-50-years-after-its-construction",
                    "https://www.fastcompany.com/3043204/a-rare-peek-inside-the-shops-of-the-soviet-union",
                    "https://www.smithsonianmag.com/smart-news/soviet-hipsters-bootlegged-banned-music-bone-records-180957505/",
                    "https://foreignpolicy.com/2015/09/15/soviet-bus-stops/",
                    "https://www.theguardian.com/world/gallery/2016/sep/06/soviet-union-rock-music-late-1980s-american-culture-perestroika",
                    "https://geohistory.today/grocery-shopping-russia-1917-present/",
                    "https://geohistory.today/grocery-shopping-russia-1917-present",
                    "https://foreignpolicy.com/2015/09/15/soviet-bus-stops",
                    "https://history.com/news/reflecting-on-the-berlin-wall-50-years-after-its-construction",
                    "https://www.foreignpolicy.com/2015/09/15/soviet-bus-stops/",
                    "https://theguardian.com/world/gallery/2016/sep/06/soviet-union-rock-music-late-1980s-american-culture-perestroika",
                    "https://www.smithsonianmag.com/smart-news/soviet-hipsters-bootlegged-banned-music-bone-records-180957505",
                    "https://fastcompany.com/3043204/a-rare-peek-inside-the-shops-of-the-soviet-union",
                    "https://www.geohistory.today/grocery-shopping-russia-1917-present/",
                    "https://smithsonianmag.com/smart-news/soviet-hipsters-bootlegged-banned-music-bone-records-180957505/"
                ],
                "external_images": [],
                "entities": {
                    "persons": [
                        {
                            "name": "Vladimir Putin",
                            "sentiment": "neutral"
                        },
                        {
                            "name": "Donald Trump",
                            "sentiment": "none"
                        }
                    ],
                    "organizations": [],
                    "locations": [
                        {
                            "name": "Europe",
                            "sentiment": "none"
                        },
                        {
                            "name": "Soviet",
                            "sentiment": "none"
                        }
                    ]
                },
                "rating": None,
                "crawled": "2025-08-13T21:26:48.348+03:00",
                "updated": "2025-08-13T22:43:50.987+03:00"
            },
            {
                "thread": {
                    "uuid": "3a0d25e99919b9988798b1ccc9a7b6418a63bee2",
                    "url": "https://www.businessinsider.com/taylor-swift-eras-tour-physical-discomfort-performance-health-kelce-podcast-2025-8",
                    "site_full": "www.businessinsider.com",
                    "site": "businessinsider.com",
                    "site_section": "https://news.google.com/search?q=was%20when%3a1h&hl=en-us&gl=us&ceid=us%3aen",
                    "site_categories": [
                        "media",
                        "tech",
                        "top_news_nz",
                        "top_news_au",
                        "top_news_ae",
                        "top_news_us",
                        "top_news_gb",
                        "top_news_th",
                        "top_news_sg",
                        "top_news_rs",
                        "top_news_ph",
                        "top_news_hk",
                        "top_news_qa",
                        "top_news_ie",
                        "top_news_pk",
                        "top_news_se",
                        "top_news_id",
                        "top_news_dk",
                        "top_news_za",
                        "top_news_my",
                        "top_news_il",
                        "top_news_kw",
                        "top_news_fi",
                        "top_news_ca",
                        "top_news"
                    ],
                    "section_title": "Google News - Search",
                    "title": "Taylor Swift Says Eras Tour Left Her Feeling 'Perpetual Physical Discomfort' - Business Insider",
                    "title_full": "Taylor Swift Says Eras Tour Left Her Feeling 'Perpetual Physical Discomfort' - Business Insider",
                    "published": "2025-08-14T07:09:00.000+03:00",
                    "replies_count": 0,
                    "participants_count": 1,
                    "site_type": "news",
                    "country": "US",
                    "main_image": "https://i.insider.com/689d4cd3cfc04e97619b6310?width=1200&format=jpeg",
                    "performance_score": 1,
                    "domain_rank": 133,
                    "domain_rank_updated": "2025-06-03T00:00:00.000+03:00",
                    "social": {
                        "updated": "2025-08-14T04:18:11.000+00:00",
                        "facebook": {
                            "likes": 13,
                            "comments": 0,
                            "shares": 1
                        },
                        "vk": {
                            "shares": 0
                        }
                    }
                },
                "uuid": "3a0d25e99919b9988798b1ccc9a7b6418a63bee2",
                "url": "https://www.businessinsider.com/taylor-swift-eras-tour-physical-discomfort-performance-health-kelce-podcast-2025-8",
                "ord_in_thread": 0,
                "parent_url": None,
                "author": "Amanda Goh",
                "published": "2025-08-14T07:09:00.000+03:00",
                "title": "Taylor Swift Says Eras Tour Left Her Feeling 'Perpetual Physical Discomfort' - Business Insider",
                "text": "- Taylor Swift is opening up about the physical toll of performing on her record-breaking Eras Tour.\n- She said she was \"in a state of perpetual physical discomfort\" and had to undergo \"a lot of physi...",
                "highlightText": "",
                "highlightTitle": "",
                "highlightThreadTitle": "",
                "language": "english",
                "sentiment": "negative",
                "categories": [
                    "Arts, Culture and Entertainment",
                    "Health",
                    "Human Interest"
                ],
                "external_links": [
                    "https://youtu.be/M2lX9XESvDE?si=M8Q-Im-ENDrYN0rV",
                    "https://youtu.be/M2lX9XESvDE",
                    "https://www.youtu.be/M2lX9XESvDE?si=M8Q-Im-ENDrYN0rV"
                ],
                "external_images": [],
                "entities": {
                    "persons": [],
                    "organizations": [],
                    "locations": []
                },
                "rating": None,
                "crawled": "2025-08-14T07:11:52.803+03:00",
                "updated": "2025-08-14T04:22:16.000+00:00"
            }
        ],
        "totalResults": 79,
        "moreResultsAvailable": 69,
        "next": "/nextpage",
        "requestsLeft": 926,
        "warnings": None
    }
    mocker.patch("backend.tools.requests.get", return_value=mock_response)
    mocker.patch("backend.tools.get_text_content", return_value="Here is the dummy test content.")
    result = fetch_news_api("US")
    
    assert result["trending_news"][0]["title"] == "Sneak peek: Unmasking the Zombie Hunter - CBS News"
    assert result["trending_news"][1]["title"] == "Dana White says UFC's White House fight card on July 4 will 'absolutely' take place"
    assert result["trending_news"][2]["title"] == "Social media opens a window to traditional trades for young workers"

@patch("backend.tools.requests.get")
def test_fetch_news_api_failure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    result = fetch_news_api("US")
    
    assert result == {"trending_news": "Error fetching news: 404"}


@patch("backend.tools.stripe.Customer.create")
def test_create_stripe_customer(mock_create):
    def side_effect(email): 
        return stripe.Customer.construct_from(
            {
                "id": "cus_NffrFeUfNV2Hib",
                "email": email,
                "object": "customer",
            },
            key="sk_test_123dummy"
        )

    mock_create.side_effect = side_effect
    customer_fake = create_stripe_customer("user@fake.com")
    customer_dummy = create_stripe_customer("user@dummy.com")
    assert customer_fake.id == "cus_NffrFeUfNV2Hib"
    assert customer_dummy.id == "cus_NffrFeUfNV2Hib"
    assert customer_fake.email == "user@fake.com"
    assert customer_dummy.email == "user@dummy.com"



@pytest.mark.asyncio
async def test_update_user_subscription(mocker): 
    
    valid_user = User(
    id=1,
    email ="good@email.com",
    hashed_password = "goodhash",
    is_subscribed = False,
    stripe_customer_id = "cus_valid123",
    stripe_subscription_id = None,
    subscription_status = None,
    subscription_end = None,
    created_at = datetime.now(),
    updated_at = datetime.now(),
    )
    
    mock_scalars = MagicMock()
    mock_scalars.one.return_value = valid_user

    mock_execute_result = MagicMock()
    mock_execute_result.scalars.return_value = mock_scalars

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_execute_result
    mock_session.commit = AsyncMock()

    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_session
    mocker.patch("backend.tools.get_pg_async_session", return_value=mock_context_manager)

    await update_user_subscription("cus_valid123", "sub_321", "active")

    assert valid_user.stripe_subscription_id == "sub_321"
    assert valid_user.subscription_status == "active"
    assert valid_user.is_subscribed == True

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


def test_send_email(mocker): 
    mock_settings = mocker.patch("backend.tools.settings")
    mock_settings.EMAIL_ADDRESS = "sender@test.com"
    mock_settings.EMAIL_PASSWORD = "senderpass"
    mock_server = MagicMock()
    mock_smtp = mocker.patch("backend.tools.SMTP_SSL")
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_email("test@email.com", "Test Subject", "<h1>Test HTML</h1>")

    mock_server.ehlo.assert_called_once()
    mock_server.login.assert_called_once_with("sender@test.com", "senderpass")
    mock_server.send_message.assert_called_once()

    sent_message = mock_server.send_message.call_args[0][0]
    html_part = sent_message.get_payload()[0]
    
    assert sent_message["From"] == "sender@test.com"
    assert sent_message["To"] == "test@email.com"
    assert sent_message["Subject"] == "Test Subject"
    assert html_part.get_payload() == "<h1>Test HTML</h1>"
    assert html_part.get_content_type() == "text/html"
