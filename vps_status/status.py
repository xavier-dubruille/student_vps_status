from dataclasses import dataclass
from datetime import datetime


@dataclass
class Status:
    group_name: str
    date_time_batch: datetime
    ip_web: str
    url_www: str
    www_https_valid: bool
    content_www_ssl: str
    content_www_http: str
    content_blog_http: str
    ip_ns: str
    date_time: datetime
