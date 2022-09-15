resource "aws_vpc" "vpc" {
  cidr_block       = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "example-vpc"
  }
}


resource "aws_subnet" "public" {
  for_each = var.public_subnet_numbers
  vpc_id            = aws_vpc.vpc.id
  availability_zone = each.key
  cidr_block = cidrsubnet(aws_vpc.vpc.cidr_block, 4, each.value)
  map_public_ip_on_launch = true
  tags = {
    Name        = "example-${var.environment}-public-subnet"
    Subnet      = "${each.key}-${each.value}"
  }
}

resource "aws_subnet" "private" {

  for_each = var.private_subnet_numbers
  vpc_id            = aws_vpc.vpc.id
  availability_zone = each.key
  cidr_block = cidrsubnet(aws_vpc.vpc.cidr_block, 4, each.value)

  tags = {
    Name        = "example-${var.environment}-private-subnet"
    Project     = "test"
  }
}

resource "aws_internet_gateway" "mygateway" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "my_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mygateway.id
  }

}
resource "aws_route_table_association" "rta_subnet_public" {
  for_each      = aws_subnet.public

  subnet_id      = each.value.id
  route_table_id = aws_route_table.my_table.id
}


# Elastic-IP (eip) for NAT
resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.mygateway]
}

# NAT gateway sits in first public subnet
resource "aws_nat_gateway" "natgw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public["us-west-1a"].id

  tags = {
    Name        = "nat gw"
    Environment = "${var.environment}"
  }

  depends_on = [aws_internet_gateway.mygateway]
}


resource "aws_route_table" "my_nat_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.natgw.id
  }

}
resource "aws_route_table_association" "rta_subnet_private" {
  for_each      = aws_subnet.private

  subnet_id      = each.value.id
  route_table_id = aws_route_table.my_nat_table.id
}



#   public_subnet_tags = {
#     "kubernetes.io/cluster/${local.cluster_name}" = "shared"
#     "kubernetes.io/role/elb"                      = 1
#   }

#   private_subnet_tags = {
#     "kubernetes.io/cluster/${local.cluster_name}" = "shared"
#     "kubernetes.io/role/internal-elb"             = 1
#   }
# }
