import boto3

def script_handler(event, context):
    old_layer_arn = event.get("OldLayerArn")
    new_layer_arn = event.get("NewLayerArn")
    lambda_function_arn = event.get("LambdaFunctionArn")

    # Fetch layer ARNs of the function
    client = boto3.client("lambda")
    response = client.get_function(FunctionName=lambda_function_arn)
    current_layer_arns = []
    layerDetails = response["Configuration"]["Layers"]
    for layerDetail in layerDetails:
        current_layer_arns.append(layerDetail['Arn'])
    print(current_layer_arns)

    # Check if the old layer ARN exists in the function's layers
    if old_layer_arn in current_layer_arns:
        # Replace the old layer ARN with the new layer ARN
        current_layer_arns.remove(old_layer_arn)
        current_layer_arns.append(new_layer_arn)

        # Update the function with the new layer ARN
        response = client.update_function_configuration(
            FunctionName=lambda_function_arn, Layers=current_layer_arns)
        return {
            "message":
            f"Successfully updated layer ARN of function {lambda_function_arn}."
        }
    else:
        return {
            "message":
            f"Old layer ARN {old_layer_arn} not found in function {lambda_function_arn}."
        }