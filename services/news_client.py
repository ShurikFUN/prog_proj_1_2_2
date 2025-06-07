from config.settings_news import news_config
import aiohttp
import asyncio


URL = "https://newsdata.io/api/1/news"
_cache = {}

available_topics = {
    "technology": "technology",
    "world": "world",
    "science": "science",
    "health": "health",
    "sports": "sports",
    "business": "business",
    "entertainment": "entertainment"
}

#получение новостей от API
async def get_news(topic: str, language: str = "en", country: str = None):
    api_topic = available_topics.get(topic.lower())
    if not api_topic:
        print(f"Invalid topic: {topic}")
        return []

    #проверка кеша
    key = (api_topic, language, country)
    if key in _cache:
        return _cache[key]

    params = {
        "apikey": news_config.news_key,
        "q": topic,
        "language": language
    }
    #исключения
    try:
        timeout = aiohttp.ClientTimeout(total=10)  # таймаут в 10 секунд

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(URL, params=params) as response:
                if response.status != 200:
                    print(f"Client error: {response.status}")
                    return []
                data = await response.json()
                results = data.get("results", [])
                _cache[key] = results

                print(f"API responded with {len(results)} results for topic '{topic}'")

                return results
    except asyncio.TimeoutError:
        print("Connection timeout")
        return []

    except aiohttp.ClientError as e:
        print(f"Network: {e}")
        return []

    except Exception as e:
        print(f"Error: {e}")
        return []

