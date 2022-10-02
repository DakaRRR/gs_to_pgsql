from django.shortcuts import render
from .models import Order
import base64
import io

import pandas as pd
from django.shortcuts import render
import matplotlib.pyplot as plt


def orders(request):
    '''Получение графика заказов отображающихся по стоимости в рублях и срока поставки'''
    df = pd.DataFrame(list(Order.objects.order_by('date_delivery').values()))
    plt.plot(df["date_delivery"], df["price_rub"])
    plt.xlabel("Срок поставки")
    plt.ylabel("Стоимость в рублях")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.figure(figsize=(20, 20))
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return render(request, 'orders_app/index.html', {'data': graphic})
