terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "local_file" "devops_lab" {
  filename = "${path.module}/devops-lab-output.txt"
  content  = var.message
}
