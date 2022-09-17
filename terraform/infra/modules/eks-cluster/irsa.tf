resource "kubernetes_service_account" "eks-service-account" {
  metadata {
    name = "demo-user" # This is used as the serviceAccountName in the spec section of the k8 pod manifest
                        # it means that the pod can assume the IAM role with the S3 policy attached
    namespace = "default"

    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.eks-service-account-role.arn
    }
  }
}


resource "aws_iam_role" "eks-service-account-role" {
  name = "workload_sa"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["sts:AssumeRoleWithWebIdentity"]
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Federated = aws_iam_openid_connect_provider.eks-cluster.arn
        }
      },
    ]
  })

  inline_policy {
    name = "eks_service_account_policy"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["s3:GetBucket", "s3:GetObject", "s3:PutObject"]
          Effect   = "Allow"
          Resource = "*"
        },
      ]
    })
  }
}