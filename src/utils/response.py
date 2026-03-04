from sdks.novavision.src.helper.package import PackageHelper
from components.QModifier.src.models.QModifierModel import QModifierModel, QModifierConfigs, ConfigExecutor, \
    QModifierOutputs, QModifierResponse, QModifierExecutor, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    Outputs = QModifierOutputs(outputImage=outputImage)
    qmodifierResponse = QModifierResponse(outputs=Outputs)
    qmodifierExecutor = QModifierExecutor(value=qmodifierResponse)
    executor = ConfigExecutor(value=qmodifierExecutor)
    qmodifierConfigs = QModifierConfigs(executor=executor)

    package = PackageHelper(packageModel=QModifierModel, packageConfigs=qmodifierConfigs)
    qmodifierModel = package.build_model(context)
    return qmodifierModel