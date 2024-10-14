def lambda_properties(dep_capture):
    return {
        "Handler": "get_fact.handler",
        "Role": {"Fn::GetAtt": [dep_capture, "Arn"]},
        "Runtime": "python3.12",
    }
