resource "aws_ecr_repository" "app_repo" {
  name = "${var.project_name}-${var.environment}-repo"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-repo"
  }
}
