from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from uvicorn import run as app_run
from typing import Optional

# Importing constants and pipeline modules from the project
from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipline.training_pipeline import TrainPipeline

# Initialize FastAPI application
app = FastAPI(title="Vehicle Insurance Prediction API")

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 for templates
templates = Jinja2Templates(directory="templates")

# Allow all origins for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    """
    Helper class to fetch and store form data from HTML inputs.
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    async def get_vehicle_data(self):
        """
        Extract form data asynchronously and convert them to proper numeric types.
        """
        form = await self.request.form()

        # Convert inputs safely (with fallback to None if empty)
        def parse_int(value): return int(value) if value and value.isdigit() else None
        def parse_float(value): return float(value) if value else None

        self.Gender = parse_int(form.get("Gender"))
        self.Age = parse_int(form.get("Age"))
        self.Driving_License = parse_int(form.get("Driving_License"))
        self.Region_Code = parse_float(form.get("Region_Code"))
        self.Previously_Insured = parse_int(form.get("Previously_Insured"))
        self.Annual_Premium = parse_float(form.get("Annual_Premium"))
        self.Policy_Sales_Channel = parse_float(form.get("Policy_Sales_Channel"))
        self.Vintage = parse_int(form.get("Vintage"))
        self.Vehicle_Age_lt_1_Year = parse_int(form.get("Vehicle_Age_lt_1_Year"))
        self.Vehicle_Age_gt_2_Years = parse_int(form.get("Vehicle_Age_gt_2_Years"))
        self.Vehicle_Damage_Yes = parse_int(form.get("Vehicle_Damage_Yes"))


@app.get("/", tags=["UI"])
async def index(request: Request):
    """
    Renders the main form for vehicle data input.
    """
    return templates.TemplateResponse("vehicledata.html", {"request": request, "context": "Enter details"})


@app.get("/train", tags=["Training"])
async def train_route():
    """
    Train the ML model.
    """
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("✅ Training successful!")
    except Exception as e:
        return Response(f"❌ Training failed: {str(e)}")


@app.post("/", tags=["Prediction"])
async def predict_route(request: Request):
    """
    Handle form submission and return predictions.
    """
    try:
        form = DataForm(request)
        await form.get_vehicle_data()

        # Prepare data for prediction
        vehicle_data = VehicleData(
            Gender=form.Gender,
            Age=form.Age,
            Driving_License=form.Driving_License,
            Region_Code=form.Region_Code,
            Previously_Insured=form.Previously_Insured,
            Annual_Premium=form.Annual_Premium,
            Policy_Sales_Channel=form.Policy_Sales_Channel,
            Vintage=form.Vintage,
            Vehicle_Age_lt_1_Year=form.Vehicle_Age_lt_1_Year,
            Vehicle_Age_gt_2_Years=form.Vehicle_Age_gt_2_Years,
            Vehicle_Damage_Yes=form.Vehicle_Damage_Yes,
        )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()
        model_predictor = VehicleDataClassifier()
        prediction = model_predictor.predict(dataframe=vehicle_df)[0]

        status = "Response-Yes ✅" if prediction == 1 else "Response-No ❌"

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": status},
        )

    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
