from aws_cdk.assertions import Match


def lambda_properties(handler, dep_capture, dlq_name, env=None):
    properties = {
        "Handler": handler,
        "Role": {"Fn::GetAtt": [dep_capture, "Arn"]},
        "Runtime": "python3.12",
        "DeadLetterConfig": {"TargetArn": {"Fn::GetAtt": [dlq_name, "Arn"]}},
    }

    if env is not None:
        properties["Environment"] = {
            "Variables": {"EVENT_BUS_ARN": {"Fn::GetAtt": [env, "Arn"]}}
        }

    return properties


def iam_role_properties(dep_capture):
    return {
        "AssumeRolePolicyDocument": {
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                }
            ],
        },
        "ManagedPolicyArns": [
            {
                "Fn::Join": Match.array_with(
                    [
                        [
                            "arn:",
                            {"Ref": "AWS::Partition"},
                            dep_capture,
                        ]
                    ]
                )
            }
        ],
    }
