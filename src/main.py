from typing import List, Union

import uvicorn
from fastapi import FastAPI

from core.schemas import schemas
from evaluators import three_reasons_evaluator, yn_evaluator, wh_question_evaluator, mc_evaluator

PREFIX = '/api/v1'

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs", redoc_url="/api/v1/redoc",
              description="Response Evaluator", version="1.0.0", title=" EVA API",
              servers=[{"url": "/"}])


@app.post(f"{PREFIX}/evaluate", response_model=Union[str, List[str]],
          response_description="Evaluate outputs generated by llm",
          description="Evaluate outputs generated by llm",
          summary="Evaluate outputs generated by llm",
          responses={200: {"description": "List of evaluations results"},
                     500: {"description": "Internal Server Error"}})
async def evaluate(outputs: Union[List[schemas.Output], schemas.Output], evaluation_type: schemas.EvaluationType):
    print(outputs)
    if evaluation_type == 'yes_no':
        if type(outputs) == list:
            result = []
            for output in outputs:
                result.append(yn_evaluator.evaluate_yes_no(output.expected_result, output.generated_result))
            return result
        else:
            return yn_evaluator.evaluate_yes_no(outputs.expected_result, outputs.generated_result)

    if evaluation_type == 'three_reasons':
        if type(outputs) == list:
            result = []
            for output in outputs:
                result.append(
                    three_reasons_evaluator.evaluate_three_reasons(output.expected_result, output.generated_result))
            return result
        else:
            return three_reasons_evaluator.evaluate_three_reasons(outputs.expected_result, outputs.generated_result)
    if evaluation_type == 'wh_question':
        if type(outputs) == list:
            result = []
            for output in outputs:
                result.append(
                    wh_question_evaluator.evaluate_wh_question(output.expected_result, output.generated_result))
            return result
        else:
            return wh_question_evaluator.evaluate_wh_question(outputs.expected_result, outputs.generated_result)
    if evaluation_type == 'mc':
        if type(outputs) == list:
            result = []
            for output in outputs:
                result.append(mc_evaluator.evaluate_mc(output.prompt, output.expected_result, output.generated_result))
            return result
        else:
            return mc_evaluator.evaluate_mc(outputs.prompt, outputs.expected_result, outputs.generated_result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
