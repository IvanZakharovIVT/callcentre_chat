import aiohttp

from apps.core.config import settings


class KibanaService:
    def __init__(self):
        self.base_url = f"http://{settings.KIBANA_HOST}:{settings.KIBANA_PORT}"
        # Если есть авторизация:
        self.headers = {
            "kbn-xsrf": "true",
            "Content-Type": "application/json"
        }
        # self.auth = aiohttp.BasicAuth("user", "password")

    async def create_data_view(self, index_name: str, time_field: str = "timestamp"):
        """Автоматически создает Data View в Kibana"""
        # Генерируем имя data view (можно совпадать с индексом)
        data_view_name = index_name

        # API для создания data view (Kibana 8.x+)
        url = f"{self.base_url}/api/data_views/data_view"

        payload = {
            "data_view": {
                "name": data_view_name,
                "title": index_name,  # индекс или паттерн (например, "my_index*")
                "timeFieldName": time_field,
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    # Логируем ошибку
                    print(f"Failed to create data view: {await resp.text()}")
                    return None
