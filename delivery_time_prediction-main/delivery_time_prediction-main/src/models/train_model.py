import os
import sys
sys.path.append('./src')
from logger import logging
from exception import CustomException
from utils import evaulate_model
from utils import save_object
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet


@dataclass
class ModelTrainerCOnfig:
    trained_model_path = os.path.join("artifacts", "model.pkl")


class TrainModel:
    def __init__(self):
        self.model_trainer_config = ModelTrainerCOnfig()

    def initiate_model_traing(self, train_array, test_array):
        try:
            logging.info("Splitting dependent and independent varible")
            x_train, x_test, y_train, y_test = (
                train_array[:, :-1],
                test_array[:, :-1],
                train_array[:, -1],
                test_array[:, -1]
            )

            models = {
                'LinearRegression': LinearRegression(),
                'Lasso': Lasso(),
                'Ridge': Ridge(),
                'ElasticNet': ElasticNet(),
                'RandomForest': RandomForestRegressor()
            }

            model_report:dict = evaulate_model(x_train, x_test, y_train, y_test, models)
            print(model_report)
            print("#" * 50)
            logging.info(f"Model Report: {model_report}")

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            logging.info(f"Best Model is {best_model} with r2_score of {best_model_score}")

            save_object (
                file_path=self.model_trainer_config.trained_model_path,
                obj=best_model
            )

        except Exception as error:
            logging.info("Exception error occured at model training")
            raise CustomException(error, sys)