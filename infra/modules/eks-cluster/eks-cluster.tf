resource "aws_eks_cluster" "demo" {
  name            = "${var.cluster-name}"
  role_arn        = "${aws_iam_role.eks-iam-role.arn}"

  vpc_config {
    security_group_ids = ["${aws_security_group.cluster_security_group_id.id}"]
    subnet_ids         =  "${var.subnets}"
  }
  version = "1.21" # kubeflow install manifests won't work with latest version of Kubernetes
  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.AmazonEKSServicePolicy,
  ]
}



resource "aws_eks_node_group" "example" {
  cluster_name    = aws_eks_cluster.demo.name
  node_group_name = "example-nodes"
  node_role_arn   = aws_iam_role.workernodes.arn
  subnet_ids      = [var.subnets[2], var.subnets[3]] # private subnets

  scaling_config {
    desired_size = 5
    max_size     = 10
    min_size     = 5
  }

  # launch_template {
  #   # custom spec for worker nodes goes here  
  # }

  update_config {
    max_unavailable = 1
  }
  tags = {
    "alpha.eksctl.io/cluster-name" = "${var.cluster-name}"
    "eksctl.cluster.k8s.io/v1alpha1/cluster-name" = "${var.cluster-name}"
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Node Group handling.
  # Otherwise, EKS will not be able to properly delete EC2 Instances and Elastic Network Interfaces.
  depends_on = [
    aws_iam_role_policy_attachment.AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.AmazonEC2ContainerRegistryReadOnly,
  ]
}





# data "aws_ami" "eks-worker" {
#   filter {
#     name   = "name"
#     values = ["amazon-eks-node-${aws_eks_cluster.demo.version}-v*"]
#   }

#   most_recent = true
#   owners      = ["602401143452"] # Amazon EKS AMI Account ID
# }


#### User data for worker launch
#### The launch template to use with the EKS managed node

# locals {
#   demo-node-userdata = <<USERDATA
# #!/bin/bash
# set -o xtrace
# /etc/eks/bootstrap.sh --apiserver-endpoint '${aws_eks_cluster.demo.endpoint}' --b64-cluster-ca '${aws_eks_cluster.demo.certificate_authority.0.data}' '${var.cluster-name}'
# USERDATA
# }

# resource "aws_launch_configuration" "demo" {
#   associate_public_ip_address = true
#   iam_instance_profile        = "${aws_iam_instance_profile.demo-node.name}"
#   image_id                    = "${data.aws_ami.eks-worker.id}"
#   instance_type               = "m4.large"
#   name_prefix                 = "terraform-eks-demo"
#   security_groups             = ["${aws_security_group.demo-node.id}"]
#   user_data_base64            = "${base64encode(local.demo-node-userdata)}"

#   lifecycle {
#     create_before_destroy = true
#   }
# }