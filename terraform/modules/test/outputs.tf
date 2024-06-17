output "webapp_url" {
    value = module.base.webapp_url
}

output "cd_webhook" {
    value = module.base.cd_webhook
    sensitive = true
}