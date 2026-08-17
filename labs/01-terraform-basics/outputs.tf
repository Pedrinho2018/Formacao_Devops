output "generated_file" {
  description = "Caminho do arquivo criado pelo Terraform."
  value       = local_file.devops_lab.filename
}
