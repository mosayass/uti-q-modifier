from sdks.novavision.src.helper.package import PackageHelper
from components.QModifier.src.models.QModifierModel import PackageModel, PackageConfigs, ConfigExecutor, \
    QModifierOutputs, QModifierResponse, QModifierExecutor, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    Outputs = QModifierOutputs(outputImage=outputImage)
    qmodifierResponse = QModifierResponse(outputs=Outputs)
    qmodifierExecutor = QModifierExecutor(value=qmodifierResponse)
    executor = ConfigExecutor(value=qmodifierExecutor)
    packageConfigs = PackageConfigs(executor=executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel