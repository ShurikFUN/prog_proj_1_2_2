
#форматирование новости
def format_news(news_text: dict) -> str:
    title = news_text.get("title", "No title")
    description = news_text.get("description", "No description")
    link = news_text.get("link", "")

    formated_text = f"<b>{title}</b>\n\n{description}\n\nRead more: {link}"
    return formated_text