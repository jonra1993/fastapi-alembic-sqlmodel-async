locals {
  fastapi = [
    {
      name  = "PROJECT_NAME"
      value = var.PROJECT_NAME
    },
    {
      name  = "FIRST_SUPERUSER_PASSWORD"
      value = var.FIRST_SUPERUSER_PASSWORD
    },
    {
      name  = "FIRST_SUPERUSER_EMAIL"
      value = var.FIRST_SUPERUSER_EMAIL
    },    
    {
      name  = "ENCRYPT_KEY"
      value = var.ENCRYPT_KEY
    },
    {
      name  = "SECRET_KEY"
      value = var.SECRET_KEY
    },
    {
      name  = "BACKEND_CORS_ORIGINS"
      value = jsonencode(var.BACKEND_CORS_ORIGINS)
    }
  ]
  database = [
    {
      name  = "DATABASE_HOST"
      value = var.DATABASE_HOST
    },
    {
      name  = "DATABASE_USER"
      value = var.DATABASE_USER
    },
    {
      name  = "DATABASE_PASSWORD"
      value = var.DATABASE_PASSWORD
    },
    {
      name  = "DATABASE_NAME"
      value = var.DATABASE_NAME
    },
    {
      name  = "DATABASE_PORT"
      value = var.DATABASE_PORT
    }    
  ]
  traefik = [
    {
      name  = "EXT_ENDPOINT1"
      value = var.EXT_ENDPOINT1
    },
    {
      name  = "LOCAL_1"
      value = var.LOCAL_1
    },
    {
      name  = "LOCAL_2"
      value = var.LOCAL_2
    }
  ]
  redis = [
    {
      name  = "REDIS_HOST"
      value = var.REDIS_HOST
    },
    {
      name  = "REDIS_PORT"
      value = var.REDIS_PORT
    }
  ]  
  minio = [
    {
      name  = "MINIO_URL"
      value = var.MINIO_URL
    },
    {
      name  = "MINIO_BUCKET"
      value = var.MINIO_BUCKET
    },
    {
      name  = "MINIO_ROOT_USER"
      value = var.MINIO_ROOT_USER
    },
    {
      name  = "MINIO_ROOT_PASSWORD"
      value = var.MINIO_ROOT_PASSWORD
    }
  ]
  external_apis = [
    {
      name  = "WHEATER_URL"
      value = var.WHEATER_URL
    }
  ]  
}
