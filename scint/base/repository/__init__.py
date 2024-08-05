from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from scint.base.requests.models import Model


metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)


def start_mappers():
    lines_mapper = mapper(Model.OrderLine, order_lines)
