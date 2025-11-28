from fastapi import FastAPI
from pydantic import BaseModel,  Field ,field_validator
from fastapi.responses import JSONResponse
import agg_trans
import agg_user
import uvicorn
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)

class Item(BaseModel):
    type: str=Field(..., description="The type of the Analysis.")
    year: int=Field(..., description="The year of the Analysis.")
    quarter: str=Field(..., description="The quarter of the Analysis.")
class VarianceInput(BaseModel):
    top_n: int=Field(..., description="Number of top states to consider for variance calculation.")
    
    @field_validator('top_n')
    def validate_top_n(cls, value):
        if value < 1 or value > 10:
            raise ValueError('top_n must be between 1 and 10')
        return value

@app.post("/dataSend")
async def send_data(item: Item):
    data=item.model_dump()
    final_data=[]
    if data['type']=='Transaction':
        data_year_quarter_total=agg_trans.get_aggregated_year_quarter(data['year'],data['quarter'])
        data_year_quarter_total={'total_transactions_amount':data_year_quarter_total[0],
              'total_transactions':data_year_quarter_total[1],
              'average_transaction_value':data_year_quarter_total[2]}
        data_categories=agg_trans.get_categories_data(data['year'],data['quarter']) ##Already a dict
     
        final_data.append(data_year_quarter_total)
        final_data.append(data_categories)
    elif data['type']=='User':
       
        total_users=agg_user.get_aggregated_year_quarter_user(data['year'],data['quarter'])
        data_user={'total_users':total_users}
        final_data.append(data_user)

       
    
    return JSONResponse(status_code=200,content=final_data)
    
@app.post("/barPlot")
async def get_bar_plot():
    image_bar=agg_trans.plot_state_transactions_bar()
    return JSONResponse(status_code=200,content={"image_base64_bar":image_bar})
@app.post("/pieChart")
async def get_pie_chart():
    image_pie=agg_trans.plot_category_pie()
    return JSONResponse(status_code=200,content={"image_base64_pie":image_pie})

@app.post("/Variance")
async def get_variance(item: VarianceInput):
    item=item.model_dump()
    top_n=int(item['top_n'])
    variance_amount=agg_trans.calculate_variance_top_states_amount(top_n)
    variance_transaction=agg_trans.calculate_variance_top_states_transaction(top_n)

    return JSONResponse(status_code=200,content={"variance_amount":variance_amount,"variance_transaction":variance_transaction})

@app.post("/predict")
async def predict(state:str,quarter:int,year:int):
    pass

class DistrictInput(BaseModel):
    dist_name: str = Field(..., description="The district name for analysis.")

@app.post("/distAnalysis")   
async def distAnalysis(item: DistrictInput):
    item=item.model_dump()
    image_base64_dist, var_amount, var_transactions, max_amount, max_trans, min_amount, min_transaction = agg_trans.distAnalysis(item["dist_name"])
    
    return JSONResponse(status_code=200, content={
        "image": image_base64_dist,
        "var_amount": var_amount,
        "var_transactions": var_transactions,
        "max_amount": max_amount,
        "max_trans": max_trans,
        "min_amount": min_amount,
        "min_trans": min_transaction
    })
@app.post('/piePlot')
async def piePlot():
    return JSONResponse(status_code=200,content=agg_trans.distAnalysisPie())

@app.post('/barPlotAnalysis')
async def barPlot(item:DistrictInput):
    item=item.model_dump()
    image_bar=agg_trans.barPlot(item["dist_name"])

    return JSONResponse(status_code=200,content={"image_bar":image_bar})