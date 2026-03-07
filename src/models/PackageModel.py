from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class QValue(Config):
    """
        Input field for the Q modifier value.
    """
    name: Literal["QValue"] = "QValue"
    value: float = Field(default=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["Enter Q Value"] = "Enter Q Value"

    class Config:
        title = "Q Value"

class QModifierInputs(Inputs):
    inputImage: InputImage

# Note: Renamed from PackageConfigs to avoid duplicate class names in the same file
class QModifierRequestConfigs(Configs):
    qValue: QValue

class QModifierOutputs(Outputs):
    outputImage: OutputImage

class QModifierRequest(Request):
    inputs: Optional[QModifierInputs]
    configs: QModifierRequestConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class QModifierResponse(Response):
    outputs: QModifierOutputs

class QModifierExecutor(Config):
    name: Literal["QModifier"] = "QModifier"
    value: Union[QModifierRequest, QModifierResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "QModifier"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[QModifierExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["QModifier"] = "QModifier"

    class Config:
        title = "Package Model"