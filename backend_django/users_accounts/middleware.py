# myapp/middleware.py

from rich import print
from django.utils.deprecation import MiddlewareMixin
import json


class LogRequestResponseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f"[bold cyan]Request URL:[/bold cyan] {request.path}")
        print(f"[yellow]Method:[/yellow] {request.method}")
        if request.body:
            try:
                # حاول تفك الترميز لو البودي UTF-8
                body_text = request.body.decode('utf-8')
                try:
                    # لو JSON اطبعه بشكل منظم
                    body_json = json.loads(body_text)
                    print(
                        f"[green]Body (JSON):[/green] {json.dumps(body_json, indent=2)}")
                except json.JSONDecodeError:
                    # لو نص عادي اطبعه كما هو
                    print(f"[green]Body (Text):[/green] {body_text}")
            except UnicodeDecodeError:
                # لو مش نص (زى ملف Binary) اطبع تنبيه
                print("[red]Body: <Binary or Non-UTF8 data>[/red]")

    def process_response(self, request, response):
        print(
            f"[bold magenta]Response Status:[/bold magenta] {response.status_code}")
        if hasattr(response, 'content'):
            print(f"[blue]Content:[/blue] {response.content.decode('utf-8')}")
        print("-" * 60)
        return response
