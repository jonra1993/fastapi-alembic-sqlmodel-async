variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

variable "vpc_cidr" {
  description = "CIDR range for the VPC"
  type        = string
  default     = "10.75.0.0/16"
}

variable "availability_zones" {
  type        = list(string)
  description = "List of availability zones"
  default     = ["us-east-1c", "us-east-1d"]
}

variable "instance_type" {
  type        = string
  description = "Instances type"
}

variable "PROJECT_NAME" {
  type        = string
  description = "The name of the project"
  default = "fastapi-sqlmodel-alembic"
}

variable "FIRST_SUPERUSER_PASSWORD" {
  type        = string
  sensitive   = true
  description = "This is the super user password"
}

variable "FIRST_SUPERUSER_EMAIL" {
  type        = string
  description = "The super admin email"
}

variable "ENCRYPT_KEY" {
  type        = string
  sensitive   = true
  description = ""
}

variable "SECRET_KEY" {
  type        = string
  sensitive   = true
  description = "Key used to jwt"
}

variable "BACKEND_CORS_ORIGINS" {
  type        = list(string)
  description = ""
  default = ["*"]
}

variable "DATABASE_HOST" {
  type        = string  
  description = ""  
}

variable "DATABASE_USER" {
  type        = string
  description = ""
}

variable "DATABASE_PASSWORD" {
  type        = string
  sensitive   = true
  description = ""  
}

variable "DATABASE_NAME" {
  type        = string
  description = ""
}

variable "DATABASE_PORT" {
  type        = number
  description = ""
  default = 5432
}

variable "EXT_ENDPOINT1" {
  type        = string
  description = ""
}

variable "LOCAL_1" {
  type        = string
  description = ""
  default = "localhost"
}

variable "LOCAL_2" {
  type        = string
  description = ""
  default = "127.0.0.1"
}

variable "REDIS_HOST" {
  type        = string
  description = ""
  default = "redis_server"
}

variable "REDIS_PORT" {
  type        = number
  description = ""
  default = 6379
}

variable "MINIO_URL" {
  type        = string
  description = ""  
}

variable "MINIO_BUCKET" {
  type        = string
  description = ""
}

variable "MINIO_ROOT_USER" {
  type        = string
  description = ""
}

variable "MINIO_ROOT_PASSWORD" {
  type        = string
  sensitive = true
  description = ""  
}

variable "WHEATER_URL" {
  type        = string
  description = ""  
  default = "https://wttr.in"
}
