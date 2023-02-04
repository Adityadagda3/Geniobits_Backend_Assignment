from django.shortcuts import render

# Create your views here.

import asyncio
import csv
import json
from django.shortcuts import render, HttpResponse
from .forms import CSVUploadForm
from .models import Candle

async def read_csv(file, timeframe):
    reader = csv.reader(file)
    header = next(reader)
    candles = []
    for row in reader:
        candles.append(Candle(
            id=row[0],
            open=row[1],
            high=row[2],
            low=row[3],
            close=row[4],
            date=row[5]
        ))
    # Convert the candles to the desired timeframe
    converted_candles = []
    for i in range(0, len(candles), timeframe):
        converted_candles.append(Candle(
            id=candles[i].id,
            open=candles[i].open,
            high=max([candle.high for candle in candles[i:i+timeframe]]),
            low=min([candle.low for candle in candles[i:i+timeframe]]),
            close=candles[i+timeframe-1].close,
            date=candles[i+timeframe-1].date
        ))
    return converted_candles

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            timeframe = form.cleaned_data['timeframe']
            loop = asyncio.get_event_loop()
            candles = loop.run_until_complete(read_csv(csv_file, timeframe))
            # Store the converted candles in a JSON file
            with open('converted_candles.json', 'w') as f:
                json.dump([candle.to_dict() for candle in candles], f)
            # Provide the option to download the JSON file
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="converted_candles.json"'
            response.write(open('converted_candles.json').read())
            return response
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})
